#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 9
# This program is optimized for Python 2.7.12.
# It may run on any other version with/without modifications.

from mininet.net import Mininet
from mininet.node import Controller, OVSKernelAP
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

def emulate():
    # Setting the position of nodes and providing mobility

    # Create a network.
    net = Mininet(controller=Controller, link=TCLink, accessPoint=OVSKernelAP)

    print ("*** Creating nodes")
    # Add the host
    h1 = net.addHost('h1', mac='00:00:00:00:00:01', ip='10.0.0.1/8')

    # Add 3 mobile stations, sta1, sta2, sta3.
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.2/8')
    sta2 = net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.3/8')
    sta3 = net.addStation('sta3', mac='00:00:00:00:00:04', ip='10.0.0.4/8')

    # Add an access point
    ap1 = net.addAccessPoint('ap1', ssid='new-ssid', mode='g', channel='1', position='45,40,30')

    # Add a controller
    c1 = net.addController('c1', controller=Controller)

    print ("*** Configuring wifi nodes")
    net.configureWifiNodes()

    print ("*** Associating and Creating links")
    net.addLink(ap1, h1)
    net.addLink(ap1, sta1)
    net.addLink(ap1, sta2)
    net.addLink(ap1, sta3)

    print ("*** Starting network")
    net.build()
    c1.start()
    ap1.start([c1])

    # Plot a 3-dimensional graph.
    net.plotGraph(max_x=100, max_y=100, max_z=200)

    # Start the mobility at the start of the emulation.
    net.startMobility(time=0)

    # Start the mobile stations from their initial positions.
    net.mobility(sta1, 'start', time=1, position='40.0,30.0,20.0')
    net.mobility(sta2, 'start', time=2, position='40.0,40.0,90.0')
    net.mobility(sta3, 'start', time=3, position='50.0,50.0,160.0')

    # Indicate the final destination of the mobile stations during the emulation.
    net.mobility(sta1, 'stop', time=12, position='31.0,10.0,50.0')
    net.mobility(sta2, 'stop', time=22, position='55.0,31.0,30.0')
    net.mobility(sta3, 'stop', time=32, position='75.0,99.0,120.0')

    # Stop the mobility at certain time.
    net.stopMobility(time=33)

    print ("*** Running CLI")
    CLI(net)

    print ("*** Stopping network")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    emulate()
