import socket
import threading
import state
from consumer import client_msg_process
from config_loader import config


_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class Server:
    def __init__(self):
        self.server = _server

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server.close()
        print("[CLOSED] Server is closed")

    def run(self):
        """Opens the connection to the server and starts listening for
        clients.
        """
        self.server.bind(config.ADDR)
        self.server.listen()

        print(f"[LISTENING] Server is listening on {config.SERVER}")

        while True:
            client, addr = self.server.accept()
            print(f"[CONNECTED] {addr} connected")
            state.Client.add_client(client)

            threading.Thread(
                target=client_msg_process,
                args=(client, addr),
            ).start()


if __name__ == "__main__":
    # with Server() as server:
    # server.run()
    server = Server()
    server.run()
