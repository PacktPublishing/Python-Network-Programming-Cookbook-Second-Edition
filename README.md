
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


## Related Products
* [Python GUI Programming Cookbook - Second Edition](https://www.packtpub.com/application-development/python-gui-programming-cookbook-second-edition?utm_source=github&utm_medium=repository&utm_content=9781787129450)

* [Modern Python Cookbook](https://www.packtpub.com/application-development/modern-python-cookbook?utm_source=github&utm_medium=repository&utm_content=9781786469250)

* [Python Machine Learning](https://www.packtpub.com/big-data-and-business-intelligence/python-machine-learning?utm_source=github&utm_medium=repository&utm_content=9781783555130)
### Suggestions and Feedback
[Click here](https://docs.google.com/forms/d/e/1FAIpQLSe5qwunkGf6PUvzPirPDtuy1Du5Rlzew23UBp2S-P3wB-GcwQ/viewform) if you have any feedback or suggestions.
