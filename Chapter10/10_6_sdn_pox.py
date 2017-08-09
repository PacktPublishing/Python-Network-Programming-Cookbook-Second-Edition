#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 10
# This program is optimized for Python 2.7.12.
# It may run on any other version with/without modifications.
# Adopted from https://github.com/noxrepo/pox/blob/carp/pox/forwarding/hub.py
# For more examples and tutorials: 
#   https://github.com/noxrepo/pox/tree/carp/pox

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpidToStr

log = core.getLogger()

# The listener definition: A simple and stupid hub.
def _handle_ConnectionUp (event):
  msg = of.ofp_flow_mod()
  msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
  event.connection.send(msg)
  # log the action.
  log.info("Hubifying %s", dpidToStr(event.dpid))


# When the application is launched with POX.
def launch ():
  #Add a listener (defined above) to the pox.core openflow.
  core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
  log.info("Hub is running.")
