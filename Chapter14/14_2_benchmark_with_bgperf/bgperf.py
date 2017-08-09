#!/usr/bin/env python
#
# Copyright (C) 2015, 2016 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import yaml
import time
import shutil
import netaddr
import datetime
from argparse import ArgumentParser, REMAINDER
from itertools import chain, islice
from requests.exceptions import ConnectionError
from pyroute2 import IPRoute
from socket import AF_INET
from nsenter import Namespace
from base import *
from exabgp import ExaBGP, ExaBGP_MRTParse
from gobgp import GoBGP, GoBGPTarget
from bird import BIRD, BIRDTarget
from quagga import Quagga, QuaggaTarget
from tester import ExaBGPTester
from mrt_tester import GoBGPMRTTester, ExaBGPMrtTester
from monitor import Monitor
from settings import dckr

from queue import Queue
# Comment out the above line and uncomment the below for Python2.
#from Queue import Queue

from mako.template import Template
from packaging import version
from docker.types import IPAMConfig, IPAMPool

def gen_mako_macro():
    return '''<%
    import netaddr
    from itertools import islice

    it = netaddr.iter_iprange('100.0.0.0','160.0.0.0')

    def gen_paths(num):
        return list('{0}/32'.format(ip) for ip in islice(it, num))
%>
'''

def rm_line():
    print ('\x1b[1A\x1b[2K\x1b[1D\x1b[1A')


def gc_thresh3():
    gc_thresh3 = '/proc/sys/net/ipv4/neigh/default/gc_thresh3'
    with open(gc_thresh3) as f:
        return int(f.read().strip())


def doctor(args):
    ver = dckr.version()['Version']
    if ver.endswith('-ce'):
        curr_version = version.parse(ver.replace('-ce', ''))
    else:
        curr_version = version.parse(ver)
    min_version = version.parse('1.9.0')
    ok = curr_version >= min_version
    print ('docker version ... {1} ({0})'.format(ver, 'ok' if ok else 'update to {} at least'.format(min_version)))

    print ('bgperf image',)
    if img_exists('bgperf/exabgp'):
        print ('... ok')
    else:
        print ('... not found. run `bgperf prepare`')

    for name in ['gobgp', 'bird', 'quagga']:
        print ('{0} image'.format(name),)
        if img_exists('bgperf/{0}'.format(name)):
            print ('... ok')
        else:
            print ('... not found. if you want to bench {0}, run `bgperf prepare`'.format(name))

    print ('/proc/sys/net/ipv4/neigh/default/gc_thresh3 ... {0}'.format(gc_thresh3()))


def prepare(args):
    ExaBGP.build_image(args.force, nocache=args.no_cache)
    ExaBGP_MRTParse.build_image(args.force, nocache=args.no_cache)
    GoBGP.build_image(args.force, nocache=args.no_cache)
    Quagga.build_image(args.force, checkout='quagga-1.0.20160309', nocache=args.no_cache)
    BIRD.build_image(args.force, nocache=args.no_cache)


def update(args):
    if args.image == 'all' or args.image == 'exabgp':
        ExaBGP.build_image(True, checkout=args.checkout, nocache=args.no_cache)
    if args.image == 'all' or args.image == 'exabgp_mrtparse':
        ExaBGP_MRTParse.build_image(True, checkout=args.checkout, nocache=args.no_cache)
    if args.image == 'all' or args.image == 'gobgp':
        GoBGP.build_image(True, checkout=args.checkout, nocache=args.no_cache)
    if args.image == 'all' or args.image == 'quagga':
        Quagga.build_image(True, checkout=args.checkout, nocache=args.no_cache)
    if args.image == 'all' or args.image == 'bird':
        BIRD.build_image(True, checkout=args.checkout, nocache=args.no_cache)


