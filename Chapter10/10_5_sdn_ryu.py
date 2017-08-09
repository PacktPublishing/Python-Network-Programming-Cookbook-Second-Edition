#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 10
# This program is optimized for Python 2.7.12.
# It may run on any other version with/without modifications.
# Adopted from https://github.com/osrg/ryu/blob/master/ryu/app/ws_topology.py

from socket import error as SocketError
from tinyrpc.exc import InvalidReplyError
from ryu.app.wsgi import (
    ControllerBase,
    WSGIApplication,
    websocket,
    WebSocketRPCClient
)
from ryu.base import app_manager
from ryu.topology import event, switches
from ryu.controller.handler import set_ev_cls


class WebSocketTopology(app_manager.RyuApp):
    _CONTEXTS = {
        'wsgi': WSGIApplication,
        'switches': switches.Switches,
    }

    def __init__(self, *args, **kwargs):
        super(WebSocketTopology, self).__init__(*args, **kwargs)

        self.rpc_clients = []

        wsgi = kwargs['wsgi']
        wsgi.register(WebSocketTopologyController, {'app': self})

    # Monitor the events / topology changes
    # EventSwitchEnter and EventSwitchLeave for switches entering and leaving.
    # EventLinkAdd and EventLinkDelete for links addition and deletion.
    # EventHostAdd for hosts addition.

    # Event - Link added
    @set_ev_cls(event.EventLinkAdd)
    def _event_link_add_handler(self, ev):
        msg = ev.link.to_dict()
        self._rpc_broadcall('event_link_add', msg)
    
    # Event - Link deleted
    @set_ev_cls(event.EventLinkDelete)
    def _event_link_delete_handler(self, ev):
        msg = ev.link.to_dict()
        self._rpc_broadcall('event_link_delete', msg)


    def _rpc_broadcall(self, func_name, msg):
        disconnected_clients = []
        for rpc_client in self.rpc_clients:
            rpc_server = rpc_client.get_proxy()
            try:
                getattr(rpc_server, func_name)(msg)
            except SocketError:
                self.logger.debug('WebSocket disconnected: %s', rpc_client.ws)
                disconnected_clients.append(rpc_client)
            except InvalidReplyError as e:
                self.logger.error(e)

        for client in disconnected_clients:
            self.rpc_clients.remove(client)


class WebSocketTopologyController(ControllerBase):

    def __init__(self, req, link, data, **config):
        super(WebSocketTopologyController, self).__init__(
            req, link, data, **config)
        self.app = data['app']

    @websocket('topology', '/v1.0/topology/ws')
    def _websocket_handler(self, ws):
        rpc_client = WebSocketRPCClient(ws)
        self.app.rpc_clients.append(rpc_client)
        rpc_client.serve_forever()

