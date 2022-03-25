"""Handles incoming messages from the client."""

import socket
from abc import ABC, abstractmethod
import constants

def client_msg_process(client: socket.socket, addr: str) -> None:
    """Handles a message from the client calling a handler class' handle
    method.
    """
    while True:
        msg_length = client.recv(constants.HEADER).decode(constants.UTF8)
        if not msg_length:
            continue

        msg_length = int(msg_length)
        msg = client.recv(msg_length).decode(constants.UTF8)

        Handler: HandlerBase
        if msg.startswith('DISCONNECT'):
            Handler = DisconnectHandler
        else:
            raise ValueError(f"Invalid message: {msg}")
        handler = Handler(client, msg)
        handler.handle()
    
    client.close()


class HandlerBase(ABC):
    """Base class for all handlers."""

    def __init__(self, client: socket.socket, msg: str):
        self.client = client
        self.msg = msg

    @abstractmethod
    def handle(self):
        """Handles the incoming message."""
        pass


class DisconnectHandler(HandlerBase):
    """Handles the disconnection message."""

    def handle(self):
        print(f"{self.msg} disconnected.")