def bench(args):
    config_dir = '{0}/{1}'.format(args.dir, args.bench_name)
    dckr_net_name = args.docker_network_name or args.bench_name + '-br'

    for target_class in [BIRDTarget, GoBGPTarget, QuaggaTarget]:
        if ctn_exists(target_class.CONTAINER_NAME):
            print ('removing target container', target_class.CONTAINER_NAME)
            dckr.remove_container(target_class.CONTAINER_NAME, force=True)

    if not args.repeat:
        if ctn_exists(Monitor.CONTAINER_NAME):
            print ('removing monitor container', Monitor.CONTAINER_NAME)
            dckr.remove_container(Monitor.CONTAINER_NAME, force=True)

        for ctn_name in get_ctn_names():
            if ctn_name.startswith(ExaBGPTester.CONTAINER_NAME_PREFIX) or \
                ctn_name.startswith(ExaBGPMrtTester.CONTAINER_NAME_PREFIX) or \
                ctn_name.startswith(GoBGPMRTTester.CONTAINER_NAME_PREFIX):
                print ('removing tester container', ctn_name)
                dckr.remove_container(ctn_name, force=True)

        if os.path.exists(config_dir):
            shutil.rmtree(config_dir)

    if args.file:
        with open(args.file) as f:
            conf = yaml.load(Template(f.read()).render())
    else:
        conf = gen_conf(args)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        with open('{0}/scenario.yaml'.format(config_dir), 'w') as f:
            f.write(conf)
        conf = yaml.load(Template(conf).render())

    bridge_found = False
    for network in dckr.networks(names=[dckr_net_name]):
        if network['Name'] == dckr_net_name:
            print ('Docker network "{}" already exists'.format(dckr_net_name))
            bridge_found = True
            break
    if not bridge_found:
        subnet = conf['local_prefix']
        print ('creating Docker network "{}" with subnet {}'.format(dckr_net_name, subnet))
        ipam = IPAMConfig(pool_configs=[IPAMPool(subnet=subnet)])
        network = dckr.create_network(dckr_net_name, driver='bridge', ipam=ipam)

    num_tester = sum(len(t.get('neighbors', [])) for t in conf.get('testers', []))
    if num_tester > gc_thresh3():
        print ('gc_thresh3({0}) is lower than the number of peer({1})'.format(gc_thresh3(), num_tester))
        print ('type next to increase the value')
        print ('$ echo 16384 | sudo tee /proc/sys/net/ipv4/neigh/default/gc_thresh3')

    print ('run monitor')
    m = Monitor(config_dir+'/monitor', conf['monitor'])
    m.run(conf, dckr_net_name)

    is_remote = True if 'remote' in conf['target'] and conf['target']['remote'] else False

    if is_remote:
        print ('target is remote ({})'.format(conf['target']['local-address']))

        ip = IPRoute()

        # r: route to the target
        r = ip.get_routes(dst=conf['target']['local-address'], family=AF_INET)
        if len(r) == 0:
            print ('no route to remote target {0}'.format(conf['target']['local-address']))
            sys.exit(1)

        # intf: interface used to reach the target
        idx = [t[1] for t in r[0]['attrs'] if t[0] == 'RTA_OIF'][0]
        intf = ip.get_links(idx)[0]
        intf_name = intf.get_attr('IFLA_IFNAME')

        # raw_bridge_name: Linux bridge name of the Docker bridge
        # TODO: not sure if the linux bridge name is always given by
        #       "br-<first 12 characters of Docker network ID>".
        raw_bridge_name = args.bridge_name or 'br-{}'.format(network['Id'][0:12])

        # raw_bridges: list of Linux bridges that match raw_bridge_name
        raw_bridges = ip.link_lookup(ifname=raw_bridge_name)
        if len(raw_bridges) == 0:
            if not args.bridge_name:
                print('can\'t determine the Linux bridge interface name starting '
                      'from the Docker network {}'.format(dckr_net_name))
            else:
                print('the Linux bridge name provided ({}) seems nonexistent'.format(
                      raw_bridge_name))
            print('Since the target is remote, the host interface used to '
                    'reach the target ({}) must be part of the Linux bridge '
                    'used by the Docker network {}, but without the correct Linux '
                    'bridge name it\'s impossible to verify if that\'s true'.format(
                        intf_name, dckr_net_name))
            if not args.bridge_name:
                print('Please supply the Linux bridge name corresponding to the '
                      'Docker network {} using the --bridge-name argument.'.format(
                          dckr_net_name))
            sys.exit(1)

        # intf_bridge: bridge interface that intf is already member of
        intf_bridge = intf.get_attr('IFLA_MASTER')

        # if intf is not member of the bridge, add it
        if intf_bridge not in raw_bridges:
            if intf_bridge is None:
                print('Since the target is remote, the host interface used to '
                      'reach the target ({}) must be part of the Linux bridge '
                      'used by the Docker network {}'.format(
                          intf_name, dckr_net_name))
                sys.stdout.write('Do you confirm to add the interface {} '
                                 'to the bridge {}? [yes/NO] '.format(
                                     intf_name, raw_bridge_name
                                    ))
                try:
                    answer = input()
                except:
                    print ('aborting')
                    sys.exit(1)
                answer = answer.strip()
                if answer.lower() != 'yes':
                    print ('aborting')
                    sys.exit(1)

                print ('adding interface {} to the bridge {}'.format(
                    intf_name, raw_bridge_name)
                )
                br = raw_bridges[0]

                try:
                    ip.link('set', index=idx, master=br)
                except Exception as e:
                    print('Something went wrong: {}'.format(str(e)))
                    print('Please consider running the following command to '
                          'add the {iface} interface to the {br} bridge:\n'
                          '   sudo brctl addif {br} {iface}'.format(
                              iface=intf_name, br=raw_bridge_name))
                    print('\n\n\n')
                    raise
            else:
                curr_bridge_name = ip.get_links(intf_bridge)[0].get_attr('IFLA_IFNAME')
                print('the interface used to reach the target ({}) '
                      'is already member of the bridge {}, which is not '
                      'the one used in this configuration'.format(
                          intf_name, curr_bridge_name))
                print('Please consider running the following command to '
                        'remove the {iface} interface from the {br} bridge:\n'
                        '   sudo brctl addif {br} {iface}'.format(
                            iface=intf_name, br=curr_bridge_name))
                sys.exit(1)
    else:
        if args.target == 'gobgp':
            target_class = GoBGPTarget
        elif args.target == 'bird':
            target_class = BIRDTarget
        elif args.target == 'quagga':
            target_class = QuaggaTarget

        print ('run', args.target)
        if args.image:
            target = target_class('{0}/{1}'.format(config_dir, args.target), conf['target'], image=args.image)
        else:
            target = target_class('{0}/{1}'.format(config_dir, args.target), conf['target'])
        target.run(conf, dckr_net_name)

    time.sleep(1)

    print ('waiting bgp connection between {0} and monitor'.format(args.target))
    m.wait_established(conf['target']['local-address'])

    if not args.repeat:
        for idx, tester in enumerate(conf['testers']):
            if 'name' not in tester:
                name = 'tester{0}'.format(idx)
            else:
                name = tester['name']
            if 'type' not in tester:
                tester_type = 'normal'
            else:
                tester_type = tester['type']
            if tester_type == 'normal':
                tester_class = ExaBGPTester
            elif tester_type == 'mrt':
                if 'mrt_injector' not in tester:
                    mrt_injector = 'gobgp'
                else:
                    mrt_injector = tester['mrt_injector']
                if mrt_injector == 'gobgp':
                    tester_class = GoBGPMRTTester
                elif mrt_injector == 'exabgp':
                    tester_class = ExaBGPMrtTester
                else:
                    print ('invalid mrt_injector:', mrt_injector)
                    sys.exit(1)
            else:
                print ('invalid tester type:', tester_type)
                sys.exit(1)
            t = tester_class(name, config_dir+'/'+name, tester)
            print ('run tester', name, 'type', tester_type)
            t.run(conf['target'], dckr_net_name)

    start = datetime.datetime.now()

    q = Queue()

    m.stats(q)
    if not is_remote:
        target.stats(q)

    def mem_human(v):
        if v > 1000 * 1000 * 1000:
            return '{0:.2f}GB'.format(float(v) / (1000 * 1000 * 1000))
        elif v > 1000 * 1000:
            return '{0:.2f}MB'.format(float(v) / (1000 * 1000))
        elif v > 1000:
            return '{0:.2f}KB'.format(float(v) / 1000)
        else:
            return '{0:.2f}B'.format(float(v))

    f = open(args.output, 'w') if args.output else None
    cpu = 0
    mem = 0
    cooling = -1
    while True:
        info = q.get()

        if not is_remote and info['who'] == target.name:
            cpu = info['cpu']
            mem = info['mem']

        if info['who'] == m.name:
            now = datetime.datetime.now()
            elapsed = now - start
            recved = info['state']['adj-table']['accepted'] if 'accepted' in info['state']['adj-table'] else 0
            if elapsed.seconds > 0:
                rm_line()
            print ('elapsed: {0}sec, cpu: {1:>4.2f}%, mem: {2}, recved: {3}'.format(elapsed.seconds, cpu, mem_human(mem), recved))
            f.write('{0}, {1}, {2}, {3}\n'.format(elapsed.seconds, cpu, mem, recved)) if f else None
            f.flush() if f else None

            if cooling == args.cooling:
                f.close() if f else None
                return

            if cooling >= 0:
                cooling += 1

            if info['checked']:
                cooling = 0

