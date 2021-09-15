import threading
import socket

HOST = "192.168.0.14"  # example 192.168.0.14
PORT = 9090  # if you want, you can change

ADMIN_NAME = 'admin'  # admin name for use extra features (kick, ban)
ADMIN_PASS = 'admin'  # admin pass

BLACK_LIST_NAME = 'black_list.txt'  # change it on your own if you want.

clients = []  # list for clients sockets
nicknames = []  # list for active nicknames on server

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))  # binding server to HOST(ip) and PORT(port)
server.listen()  # start server


def broadcast(message):  # message from server to all active clients
    for client in clients:
        client.send(message)


def client_handle(client):
    while True:
        try:
            msg = message = client.recv(1024)
            if msg.decode('ascii').startswith('KICK'):
                if nicknames[clients.index(client)] == ADMIN_NAME:  # checking, is client admin or not
                    name_to_kick = msg.decode('ascii')[5:]  # /kick {name}
                    kick_user(name_to_kick)
                else:
                    client.send('Command was refused!'.encode('ascii'))
            elif msg.decode('ascii').startswith('BAN'):
                if nicknames[clients.index(client)] == ADMIN_NAME:  # checking, is client admin or not
                    name_to_ban = msg.decode('ascii')[4:]  # /ban {name}
                    ban_user(name_to_ban)
                else:
                    client.send('Command was refused!'.encode('ascii'))
            else:
                broadcast(message)
        except:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast(f'{nickname} left the chat!'.encode('ascii'))
                nicknames.remove(nickname)
                break


def accept_clients():
    while True:
        client, address = server.accept()  # accepting connections and unpacking for {client_socket} and {client_IP}
        print(f'Connected with {str(address)}')

        client.send('NICK'.encode('ascii'))  # Sending NICK to client to set up nickname

        nickname = client.recv(1024).decode('ascii')  # getting nickname from client

        with open(BLACK_LIST_NAME, 'r') as f:
            bans = f.readlines()

        if nickname+'\n' in bans:
            client.send('BAN'.encode('ascii'))
            client.close()
            continue

        if nickname == ADMIN_NAME:
            client.send('PASS'.encode('ascii'))
            password = client.recv(1024).decode('ascii')

            if password != ADMIN_PASS:
                client.send('REFUSE'.encode('ascii'))
                client.close()
                continue

        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}!')
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))
        client.send('Connected to the server!'.encode('ascii'))

        thread = threading.Thread(target=client_handle, args=(client,))  # init thread for current client
        thread.start()  # start thread


def kick_user(nickname):
    if nickname in nicknames:
        name_index = nicknames.index(nickname)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        client_to_kick.send('You were kicked!'.encode('ascii'))
        client_to_kick.close()
        nicknames.remove(nickname)
        broadcast(f'{nickname} was kicked!'.encode('ascii'))
        print(f"{nickname} was kicked!")


def ban_user(nickname):
    if nickname in nicknames:
        name_index = nicknames.index(nickname)
        client_to_ban = clients[name_index]
        clients.remove(client_to_ban)
        client_to_ban.send('You were banned!'.encode('ascii'))
        client_to_ban.close()
        nicknames.remove(nickname)
        broadcast(f'{nickname} was banned!'.encode('ascii'))
        with open(BLACK_LIST_NAME, 'a') as f:
            f.write(f'{nickname}\n')
        print(f"{nickname} was banned!")


if __name__ == '__main__':
    try:
        open(BLACK_LIST_NAME, 'r')
        print('Started. Waiting for connections...')
        accept_clients()
    except FileNotFoundError:
        open(BLACK_LIST_NAME, 'w')
