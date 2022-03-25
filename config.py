"""Configuration file."""

import socket

# Size of the initial message from the client.
HEADER = 64
# Port to listen on.
PORT = 8000
# Server's IP. If you want to make this server public, change this to
# `SERVER = '0.0.0.0`.
SERVER = socket.gethostbyname(socket.gethostname())
# You shouldn't need to change this. This is a tuple of the IP and TCP port
# bind to.
ADDR = (SERVER, PORT)
