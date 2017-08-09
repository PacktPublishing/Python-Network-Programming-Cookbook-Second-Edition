#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 7
# This program is optimized for Python 2.7.12 and Python 3.5.2.
# It may run on any other version with/without modifications.

from flask import Flask
app = Flask(__name__)

@app.route('/<int:num>')
def index(num=1):
    return "Your Python Web Service <hr>Fibonacci("+ str(num) + "): "+ str(fibonacci(num))+ "<hr>Square("+ str(num) + "): "+ str(square(num))

def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)


def square(n):
    print ("Calculating for the number %s" %n)
    return n*n

if __name__ == '__main__':
    app.run(debug=True)
