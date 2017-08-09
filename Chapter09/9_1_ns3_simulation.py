#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 9
# This program is optimized for Python 2.7.12 and Python 3.5.2.
# It may run on any other version with/without modifications.

import ns.applications
import ns.core
import ns.internet
import ns.network
import ns.point_to_point
import argparse


def simulate(ipv4add, ipv4mask):
    # Enabling logs at INFO level for both the server and the client.
    ns.core.LogComponentEnable("UdpEchoClientApplication", ns.core.LOG_LEVEL_INFO)
    ns.core.LogComponentEnable("UdpEchoServerApplication", ns.core.LOG_LEVEL_INFO)
    
    # Create the 2 nodes.
    nodes = ns.network.NodeContainer()
    nodes.Create(2)

    pointToPoint = ns.point_to_point.PointToPointHelper()

    devices = pointToPoint.Install(nodes)

    stack = ns.internet.InternetStackHelper()
    stack.Install(nodes)

    # Set addresses based on the input args.
    address = ns.internet.Ipv4AddressHelper()
    address.SetBase(ns.network.Ipv4Address(ipv4add), ns.network.Ipv4Mask(ipv4mask))

    interfaces = address.Assign(devices)

    # Running the echo server
    echoServer = ns.applications.UdpEchoServerHelper(9)
    serverApps = echoServer.Install(nodes.Get(1))

    # Running the echo client
    echoClient = ns.applications.UdpEchoClientHelper(interfaces.GetAddress(1), 3)
    clientApps = echoClient.Install(nodes.Get(0))

    # Running the simulator
    ns.core.Simulator.Run()
    ns.core.Simulator.Destroy()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='NS-3 Simple Simulation')
    parser.add_argument('--ipv4add', action="store", dest="ipv4add", type=str, required=True)
    parser.add_argument('--ipv4mask', action="store", dest="ipv4mask", type=str, required=True)
    given_args = parser.parse_args()
    simulate(given_args.ipv4add, given_args.ipv4mask)

