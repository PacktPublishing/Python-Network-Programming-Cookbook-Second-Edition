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

class BIRD(Container):

    CONTAINER_NAME = None
    GUEST_DIR = '/root/config'

    def __init__(self, host_dir, conf, image='bgperf/bird'):
        super(BIRD, self).__init__(self.CONTAINER_NAME, image, host_dir, self.GUEST_DIR, conf)

    @classmethod
    def build_image(cls, force=False, tag='bgperf/bird', checkout='HEAD', nocache=False):
        cls.dockerfile = '''
FROM ubuntu:latest
WORKDIR /root
RUN apt-get update && apt-get install -qy git autoconf libtool gawk make \
flex bison libncurses-dev libreadline6-dev
RUN apt-get install -qy flex
RUN git clone https://gitlab.labs.nic.cz/labs/bird.git bird
RUN cd bird && git checkout {0} && autoreconf -i && ./configure && make && make install
'''.format(checkout)
        super(BIRD, cls).build_image(force, tag, nocache)


class BIRDTarget(BIRD, Target):

    CONTAINER_NAME = 'bgperf_bird_target'
    CONFIG_FILE_NAME = 'bird.conf'

    def write_config(self, scenario_global_conf):
        config = '''router id {0};
listen bgp port 179;
protocol device {{ }}
protocol direct {{ disabled; }}
protocol kernel {{ disabled; }}
table master{1};
'''.format(self.conf['router-id'], ' sorted' if self.conf['single-table'] else '')

        def gen_filter_assignment(n):
            if 'filter' in n:
                c = []
                if 'in' not in n['filter'] or len(n['filter']['in']) == 0:
                    c.append('import all;')
                else:
                    c.append('import where {0};'.format( '&&'.join(x + '()' for x in n['filter']['in'])))

                if 'out' not in n['filter'] or len(n['filter']['out']) == 0:
                    c.append('export all;')
                else:
                    c.append('export where {0};'.format( '&&'.join(x + '()' for x in n['filter']['out'])))

                return '\n'.join(c)
            return '''import all;
export all;
'''

        def gen_neighbor_config(n):
            return ('''table table_{0};
protocol pipe pipe_{0} {{
    table master;
    mode transparent;
    peer table table_{0};
{1}
}}'''.format(n['as'], gen_filter_assignment(n)) if not self.conf['single-table'] else '') + '''protocol bgp bgp_{0} {{
    local as {1};
    neighbor {2} as {0};
    {3};
    import all;
    export all;
    rs client;
}}
'''.format(n['as'], self.conf['as'], n['local-address'], 'secondary' if self.conf['single-table'] else 'table table_{0}'.format(n['as']))
            return n1 + n2

        def gen_prefix_filter(name, match):
            return '''function {0}()
prefix set prefixes;
{{
prefixes = [
{1}
];
if net ~ prefixes then return false;
return true;
}}
'''.format(name, ',\n'.join(match['value']))

        def gen_aspath_filter(name, match):
            c = '''function {0}()
{{
'''.format(name)
            c += '\n'.join('if (bgp_path ~ [= * {0} * =]) then return false;'.format(v) for v in match['value'])
            c += '''
return true;
}
'''
            return c

        def gen_community_filter(name, match):
            c = '''function {0}()
{{
'''.format(name)
            c += '\n'.join('if ({0}, {1}) ~ bgp_community then return false;'.format(*v.split(':')) for v in match['value'])
            c += '''
return true;
}
'''
            return c

        def gen_ext_community_filter(name, match):
            c = '''function {0}()
{{
'''.format(name)
            c += '\n'.join('if ({0}, {1}, {2}) ~ bgp_ext_community then return false;'.format(*v.split(':')) for v in match['value'])
            c += '''
return true;
}
'''
            return c



        def gen_filter(name, match):
            c = ['function {0}()'.format(name), '{']
            for typ, name in match:
                c.append(' if ! {0}() then return false;'.format(name))
            c.append('return true;')
            c.append('}')
            return '\n'.join(c) + '\n'

        with open('{0}/{1}'.format(self.host_dir, self.CONFIG_FILE_NAME), 'w') as f:
            f.write(config)

            if 'policy' in scenario_global_conf:
               for k, v in list(scenario_global_conf['policy'].items()):
                    match_info = []
                    for i, match in enumerate(v['match']):
                        n = '{0}_match_{1}'.format(k, i)
                        if match['type'] == 'prefix':
                            f.write(gen_prefix_filter(n, match))
                        elif match['type'] == 'as-path':
                            f.write(gen_aspath_filter(n, match))
                        elif match['type'] == 'community':
                            f.write(gen_community_filter(n, match))
                        elif match['type'] == 'ext-community':
                            f.write(gen_ext_community_filter(n, match))
                        match_info.append((match['type'], n))
                    f.write(gen_filter(k, match_info))

            for n in sorted(list(flatten(list(t.get('neighbors', {}).values()) for t in scenario_global_conf['testers'])) + [scenario_global_conf['monitor']], key=lambda n: n['as']):
                f.write(gen_neighbor_config(n))
            f.flush()

    def get_startup_cmd(self):
        return '\n'.join(
            ['#!/bin/bash',
             'ulimit -n 65536',
             'bird -c {guest_dir}/{config_file_name}']
        ).format(
            guest_dir=self.guest_dir,
            config_file_name=self.CONFIG_FILE_NAME)
