from .json_socket import JsonSocket


class JsonServer(JsonSocket):
    def __init__(self, address='127.0.0.1', port=5489):
        super(JsonServer, self).__init__(address, port)
        self._bind()

    def _bind(self):
        self.socket.bind((self.address, self.port))

    def _listen(self):
        self.socket.listen(1)

    def _accept(self):
        return self.socket.accept()

    def accept_connection(self):
        self._listen()
        self.conn, addr = self._accept()
        self.conn.settimeout(self.timeout)

    def _is_connected(self):
        return True if not self.conn else False

    connected = property(_is_connected, doc="True if server is connected")
