"""Handles outgoing messages to the client."""

import socket
import constants
import state


def publish(client: socket.socket, channel: str, msg: str) -> None:
    """Publishes a message to a channel."""
    if channel not in state.Subscription.subscriptions:
        print('Channel doesnt exist')
        return
    for client in state.Subscription.subscriptions[channel]:
        try:
            client.send(
                f'{len(msg):<{constants.HEADER}}'.encode(constants.UTF8)
            )
            client.send(msg.encode(constants.UTF8))
        except BrokenPipeError:
            state.Client.remove_client(client)
