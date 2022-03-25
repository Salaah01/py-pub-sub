import typing as _t
import socket
from config_loader import config

_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class Client:
    def __init__(self):
        self.client = _client

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # self.disconnect()
        # self.client.close()
        print("[CLOSED] Client is closed")

    def connect(self):
        """Opens the connection to the server."""
        self.client.connect(config.ADDR)

    def send_message(self, msg: str) -> None:
        """Sends a message to the server."""
        message = msg.encode('utf-8')
        self.client.send(f"{len(message):<{config.HEADER}}".encode('utf-8'))
        self.client.send(message)

    def receive_message(self) -> str:
        """Receives a message from the server."""
        msg_len = int(self.client.recv(config.HEADER).decode())
        return self.client.recv(msg_len).decode()

    def subscribe(self, channel: str) -> None:
        """Subscribes to a channel."""
        self.send_message(f"SUBSCRIBE {channel}")

    def unsubscribe(self, channel: str) -> None:
        """Unsubscribes from a channel."""
        self.send_message(f"UNSUBSCRIBE {channel}")

    def disconnect(self) -> None:
        """Disconnects from the server."""
        self.send_message("DISCONNECT")

    def publish_message(self, channel: str, msg: str) -> None:
        """Publishes a message to a channel."""
        self.send_message(f"PUBLISH {channel} {msg}")

    def listen(self, func: _t.Callable) -> None:
        """Listens for incoming messages from the server. Any messages that
        are received are passed to the callback function.
        """
        while True:
            msg_len = int(self.client.recv(config.HEADER).decode('utf-8'))
            if not msg_len:
                continue
            func(self.client.recv(int(msg_len)).decode())


if __name__ == "__main__":
    # with Client() as client:
        # client.connect()
        # client.subscribe("test")
        # client.publish_message("test", f"Hello from {client.client.getsockname()}")
        # client.listen(print)
        # print(1111111111111)
    client = Client()
    client.connect()
    client.subscribe("test")
    while True:
        pass
    print('11111111111111')