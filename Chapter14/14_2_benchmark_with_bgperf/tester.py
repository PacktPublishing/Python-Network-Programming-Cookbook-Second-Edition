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

from base import Tester
from exabgp import ExaBGP
import os
from  settings import dckr

def rm_line():
    print ('\x1b[1A\x1b[2K\x1b[1D\x1b[1A')


class ExaBGPTester(Tester, ExaBGP):

    CONTAINER_NAME_PREFIX = 'bgperf_exabgp_tester_'

    def __init__(self, name, host_dir, conf, image='bgperf/exabgp'):
        super(ExaBGPTester, self).__init__(name, host_dir, conf, image)

    def configure_neighbors(self, target_conf):
        peers = list(self.conf.get('neighbors', {}).values())

        for p in peers:
            with open('{0}/{1}.conf'.format(self.host_dir, p['router-id']), 'w') as f:
                local_address = p['local-address']
                config = '''neighbor {0} {{
    peer-as {1};
    router-id {2};
    local-address {3};
    local-as {4};
    static {{
'''.format(target_conf['local-address'], target_conf['as'],
               p['router-id'], local_address, p['as'])
                f.write(config)
                for path in p['paths']:
                    f.write('      route {0} next-hop {1};\n'.format(path, local_address))
                f.write('''   }
}''')

    def get_startup_cmd(self):
        startup = ['''#!/bin/bash
ulimit -n 65536''']

        peers = list(self.conf.get('neighbors', {}).values())
        for p in peers:
            startup.append('''env exabgp.log.destination={0}/{1}.log \
exabgp.daemon.daemonize=true \
exabgp.daemon.user=root \
exabgp {0}/{1}.conf'''.format(self.guest_dir, p['router-id']))

        return '\n'.join(startup)
