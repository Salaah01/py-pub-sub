import socket


HEADER = 64
PORT = 8000
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
UTF8 = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message = msg.encode(UTF8)
    msg_length = len(message)
    send_length = str(msg_length).encode(UTF8)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(UTF8))

send('DISCONNECT Hello 1')
send('DISCONNECT Hello 2')
send('DISCONNECT Hello 3')

send(DISCONNECT_MESSAGE)