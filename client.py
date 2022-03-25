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
    client.send(f'{len(message):<{HEADER}}'.encode(UTF8))
    client.send(message)


def listen():
    while True:
        msg_length = client.recv(HEADER).decode(UTF8)
        if not msg_length:
            continue
        msg_length = int(msg_length)
        msg = client.recv(msg_length).decode(UTF8)
        print(msg)


# send('DISCONNECT Hello 1')
send('SUBSCRIBE Hello')
send('PUBLISH Hello Hello world 2')
listen()
