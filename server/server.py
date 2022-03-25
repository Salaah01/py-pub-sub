import typing as _t
import socket
import threading
import constants
from incoming import client_msg_process

_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
_subscriptions: _t.Dict[str, _t.Set[socket.socket]] = {}


class Server:

    def __init__(self):
        self.clients: _t.Dict[str, _t.Set[str]] = {}
        self.server = _server
        self.subscriptions = _subscriptions

    def register_client(self, client: socket.socket) -> None:
        """Registers a client with the server. This method is called when a
        client connects to the server.
        """
        if client not in self.clients:
            self.clients[client] = set()

    def run(self):
        """Opens the connection to the server and starts listening for
        clients.
        """
        self.server.bind(constants.ADDR)
        self.server.listen()

        print(f"[LISTENING] Server is listening on {constants.SERVER}")

        while True:
            client, addr = self.server.accept()
            print(f"[CONNECTED] {addr} connected")
            self.register_client(client)

            thread = threading.Thread(
                target=client_msg_process,
                args=(client, addr)
            )
            thread.start()


if __name__ == '__main__':
    server = Server()
    server.run()
