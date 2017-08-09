# Copyright (C) 2017 Nippon Telegraph and Telephone Corporation.
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

from tester import Tester
from gobgp import GoBGP
from exabgp import ExaBGP_MRTParse
import os
import yaml
from  settings import dckr
import shutil


class MRTTester(object):

    def get_mrt_file(self, conf, name):
        # conf: tester or neighbor configuration
        if 'mrt-file' in conf:
            mrt_file_path = os.path.expanduser(conf['mrt-file'])

            guest_mrt_file_path = '{guest_dir}/{filename}'.format(
                guest_dir=self.guest_dir,
                filename=name + '.mrt'
            )
            host_mrt_file_path = '{host_dir}/{filename}'.format(
                host_dir=self.host_dir,
                filename=name + '.mrt'
            )
            if not os.path.isfile(host_mrt_file_path):
                shutil.copyfile(mrt_file_path, host_mrt_file_path)
            return guest_mrt_file_path

class ExaBGPMrtTester(Tester, ExaBGP_MRTParse, MRTTester):

    CONTAINER_NAME_PREFIX = 'bgperf_exabgp_mrttester_'

    def __init__(self, name, host_dir, conf, image='bgperf/exabgp_mrtparse'):
        super(ExaBGPMrtTester, self).__init__(name, host_dir, conf, image)

    def configure_neighbors(self, target_conf):
        tester_mrt_guest_file_path = self.get_mrt_file(self.conf, self.name)

        neighbors = list(self.conf.get('neighbors', {}).values())

        for neighbor in neighbors:
            config = '''neighbor {0} {{
    peer-as {1};
    router-id {2};
    local-address {3};
    local-as {4};
    api {{
        processes [ inject_mrt ];
    }}
}}'''.format(target_conf['local-address'], target_conf['as'],
             neighbor['router-id'], neighbor['local-address'],
             neighbor['as'])

            mrt_guest_file_path = self.get_mrt_file(neighbor,
                                                    neighbor['router-id'])
            if not mrt_guest_file_path:
                mrt_guest_file_path = tester_mrt_guest_file_path

            cmd = ['/usr/bin/python', '/root/mrtparse/examples/mrt2exabgp.py']
            cmd += ['-r {router_id}',
                    '-l {local_as}',
                    '-p {peer_as}',
                    '-L {local_addr}',
                    '-n {peer_addr}',
                    '-G',
                    '{mrt_file_path}']

            config += '\n'
            config += 'process inject_mrt {\n'
            config += '    run {cmd};\n'.format(
                cmd=' '.join(cmd).format(
                    router_id = neighbor['router-id'],
                    local_as = neighbor['as'],
                    peer_as = target_conf['as'],
                    local_addr = neighbor['local-address'],
                    peer_addr = target_conf['local-address'],
                    mrt_file_path = mrt_guest_file_path
                )
            )
            config += '    encoder text;\n'
            config += '}\n'

            with open('{0}/{1}.conf'.format(self.host_dir, neighbor['router-id']), 'w') as f:
                f.write(config)

    def get_startup_cmd(self):
        peers = list(self.conf.get('neighbors', {}).values())

        startup = ['#!/bin/bash',
                   'ulimit -n 65536']

        cmd = ['env',
               'exabgp.daemon.daemonize=true',
               'exabgp.daemon.user=root']

        # Higher performances:
        #   exabgp -d config1 config2
        # https://github.com/Exa-Networks/exabgp/wiki/High-Performance
        # WARNING: can not log to files when running multiple configuration
        if self.conf.get('high-perf', False) is True:
            cmd += ['exabgp -d {} >/dev/null 2>&1 &'.format(
                       ' '.join([
                           '{}/{}.conf'.format(self.guest_dir, p['router-id']) for p in peers
                       ])
                   )]
            startup += [' '.join(cmd)]
        else:
            for p in peers:
                startup += [' '.join(
                    cmd + [
                        'exabgp.log.destination={0}/{1}'.format(
                            self.guest_dir, p['router-id']),
                        'exabgp {}/{}.conf'.format(
                            self.guest_dir, p['router-id']),
                        '&'
                    ])
                ]

        return '\n'.join(startup)


class GoBGPMRTTester(Tester, GoBGP, MRTTester):

    CONTAINER_NAME_PREFIX = 'bgperf_gobgp_mrttester_'

    def __init__(self, name, host_dir, conf, image='bgperf/gobgp'):
        super(GoBGPMRTTester, self).__init__(name, host_dir, conf, image)

    def configure_neighbors(self, target_conf):
        conf = list(self.conf.get('neighbors', {}).values())[0]

        config = {
            'global': {
                'config': {
                    'as': conf['as'],
                    'router-id': conf['router-id'],
                }
            },
            'neighbors': [
                {
                    'config': {
                        'neighbor-address': target_conf['local-address'],
                        'peer-as': target_conf['as']
                    }
                }
            ]
        }

        with open('{0}/{1}.conf'.format(self.host_dir, self.name), 'w') as f:
            f.write(yaml.dump(config, default_flow_style=False))
            self.config_name = '{0}.conf'.format(self.name)

    def get_startup_cmd(self):
        conf = list(self.conf.get('neighbors', {}).values())[0]

        mrtfile = self.get_mrt_file(conf, conf['router-id'])
        if not mrtfile:
            mrtfile = self.get_mrt_file(self.conf, self.name)

        startup = '''#!/bin/bash
ulimit -n 65536
gobgpd -t yaml -f {1}/{2} -l {3} > {1}/gobgpd.log 2>&1 &
'''.format(conf['local-address'], self.guest_dir, self.config_name, 'info')

        cmd = ['gobgp', 'mrt']
        if conf.get('only-best', False):
            cmd.append('--only-best')
        cmd += ['inject', 'global', mrtfile]
        if 'count' in conf:
            cmd.append(str(conf['count']))
        if 'skip' in conf:
            cmd.append(str(conf['skip']))

        startup += '\n' + ' '.join(cmd)

        startup += '\n' + 'pkill -SIGHUP gobgpd'
        return startup
