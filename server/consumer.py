"""Handles incoming messages from the client."""

import socket
from abc import ABC, abstractmethod

try:
    from config_loader import config
    import state
    import producer
except ImportError:
    from .config_loader import config
    from . import state
    from . import producer


def client_msg_process(client: socket.socket, addr: str) -> None:
    """Handles a message from the client calling a handler class' handle
    method.
    """
    connected = True
    while connected:
        msg_length = client.recv(config.HEADER).decode("utf-8")
        if not msg_length:
            continue

        msg_length = int(msg_length)
        msg = client.recv(msg_length).decode("utf-8")

        for handler in handler_map:
            if msg.startswith(handler):
                handler_map[handler](client, msg).handle()
                if handler == "DISCONNECT":
                    connected = False
                break
        else:
            raise Exception(f"Unknown message: {msg}")

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
        state.Client.remove_client(self.client)
        print(f"[DISCONNECTED] {self.client.getpeername()} disconnected")


class SubscribeHandler(HandlerBase):
    """Handles subscribing a client to a channel."""

    def handle(self):
        try:
            channel = self.msg.split(" ")[1]
        except IndexError:
            print(f"[ERROR] Invalid message: {self.msg}")
            return

        state.Subscription.add_subscription(self.client, channel)
        print(
            f"[SUBSCRIBED] {self.client.getpeername()} subscribed to {channel}"
        )


class UnsubscribeHandler(HandlerBase):
    """Handles unsubscribing a client from a channel."""

    def handle(self):
        try:
            channel = self.msg.split(" ")[1]
        except IndexError:
            print(f"[ERROR] Invalid message: {self.msg}")
            return

        state.Subscription.remove_subscription(self.client, channel)
        print(
            f"[UNSUBSCRIBED] {self.client.getpeername()} "
            f"unsubscribed from {channel}"
        )


class PublishHandler(HandlerBase):
    """Handles publishing a message to all clients subscribed to a channel."""

    def handle(self):
        msg_components = self.msg.split(" ")
        try:
            channel = msg_components[1]
            msg = " ".join(msg_components[2:])

        except IndexError:
            print(f"[ERROR] Invalid message: {self.msg}")
            return

        producer.publish(client=self.client, channel=channel, msg=msg)
        print(
            f"[PUBLISHED] {self.client.getpeername()} published to {channel}: "
            f"{msg}"
        )


# Map of message types to their corresponding handler classes.
handler_map = {
    "DISCONNECT": DisconnectHandler,
    "SUBSCRIBE": SubscribeHandler,
    "UNSUBSCRIBE": UnsubscribeHandler,
    "PUBLISH": PublishHandler,
}
