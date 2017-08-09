#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 9
# This program is optimized for Python 2.7.12.
# It may run on any other version with/without modifications.

import sys
import maxinet
from mininet.topolib import TreeTopo

# Emulate a network with depth of depth_ and fanout of fanout_
def emulate(depth_, fanout_):
    # Start the MaxiNet as a Mininet cluster.
    cluster = maxinet.MininetCluster("pc1","pc2","pc3")
    cluster.start()

    # Emulate the network topology.
    emu = maxinet.Emulation(cluster, TreeTopo(depth_,fanout_))

    # Start Execution of the Emulated System.
    emu.setup()

    # Name two of the instances as h1 and h2.
    h1, h2  = net.hosts[0], net.hosts[depth_]

    # Ping from an instance to another, and print the output.
    print (h1.cmd('ping -c1 %s' % h2.IP()))

    # Stop the MaxiNet Emulation.
    emu.stop()
    cluster.stop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Maxinet Simple Emulation')
    parser.add_argument('--depth', action="store", dest="depth", type=int, required=True)
    parser.add_argument('--fanout', action="store", dest="fanout", type=int, required=True)
    given_args = parser.parse_args()
    emulate(given_args.depth, given_args.fanout)

