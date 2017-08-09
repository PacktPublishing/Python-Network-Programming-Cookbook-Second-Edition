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

class GoBGP(Container):

    CONTAINER_NAME = None
    GUEST_DIR = '/root/config'

    def __init__(self, host_dir, conf, image='bgperf/gobgp'):
        super(GoBGP, self).__init__(self.CONTAINER_NAME, image, host_dir, self.GUEST_DIR, conf)

    @classmethod
    def build_image(cls, force=False, tag='bgperf/gobgp', checkout='HEAD', nocache=False):
        cls.dockerfile = '''
FROM golang:1.6
WORKDIR /root
RUN go get -v github.com/osrg/gobgp/gobgpd
RUN go get -v github.com/osrg/gobgp/gobgp
RUN cd $GOPATH/src/github.com/osrg/gobgp && git checkout {0}
RUN go install github.com/osrg/gobgp/gobgpd
RUN go install github.com/osrg/gobgp/gobgp
'''.format(checkout)
        super(GoBGP, cls).build_image(force, tag, nocache)


class GoBGPTarget(GoBGP, Target):

    CONTAINER_NAME = 'bgperf_gobgp_target'
    CONFIG_FILE_NAME = 'gobgpd.conf'

    def write_config(self, scenario_global_conf):

        config = {}
        config['global'] = {
            'config': {
                'as': self.conf['as'],
                'router-id': self.conf['router-id']
            },
        }
        if 'policy' in scenario_global_conf:
            config['policy-definitions'] = []
            config['defined-sets'] = {
                    'prefix-sets': [],
                    'bgp-defined-sets': {
                        'as-path-sets': [],
                        'community-sets': [],
                        'ext-community-sets': [],
                    },
            }
            for k, v in list(scenario_global_conf['policy'].items()):
                conditions = {
                    'bgp-conditions': {},
                }
                for i, match in enumerate(v['match']):
                    n = '{0}_match_{1}'.format(k, i)
                    if match['type'] == 'prefix':
                        config['defined-sets']['prefix-sets'].append({
                            'prefix-set-name': n,
                            'prefix-list': [{'ip-prefix': p} for p in match['value']]
                        })
                        conditions['match-prefix-set'] = {'prefix-set': n}
                    elif match['type'] == 'as-path':
                        config['defined-sets']['bgp-defined-sets']['as-path-sets'].append({
                            'as-path-set-name': n,
                            'as-path-list': match['value'],
                        })
                        conditions['bgp-conditions']['match-as-path-set'] = {'as-path-set': n}
                    elif match['type'] == 'community':
                        config['defined-sets']['bgp-defined-sets']['community-sets'].append({
                            'community-set-name': n,
                            'community-list': match['value'],
                        })
                        conditions['bgp-conditions']['match-community-set'] = {'community-set': n}
                    elif match['type'] == 'ext-community':
                        config['defined-sets']['bgp-defined-sets']['ext-community-sets'].append({
                            'ext-community-set-name': n,
                            'ext-community-list': match['value'],
                        })
                        conditions['bgp-conditions']['match-ext-community-set'] = {'ext-community-set': n}

                config['policy-definitions'].append({
                    'name': k,
                    'statements': [{'name': k, 'conditions': conditions, 'actions': {'route-disposition': {'accept-route': True}}}],
                })


        def gen_neighbor_config(n):
            c = {'config': {'neighbor-address': n['local-address'], 'peer-as': n['as']},
                 'transport': {'config': {'local-address': self.conf['local-address']}},
                 'route-server': {'config': {'route-server-client': True}}}
            if 'filter' in n:
                a = {}
                if 'in' in n['filter']:
                    a['in-policy-list'] = n['filter']['in']
                    a['default-in-policy'] = 'accept-route'
                if 'out' in n['filter']:
                    a['export-policy-list'] = n['filter']['out']
                    a['default-export-policy'] = 'accept-route'
                c['apply-policy'] = {'config': a}
            return c

        config['neighbors'] = [gen_neighbor_config(n) for n in list(flatten(list(t.get('neighbors', {}).values()) for t in scenario_global_conf['testers'])) + [scenario_global_conf['monitor']]]
        with open('{0}/{1}'.format(self.host_dir, self.CONFIG_FILE_NAME), 'w') as f:
            f.write(yaml.dump(config, default_flow_style=False))

    def get_startup_cmd(self):
        return '\n'.join(
            ['#!/bin/bash',
             'ulimit -n 65536',
             'gobgpd -t yaml -f {guest_dir}/{config_file_name} -l {debug_level} > {guest_dir}/gobgpd.log 2>&1']
        ).format(
            guest_dir=self.guest_dir,
            config_file_name=self.CONFIG_FILE_NAME,
            debug_level='info')
