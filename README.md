
# 	Python Network Programming Cookbook – Second Edition
This is the code repository for [Python Network Programming Cookbook - Second Edition](https://www.packtpub.com/networking-and-servers/python-network-programming-cookbook-second-edition?utm_source=github&utm_medium=repository&utm_content=9781786463999), published by [Packt](https://www.packtpub.com). It contains all the supporting project files necessary to work through the book from start to finish.
## About the Book
Python Network Programming Cookbook - Second Edition highlights the major aspects of network programming in Python, starting from writing simple networking clients to developing and deploying complex Software-Defined Networking (SDN) and Network Functions Virtualization (NFV) systems. It creates the building blocks for many practical web and networking applications that rely on various networking protocols. It presents the power and beauty of Python to solve numerous real-world tasks in the area of network programming, network and system administration, network monitoring, and web-application development.

In this edition, you will also be introduced to network modelling to build your own cloud network. You will learn about the concepts and fundamentals of SDN and then extend your network with Mininet. Next, you’ll find recipes on Authentication, Authorization, and Accounting (AAA) and open and proprietary SDN approaches and frameworks. You will also learn to configure the Linux Foundation networking ecosystem and deploy and automate your networks with Python in the cloud and the Internet scale.

By the end of this book, you will be able to analyze your network security vulnerabilities using advanced network packet capture and analysis techniques.

## Instructions and Navigations
All of the code is organized into folders. Each folder starts with a number followed by the application name. For example, Chapter02.

The code will look like the following:
```
import socket
import select
import argparse

SERVER_HOST = 'localhost'

EOL1 = b'\n\n'
EOL2 = b'\n\r\n'
SERVER_RESPONSE  = b"""HTTP/1.1 200 OK\r\nDate: Mon, 1 Apr 2013 01:01:01 GMT\r\nContent-Type: text/plain\r\nContent-Length: 25\r\n\r\n
Hello from Epoll Server!"""
```
## Software and Hardware Requirements

You need a working PC or laptop, preferably with a modern Linux operating system. The installation instructions are written and tested on Ubuntu 16.04 LTS and would work on any recent Debian-based Linux operating system without modification. We developed for Python 3. However, we have maintained backward-compatibility with Python 2 in our recipes as much as we can. On the other hand, some open source projects used in this book do not yet support Python 3. So, ideally, you will need both Python 2 and Python 3 to test all the recipes in this book.

Most of the recipes in this book will run on other platforms such as Windows and Mac OS with some changes in the configuration steps. Some of the recipes require two or more computers in a cluster to test the distributed systems. You may use Amazon Web Services (AWS) to initiate a cluster inside a single placement group to test these recipes.

You also need a working internet connection to install the third-party software libraries mentioned with respective recipes. If you do not have a stable or continuous internet connection, you can download the third-party libraries and install them in one go. However, it is highly recommended to test some of these recipes with the internet connection, as it would make the configuration task minimal and more interesting, than having to download a bulk of software in bunch. Moreover, testing the application in an AWS cluster would certainly require the internet connectivity.

The following is a list of the Python third-party libraries with their download URLs:

•	ntplib: https://pypi.python.org/pypi/ntplib/

•	diesel: https://pypi.python.org/pypi/diesel/

•	nmap: https://pypi.python.org/pypi/python-nmap

•	scapy: https://pypi.python.org/pypi/scapy

•	netifaces: https://pypi.python.org/pypi/netifaces/

•	netaddr: https://pypi.python.org/pypi/netaddr

•	pyopenssl: https://pypi.python.org/pypi/pyOpenSSL

•	pygeocoder: https://pypi.python.org/pypi/pygocoder

•	pyyaml: https://pypi.python.org/pypi/PyYAML

•	requests: https://pypi.python.org/pypi/requests

•	feedparser: https://pypi.python.org/pypi/feedparser

•	paramiko: https://pypi.python.org/pypi/paramiko/

•	fabric: https://pypi.python.org/pypi/Fabric

•	supervisor: https://pypi.python.org/pypi/supervisor

•	xmlrpclib: https://pypi.python.org/pypi/xmlrpclib

•	SOAPpy: https://pypi.python.org/pypi/SOAPpy

•	bottlenose: https://pypi.python.org/pypi/bottlenose

•	construct: https://pypi.python.org/pypi/construct/

•	libpcap: https://pypi.python.org/pypi/pcap

•	setup tools: https://pypi.python.org/pypi/setuptools

•	exabgp: https://pypi.python.org/pypi/exabgp

•	traixroute: https://pypi.python.org/pypi/traixroute

•	dronekit: https://pypi.python.org/pypi/dronekit

•	dronekit-sitl: https://pypi.python.org/simple/dronekit-sitl/

•	ryu: https://pypi.python.org/pypi/ryu

•	Flask: https://pypi.python.org/pypi/Flask

•	smtpd: https://pypi.python.org/pypi/secure-smtpd

•	twisted: https://pypi.python.org/pypi/Twisted

•	tornado: https://pypi.python.org/pypi/tornado

•	dnspython: https://pypi.python.org/pypi/dnspython

•	ldap3: https://pypi.python.org/pypi/ldap3

•	Eve: https://pypi.python.org/pypi/Eve

•	RequestsThrottler: https://pypi.python.org/pypi/RequestsThrottler

•	PyNSXv: https://pypi.python.org/pypi/pynsxv

•	vmware-nsx: https://pypi.python.org/pypi/vmware-nsx

Other software needed to run some recipes are as follows:

•	postfix: http://www.postfix.org/

•	openssh server: http://www.openssh.com/

•	mysql server: http://downloads.mysql.com/

•	apache2: http://httpd.apache.org/download.cgi/

•	virtualenv: https://virtualenv.pypa.io/

•	filezilla: https://filezilla-project.org/

•	vsftpd: https://security.appspot.com/vsftpd.html

•	telnetd: telnetd.sourceforge.net/

•	curl: https://curl.haxx.se/

•	NS-3: https://www.nsnam.org/ns-3-26/download/

•	Mininet: mininet.org/

•	Ansible: https://www.ansible.com/

•	Git: https://git-scm.com/

•	aptitude: https://www.openhub.net/p/aptitude

•	Node-ws / wscat: https://www.npmjs.com/package/wscat

•	MaxiNet: https://github.com/MaxiNet/MaxiNet/

•	Mininet-WiFi: https://github.com/intrig-unicamp/mininet-wifi

•	ContainerNet: https://github.com/containernet/containernet.git

•	Ant: ant.apache.org/

•	Maven: https://maven.apache.org/

•	OpenDaylight: https://www.opendaylight.org/downloads

•	ONOS: https://wiki.onosproject.org/display/ONOS/Downloads

•	Floodlight: http://www.projectfloodlight.org/download/

•	POX: http://github.com/noxrepo/pox

•	libnl-3-dev: https://packages.debian.org/sid/libnl-3-dev

•	libnl-genl-3-dev: https://packages.debian.org/sid/libnl-genl-3-dev

•	libnl-route-3-dev: https://packages.debian.org/sid/libnl-route-3-dev

•	pkg-config: https://www.freedesktop.org/wiki/Software/pkg-config/

•	python-tz: pytz.sourceforge.net/

•	libpcap-dev: https://packages.debian.org/libpcap-dev

•	libcap2-dev: https://packages.debian.org/jessie/libcap2-dev

•	wireshark: https://www.wireshark.org/

•	Juniper Contrail: http://www.juniper.net/support/downloads/?p=contrail#sw

•	OpenContrail Controller: https://github.com/Juniper/contrail-controller

•	Contrail Server Manager: https://github.com/Juniper/contrail-server-manager.git

•	VMWare NSX for vSphere 6.3.2: https://my.vmware.com/group/vmware/details?downloadGroup=NSXV_632_OSS&productId=417

•	OPNFV Compass: https://wiki.opnfv.org/display/compass4nfv/Compass4nfv

•	OPNFV SDNVPN: https://wiki.opnfv.org/display/sdnvpn/SDNVPN+project+main+page

•	libpcap-dev: https://packages.debian.org/libpcap-dev

•	DPDK: http://dpdk.org/download

•	SNAS.io: http://www.snas.io/

•	pnda.io: http://pnda.io/

•	bgperf: https://github.com/pradeeban/bgperf.git

•	swig: www.swig.org/

•	yabgp: https://github.com/smartbgp/yabgp

•	Virtualbox: https://www.virtualbox.org/wiki/VirtualBox

•	Vagrant: https://www.vagrantup.com/

•	RED PNDA: https://github.com/pndaproject/red-pnda

•	Apache ZooKeeper: https://zookeeper.apache.org/

•	Apache Cassandra: http://cassandra.apache.org/

•	RabbitMQ: https://www.rabbitmq.com/

•	pyIOSXR: https://github.com/fooelisa/pyiosxr

•	Cisco Spark API: https://github.com/CiscoDevNet/ciscosparkapi


## Related Products
* [Python GUI Programming Cookbook - Second Edition](https://www.packtpub.com/application-development/python-gui-programming-cookbook-second-edition?utm_source=github&utm_medium=repository&utm_content=9781787129450)

* [Modern Python Cookbook](https://www.packtpub.com/application-development/modern-python-cookbook?utm_source=github&utm_medium=repository&utm_content=9781786469250)

* [Python Machine Learning](https://www.packtpub.com/big-data-and-business-intelligence/python-machine-learning?utm_source=github&utm_medium=repository&utm_content=9781783555130)
