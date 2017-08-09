#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 10
# This program is optimized for Python 2.7.12.
# It may run on any other version with/without modifications.

from mininet.net import Mininet
from mininet.node import OVSSwitch, Controller, RemoteController		
from mininet.cli import CLI
from mininet.log import setLogLevel

def execute():

    # Create Mininet instance.
    net = Mininet()

    # Add the SDN controller to the network.
    c1 = net.addController(name='c1', controller=RemoteController,
                                       ip='127.0.0.1')

    # Add hosts to the network.
    h0=net.addHost('h0')
    h1=net.addHost('h1')

    # Add switches to the network.
    s0=net.addSwitch('s0')
    s1=net.addSwitch('s1')
    s2=net.addSwitch('s2')

    # Creating links between the switches in the network
    net.addLink(s0, s1)
    net.addLink(s1, s2)
    net.addLink(s0, s2)

    # Connect hosts to the relevant switches in the network.
    net.addLink(h0, s0)
    net.addLink(h1, s1)

    # Start execution.
    net.start()

    CLI( net )

if __name__ == '__main__':
    setLogLevel( 'info' )  # for CLI output
    execute()
