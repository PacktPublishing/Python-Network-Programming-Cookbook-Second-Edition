#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 12
# This program is optimized for Python 3.5.2 and Python 2.7.12.
# It may run on any other version with/without modifications.


from ciscosparkapi import CiscoSparkAPI

api = CiscoSparkAPI()

# Create a new demo room
demo_room = api.rooms.create('ciscosparkapi Demonstration')
print('Successfully Created the Room')

# Post a message to the new room, and upload an image from a web url.
api.messages.create(demo_room.id, text="Welcome to the room!",
                    files=["https://3.bp.blogspot.com/-wWHD9LVAI7c/WVeyurRmeDI/AAAAAAAADXc/CDY17VfYBdAMbI4GS6dGm2Tc4pHBvmpngCLcBGAs/s1600/IMG_4469.JPG"])
print('Successfully Posted the Message and the Image to the Room')
