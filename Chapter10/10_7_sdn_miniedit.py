#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 10
# This program is optimized for Python 2.7.12.
# It may run on any other version with/without modifications.

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=Controller,
                      protocol='tcp',
                      port=6633)

    info( '*** Add switches\n')
    s9 = net.addSwitch('s9', cls=OVSKernelSwitch)
    s8 = net.addSwitch('s8', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch)
    s7 = net.addSwitch('s7', cls=OVSKernelSwitch)
    s6 = net.addSwitch('s6', cls=OVSKernelSwitch)
    s10 = net.addSwitch('s10', cls=OVSKernelSwitch)
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
    h9 = net.addHost('h9', cls=Host, ip='10.0.0.9', defaultRoute=None)
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
    h7 = net.addHost('h7', cls=Host, ip='10.0.0.7', defaultRoute=None)
    h10 = net.addHost('h10', cls=Host, ip='10.0.0.10', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
    h6 = net.addHost('h6', cls=Host, ip='10.0.0.6', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None)
    h11 = net.addHost('h11', cls=Host, ip='10.0.0.11', defaultRoute=None)
    h8 = net.addHost('h8', cls=Host, ip='10.0.0.8', defaultRoute=None)
    h5 = net.addHost('h5', cls=Host, ip='10.0.0.5', defaultRoute=None)

    info( '*** Add links\n')
    s7s1 = {'bw':250,'loss':0}
    net.addLink(s7, s1, cls=TCLink , **s7s1)
    s7s8 = {'bw':250,'loss':0}
    net.addLink(s7, s8, cls=TCLink , **s7s8)
    s8s2 = {'bw':250,'loss':0}
    net.addLink(s8, s2, cls=TCLink , **s8s2)
    net.addLink(s1, s3)
    net.addLink(s1, s4)
    net.addLink(s1, s9)
    net.addLink(s1, s10)
    net.addLink(s1, s5)
    net.addLink(s1, s6)
    net.addLink(s2, s3)
    net.addLink(s2, s4)
    net.addLink(s2, s9)
    net.addLink(s2, s10)
    net.addLink(s2, s5)
    net.addLink(s2, s6)
    net.addLink(s3, h1)
    net.addLink(s3, h2)
    net.addLink(s4, h3)
    net.addLink(s4, h4)
    net.addLink(s9, h5)
    net.addLink(s9, h6)
    net.addLink(s10, h7)
    net.addLink(s10, h8)
    net.addLink(s5, h9)
    net.addLink(s6, h10)
    net.addLink(s6, h11)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s9').start([])
    net.get('s8').start([c0])
    net.get('s4').start([])
    net.get('s5').start([])
    net.get('s7').start([c0])
    net.get('s6').start([])
    net.get('s10').start([])
    net.get('s1').start([])
    net.get('s3').start([])
    net.get('s2').start([])

    info( '*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

