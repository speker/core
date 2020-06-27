# -*- coding: utf-8 -*-

from core.utilities.tcp.json.threaded_server import ServerFactoryThread
from core.utilities.tcp.json.threaded_server import ServerFactory
from core.utilities.tcp.json.json_socket import JsonSocket


class JsonServer(ServerFactoryThread):
    master = None
    __instance = None

    def __init__(self):
        super(JsonServer, self).__init__()

    @staticmethod
    def start_server(address, port, timeout):
        JsonSocket.timeout = timeout
        JsonSocket.port = port
        JsonSocket.address = address
        server = ServerFactory(JsonServer)
        server.start()

    def _client_connect(self):
        JsonServer.master.client_connect(self)

    def _client_disconnect(self):
        JsonServer.master.client_disconnect()

    def _process_message(self, obj):
        JsonServer.master.incoming_message(obj)

    def send_data(self, obj):
        self.send_obj(obj)
