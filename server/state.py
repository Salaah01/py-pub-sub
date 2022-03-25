import typing as _t
import socket

_clients: _t.Dict[str, _t.Set[str]] = {}
_subscriptions: _t.Dict[str, _t.Set[socket.socket]] = {}


class Client:
    """Manages clients within the state."""

    clients = _clients

    def __len__(self):
        return len(Client.clients)

    def __contains__(self, client: socket.socket) -> bool:
        return client in Client.clients

    @classmethod
    def add_client(cls, client: socket.socket) -> None:
        """Adds a client to the state."""
        if client not in cls.clients:
            cls.clients[client] = set()

    @classmethod
    def remove_client(cls, client: socket.socket) -> None:
        """Removes a client from the state."""
        if client not in cls.clients:
            return

        for channel in cls.clients[client]:
            Subscription.remove_subscription(client, channel)

        del cls.clients[client]


class Subscription:
    """Manages subscriptions within the state."""

    subscriptions = _subscriptions

    def __len__(self):
        """Returns the number of all subscriptions."""
        return sum(
            len(subscriptions) for subscriptions in self.subscriptions.values()
        )

    @classmethod
    def add_subscription(cls, client: socket.socket, channel: str) -> None:
        """Adds a client to a channel."""
        if channel not in cls.subscriptions:
            cls.subscriptions[channel] = set()

        cls.subscriptions[channel].add(client)

    @classmethod
    def remove_subscription(cls, client: socket.socket, channel: str) -> None:
        """Removes a client from a channel."""
        if channel not in cls.subscriptions:
            return
        try:
            cls.subscriptions[channel].remove(client)
        except KeyError:
            pass