def gen_conf(args):
    neighbor_num = args.neighbor_num
    prefix = args.prefix_num
    as_path_list = args.as_path_list_num
    prefix_list = args.prefix_list_num
    community_list = args.community_list_num
    ext_community_list = args.ext_community_list_num

    local_address_prefix = netaddr.IPNetwork(args.local_address_prefix)

    if args.target_local_address:
        target_local_address = netaddr.IPAddress(args.target_local_address)
    else:
        target_local_address = local_address_prefix.broadcast - 1

    if args.monitor_local_address:
        monitor_local_address = netaddr.IPAddress(args.monitor_local_address)
    else:
        monitor_local_address = local_address_prefix.ip + 2

    if args.target_router_id:
        target_router_id = netaddr.IPAddress(args.target_router_id)
    else:
        target_router_id = target_local_address

    if args.monitor_router_id:
        monitor_router_id = netaddr.IPAddress(args.monitor_router_id)
    else:
        monitor_router_id = monitor_local_address

    conf = {}
    conf['local_prefix'] = str(local_address_prefix)
    conf['target'] = {
        'as': 1000,
        'router-id': str(target_router_id),
        'local-address': str(target_local_address),
        'single-table': args.single_table,
    }

    if args.target_config_file:
        conf['target']['config_path'] = args.target_config_file

    conf['monitor'] = {
        'as': 1001,
        'router-id': str(monitor_router_id),
        'local-address': str(monitor_local_address),
        'check-points': [prefix * neighbor_num],
    }

    offset = 0

    it = netaddr.iter_iprange('90.0.0.0', '100.0.0.0')

    conf['policy'] = {}

    assignment = []

    if prefix_list > 0:
        name = 'p1'
        conf['policy'][name] = {
            'match': [{
                'type': 'prefix',
                'value': list('{0}/32'.format(ip) for ip in islice(it, prefix_list)),
            }],
        }
        assignment.append(name)

    if as_path_list > 0:
        name = 'p2'
        conf['policy'][name] = {
            'match': [{
                'type': 'as-path',
                'value': list(range(10000, 10000 + as_path_list)),
            }],
        }
        assignment.append(name)

    if community_list > 0:
        name = 'p3'
        conf['policy'][name] = {
            'match': [{
                'type': 'community',
                'value': list('{0}:{1}'.format(i/(1<<16), i%(1<<16)) for i in range(community_list)),
            }],
        }
        assignment.append(name)

    if ext_community_list > 0:
        name = 'p4'
        conf['policy'][name] = {
            'match': [{
                'type': 'ext-community',
                'value': list('rt:{0}:{1}'.format(i/(1<<16), i%(1<<16)) for i in range(ext_community_list)),
            }],
        }
        assignment.append(name)

    neighbors = {}
    configured_neighbors_cnt = 0
    for i in range(3, neighbor_num+3+2):
        if configured_neighbors_cnt == neighbor_num:
            break
        curr_ip = local_address_prefix.ip + i
        if curr_ip in [target_local_address, monitor_local_address]:
            print('skipping tester\'s neighbor with IP {} because it collides with target or monitor'.format(curr_ip))
            continue
        router_id = str(local_address_prefix.ip + i)
        neighbors[router_id] = {
            'as': 1000 + i,
            'router-id': router_id,
            'local-address': router_id,
            'paths': '${{gen_paths({0})}}'.format(prefix),
            'filter': {
                args.filter_type: assignment,
            },
        }
        configured_neighbors_cnt += 1

    conf['testers'] = [{
        'name': 'tester',
        'type': 'normal',
        'neighbors': neighbors,
    }]
    return gen_mako_macro() + yaml.dump(conf, default_flow_style=False)


