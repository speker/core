import socket
import time

from .json_socket import JsonSocket


class JsonClient(JsonSocket):
    __instance = None

    def __init__(self):
        super(JsonClient, self).__init__()
        if JsonClient.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            JsonClient.__instance = self

    @staticmethod
    def get_instance():
        if JsonClient.__instance is None:
            JsonClient()
        return JsonClient.__instance

    def connect(self, address, port):
        try:
            self.socket.connect((address, port))
        except socket.error:
            time.sleep(3)
        return True

    @staticmethod
    def _process_message(obj):
        print(obj)
