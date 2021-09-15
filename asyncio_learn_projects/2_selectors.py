import socket
import selectors

selector = selectors.DefaultSelector()


def init_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 9090))
    server_socket.listen()

    selector.register(fileobj=server_socket, events=selectors.EVENT_READ, data=accept_connection)


def accept_connection(server_socket):
    client_socket, address = server_socket.accept()
    print('[+] Connection from', address)

    selector.register(fileobj=client_socket, events=selectors.EVENT_READ, data=start_communication)


def start_communication(client_socket):
    request = client_socket.recv(4096)

    if request:
        response = 'Hello world\n'.encode()
        client_socket.send(response)
    else:
        selector.unregister(client_socket)
        client_socket.close()


def event_loop():
    while True:

        events = selector.select()  # (key, events)

        for key, _ in events:
            callback = key.data
            callback(key.fileobj)


if __name__ == '__main__':
    init_server()
    event_loop()