def config(args):
    conf = gen_conf(args)

    with open(args.output, 'w') as f:
        f.write(conf)


if __name__ == '__main__':
    parser = ArgumentParser(description='BGP performance measuring tool')
    parser.add_argument('-b', '--bench-name', default='bgperf')
    parser.add_argument('-d', '--dir', default='/tmp')
    s = parser.add_subparsers()
    parser_doctor = s.add_parser('doctor', help='check env')
    parser_doctor.set_defaults(func=doctor)

    parser_prepare = s.add_parser('prepare', help='prepare env')
    parser_prepare.add_argument('-f', '--force', action='store_true', help='build even if the container already exists')
    parser_prepare.add_argument('-n', '--no-cache', action='store_true')
    parser_prepare.set_defaults(func=prepare)

    parser_update = s.add_parser('update', help='rebuild bgp docker images')
    parser_update.add_argument('image', choices=['exabgp', 'exabgp_mrtparse', 'gobgp', 'bird', 'quagga', 'all'])
    parser_update.add_argument('-c', '--checkout', default='HEAD')
    parser_update.add_argument('-n', '--no-cache', action='store_true')
    parser_update.set_defaults(func=update)

    def add_gen_conf_args(parser):
        parser.add_argument('-n', '--neighbor-num', default=100, type=int)
        parser.add_argument('-p', '--prefix-num', default=100, type=int)
        parser.add_argument('-l', '--filter-type', choices=['in', 'out'], default='in')
        parser.add_argument('-a', '--as-path-list-num', default=0, type=int)
        parser.add_argument('-e', '--prefix-list-num', default=0, type=int)
        parser.add_argument('-c', '--community-list-num', default=0, type=int)
        parser.add_argument('-x', '--ext-community-list-num', default=0, type=int)
        parser.add_argument('-s', '--single-table', action='store_true')
        parser.add_argument('--target-config-file', type=str,
                            help='target BGP daemon\'s configuration file')
        parser.add_argument('--local-address-prefix', type=str, default='10.10.0.0/16',
                            help='IPv4 prefix used for local addresses; default: 10.10.0.0/16')
        parser.add_argument('--target-local-address', type=str,
                            help='IPv4 address of the target; default: the last address of the '
                                 'local prefix given in --local-address-prefix')
        parser.add_argument('--target-router-id', type=str,
                            help='target\' router ID; default: same as --target-local-address')
        parser.add_argument('--monitor-local-address', type=str,
                            help='IPv4 address of the monitor; default: the second address of the '
                                 'local prefix given in --local-address-prefix')
        parser.add_argument('--monitor-router-id', type=str,
                            help='monitor\' router ID; default: same as --monitor-local-address')

    parser_bench = s.add_parser('bench', help='run benchmarks')
    parser_bench.add_argument('-t', '--target', choices=['gobgp', 'bird', 'quagga'], default='gobgp')
    parser_bench.add_argument('-i', '--image', help='specify custom docker image')
    parser_bench.add_argument('--docker-network-name', help='Docker network name; this is the name given by \'docker network ls\'')
    parser_bench.add_argument('--bridge-name', help='Linux bridge name of the '
                              'interface corresponding to the Docker network; '
                              'use this argument only if bgperf can\'t '
                              'determine the Linux bridge name starting from '
                              'the Docker network name in case of tests of '
                              'remote targets.')
    parser_bench.add_argument('-r', '--repeat', action='store_true', help='use existing tester/monitor container')
    parser_bench.add_argument('-f', '--file', metavar='CONFIG_FILE')
    parser_bench.add_argument('-g', '--cooling', default=0, type=int)
    parser_bench.add_argument('-o', '--output', metavar='STAT_FILE')
    add_gen_conf_args(parser_bench)
    parser_bench.set_defaults(func=bench)

    parser_config = s.add_parser('config', help='generate config')
    parser_config.add_argument('-o', '--output', default='bgperf.yml', type=str)
    add_gen_conf_args(parser_config)
    parser_config.set_defaults(func=config)


    args = parser.parse_args()
    args.func(args)
