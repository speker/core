import threading
import time

from core.utilities.tcp.json.json_server import JsonServer
from core.utilities.tcp.json.json_socket import JsonSocket
import socket


class ThreadedServer(threading.Thread, JsonServer):
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        JsonServer.__init__(self, **kwargs)
        self._isAlive = False

    def _process_message(self, obj):
        pass

    def run(self):
        while self._isAlive:
            try:
                self.accept_connection()
            except socket.timeout as e:
                continue
            except Exception as e:
                continue

            while self._isAlive:
                try:
                    obj = self.read_obj()
                    self._process_message(obj)
                except socket.timeout as e:
                    continue
                except Exception as e:
                    self._close_connection()
                    break
            self.close()

    def start(self):
        self._isAlive = True
        super(ThreadedServer, self).start()

    def stop(self):
        self._isAlive = False


class ServerFactoryThread(threading.Thread, JsonSocket):
    def __init__(self, **kwargs):
        threading.Thread.__init__(self, **kwargs)
        JsonSocket.__init__(self, **kwargs)
        self._isAlive = False

    def _process_message(self, obj):
        pass

    def _client_connect(self):
        pass

    def _client_disconnect(self):
        pass

    def swap_socket(self, new_sock):
        del self.socket
        self.socket = new_sock
        self.conn = self.socket
        self._client_connect()

    def run(self):
        while self._isAlive:
            try:
                obj = self.read_obj()
                self._process_message(obj)
            except socket.timeout:
                continue
            except Exception:
                self._client_disconnect()
                self._close_connection()
                self._isAlive = False
                break
        self.close()

    def start(self):
        self._isAlive = True
        super(ServerFactoryThread, self).start()

    def force_stop(self):
        self._isAlive = False


class ServerFactory(ThreadedServer):
    def __init__(self, server_thread, **kwargs):
        ThreadedServer.__init__(self, **kwargs)
        if not issubclass(server_thread, ServerFactoryThread):
            raise TypeError("serverThread not of type", ServerFactoryThread)
        self._thread_type = server_thread
        self._threads = []

    def run(self):
        while self._isAlive:
            tmp = self._thread_type()
            self._purge_threads()
            while not self.connected and self._isAlive:
                try:
                    self.accept_connection()
                except socket.timeout:
                    continue
                except Exception:
                    continue
                else:
                    tmp.swap_socket(self.conn)
                    tmp.start()
                    self._threads.append(tmp)
                    break

        self._wait_to_exit()
        self.close()

    def stop_all(self):
        for t in self._threads:
            if t.isAlive():
                t.force_stop()
                t.join()

    def _purge_threads(self):
        for t in self._threads:
            if not t.isAlive():
                self._threads.remove(t)

    def _wait_to_exit(self):
        while self._get_num_of_active_threads():
            time.sleep(0.2)

    def _get_num_of_active_threads(self):
        return len([True for x in self._threads if x.isAlive()])

    active = property(_get_num_of_active_threads, doc="number of active threads")
