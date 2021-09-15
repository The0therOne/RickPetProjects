import socket
import threading


HOST = '192.168.0.14'  # Enter server's IP | example 192.168.0.14
PORT = 9090  # change it, it you want

nickname = input("Enter the nickname: ")
if nickname == 'admin':
    password = input("Enter the password: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

stop_thread = False


def receive_from_server():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                next_message = client.recv(1024).decode('ascii')
                if next_message == 'PASS':
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii') == 'REFUSE':
                        print('Connection was refused, wrong password!')
                        stop_thread = True
                elif next_message == 'BAN':
                    print('Connection refused because of ban!')
                    stop_thread = True
            else:
                print(message)
        except:
            print('Connection lost! Press ENTER to continue...')
            client.close()
            stop_thread = True
            break


def communication_with_users():
    while True:
        if stop_thread:
            break

        message = f"{nickname}: {input('')}"

        if message[len(nickname)+2:].startswith('/'):  # Admin: /
            if nickname == 'admin':
                if message[len(nickname)+2:].startswith('/kick'):  # Admin: /
                    client.send(f'KICK {message[len(nickname)+2+6:]}'.encode('ascii'))  # username: /kick (here)
                elif message[len(nickname)+2:].startswith('/ban'):
                    client.send(f'BAN {message[len(nickname)+2+5:]}'.encode('ascii'))
            else:
                print("Commands can only be executed by the admin!")
        else:
            if stop_thread:
                break
            client.send(message.encode('ascii'))


receive_thread = threading.Thread(target=receive_from_server)
receive_thread.start()

communication_thread = threading.Thread(target=communication_with_users)
communication_thread.start()
