# Copyright (C) 2016 Nippon Telegraph and Telephone Corporation.
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

from base import *

class Quagga(Container):

    CONTAINER_NAME = None
    GUEST_DIR = '/root/config'

    def __init__(self, host_dir, conf, image='bgperf/quagga'):
        super(Quagga, self).__init__(self.CONTAINER_NAME, image, host_dir, self.GUEST_DIR, conf)

    @classmethod
    def build_image(cls, force=False, tag='bgperf/quagga', checkout='HEAD', nocache=False):
        cls.dockerfile = '''
FROM ubuntu:latest
WORKDIR /root
RUN useradd -M quagga
RUN mkdir /var/log/quagga && chown quagga:quagga /var/log/quagga
RUN mkdir /var/run/quagga && chown quagga:quagga /var/run/quagga
RUN apt-get update && apt-get install -qy git autoconf libtool gawk make telnet libreadline6-dev
RUN git clone git://git.sv.gnu.org/quagga.git quagga
RUN cd quagga && git checkout {0} && ./bootstrap.sh && \
./configure --disable-doc --localstatedir=/var/run/quagga && make && make install
RUN ldconfig
'''.format(checkout)
        super(Quagga, cls).build_image(force, tag, nocache)


class QuaggaTarget(Quagga, Target):

    CONTAINER_NAME = 'bgperf_quagga_target'
    CONFIG_FILE_NAME = 'bgpd.conf'

    def write_config(self, scenario_global_conf):

        config = """hostname bgpd
password zebra
router bgp {0}
bgp router-id {1}
""".format(self.conf['as'], self.conf['router-id'])

        def gen_neighbor_config(n):
            local_addr = n['local-address']
            c = """neighbor {0} remote-as {1}
neighbor {0} advertisement-interval 1
neighbor {0} route-server-client
neighbor {0} timers 30 90
""".format(local_addr, n['as'])
            if 'filter' in n:
                for p in (n['filter']['in'] if 'in' in n['filter'] else []):
                    c += 'neighbor {0} route-map {1} export\n'.format(local_addr, p)
            return c

        with open('{0}/{1}'.format(self.host_dir, self.CONFIG_FILE_NAME), 'w') as f:
            f.write(config)
            for n in list(flatten(list(t.get('neighbors', {}).values()) for t in scenario_global_conf['testers'])) + [scenario_global_conf['monitor']]:
                f.write(gen_neighbor_config(n))

            if 'policy' in scenario_global_conf:
                seq = 10
                for k, v in list(scenario_global_conf['policy'].items()):
                    match_info = []
                    for i, match in enumerate(v['match']):
                        n = '{0}_match_{1}'.format(k, i)
                        if match['type'] == 'prefix':
                            f.write(''.join('ip prefix-list {0} deny {1}\n'.format(n, p) for p in match['value']))
                            f.write('ip prefix-list {0} permit any\n'.format(n))
                        elif match['type'] == 'as-path':
                            f.write(''.join('ip as-path access-list {0} deny _{1}_\n'.format(n, p) for p in match['value']))
                            f.write('ip as-path access-list {0} permit .*\n'.format(n))
                        elif match['type'] == 'community':
                            f.write(''.join('ip community-list standard {0} permit {1}\n'.format(n, p) for p in match['value']))
                            f.write('ip community-list standard {0} permit\n'.format(n))
                        elif match['type'] == 'ext-community':
                            f.write(''.join('ip extcommunity-list standard {0} permit {1} {2}\n'.format(n, *p.split(':', 1)) for p in match['value']))
                            f.write('ip extcommunity-list standard {0} permit\n'.format(n))

                        match_info.append((match['type'], n))

                    f.write('route-map {0} permit {1}\n'.format(k, seq))
                    for info in match_info:
                        if info[0] == 'prefix':
                            f.write('match ip address prefix-list {0}\n'.format(info[1]))
                        elif info[0] == 'as-path':
                            f.write('match as-path {0}\n'.format(info[1]))
                        elif info[0] == 'community':
                            f.write('match community {0}\n'.format(info[1]))
                        elif info[0] == 'ext-community':
                            f.write('match extcommunity {0}\n'.format(info[1]))

                    seq += 10

    def get_startup_cmd(self):
        return '\n'.join(
            ['#!/bin/bash',
             'ulimit -n 65536',
             'bgpd -u root -f {guest_dir}/{config_file_name}']
        ).format(
            guest_dir=self.guest_dir,
            config_file_name=self.CONFIG_FILE_NAME)
