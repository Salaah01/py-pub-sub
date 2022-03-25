import typing as _t
import socket
import threading
import constants
from incoming import client_msg_process
import state

_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
_subscriptions: _t.Dict[str, _t.Set[socket.socket]] = {}


class Server:

    def __init__(self):
        self.server = _server

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
            state.Client.add_client(client)

            thread = threading.Thread(
                target=client_msg_process,
                args=(client, addr)
            )
            thread.start()


if __name__ == '__main__':
    server = Server()
    server.run()
