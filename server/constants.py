import socket

HEADER = 64
PORT = 8000
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
UTF8 = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
