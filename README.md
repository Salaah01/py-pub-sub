# Pub-Sub
A simple pub-sub implementation in Python.

Data will be stored in memory and so will be lost if the program is terminated.

There are two main apps in this project: server and client.

The server is a simple TCP server that listens for connections on a port. It has the ability to accept connections and send data to clients.

Client is a simple TCP client that connects to a server and sends data.

The client is able to subscribe to channels and receive publish messages from the server.

## Sections
- [Pub-Sub](#pub-sub)
  - [Sections](#sections)
  - [Installation](#installation)
  - [Setup](#setup)
  - [Running the Server](#running-the-server)
  - [Using the Client](#using-the-client)
  - [Setting Up the Pub-Sub](#setting-up-the-pub-sub)
    - [Server](#server)
    - [Client - Listening](#client---listening)
    - [Client - Publishing](#client---publishing)
## Installation
The application uses Python's standard library only and so there are no dependencies.

## Setup
Review `config.py` to check if you are happy with the settings. The default settings should be fine in most cases. But you may wish to change the port or change the server address to `0.0.0.0`.

## Running the Server
To run the server, run any of the following two commands:
```python
python3 -m server
```
or 
```python
python3 server/server.py 
```

## Using the Client
In `client/client.py` there is a `Client` class that can be used to communicate with the server.

The client can be used as a context manager. This is the recommended way to use the client so that it may handle errors and gracefully close the connection.

```python
with Client() as client:
  # Do stuff
```

Below is a guide of how you can use the client object.

**Connecting to the server**
```python
client.connect()
```

**Disconnect from the server.**
```python
client.disconnect()
```

**Sending messages**
```python
message = 'My message'
client.send_message(message)
```

**Receiving messages**
This will block the current thread until a message is received.
```python
client.receive_message()
```

**Publishing messages to a channel**
```python
channel = 'my_channel
message  = 'My message'
client.publish_message(channel, message)
```

**Subscribe to a channel**
```python
channel = 'my_channel'
client.subscribe(channel)
```

**Unsubscribing from a channel**
```python
channel = 'my_channel'
client.unsubscribe(channel)
```

**Listening for messages on all subscribed channels.**
This is a blocking call and will continue to listen until the process is interrupted.
The `client.listen` function takes a function that will be called when a message is received. The function will be called with the message as the only argument.

```python
def my_function(message):
  print(f'message received: {message})

client.listen(my_function)
```
## Setting Up the Pub-Sub
You will need three shells to run the server and two instances of the client, one for listening and one for publishing messages.

### Server
On one shell, run the server:
```python
python3 -m server
```

### Client - Listening
Within your code where you wish to use the client you will need to import the
`Client` class.

```python
from client.client import Client
```
(I know, that's a lot of clients!)

Next, create some function that will be called when a message is received.
We will create a modified print statement.

```python
def my_print(message):
    print(f'message received: {message}')
```

Subscribe to some channels and listen for messages.
```python
with Client() as consumer:
    consumer.connect()
    consumer.subscribe('channel1')
    consumer.subscribe('channel2')
    consumer.listen(my_print)
```
The consumer will now listen for any new messages in `channel1` and `channel2` and call the `my_print` function when a message is received.

### Client - Publishing
Import the `Client` class.

```python
from client.client import Client
```

Publish a message.
```python
with Client() as producer:
    producer.connect()
    producer.publish_message('channel1', 'message1')
```

Now, all clients subscribed to `channel1` will receive the message.
