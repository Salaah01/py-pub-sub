"""Handles outgoing messages to the client."""

import socket
import state
from config_loader import config


def publish(client: socket.socket, channel: str, msg: str) -> None:
    """Publishes a message to a channel."""
    if channel not in state.Subscription.subscriptions:
        return
    for client in state.Subscription.subscriptions[channel]:
        try:
            client.send(f"{len(msg):<{config.HEADER}}".encode())
            client.send(msg.encode())
        except BrokenPipeError:
            state.Client.remove_client(client)
