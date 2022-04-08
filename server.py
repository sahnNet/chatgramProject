# import socket library
import socket
from time import sleep

from colorama import Fore
# import threading library
import threading

import dataBase as db
import serverTOClient as stoc

# Choose a port that is free
PORT = 50000

# An IPv4 address is obtained
# for the server.
SERVER = 'localhost'

# Address is stored as a tuple
ADDRESS = (SERVER, PORT)

# the format in which encoding
# and decoding will occur
FORMAT = "utf-8"

# Lists that will contains
# all the clients connected to
# the server and their names.
clients = {}


def body_to_dict(body):
    items = {}
    for b in body:
        k, v = b.split(':')
        k = k.split('<')[-1]
        v = v.split('>')[0]
        items[k] = v
    return items


def send_to_all(message):
    for client in clients.values():
        client.send(stoc.message(message).encode(FORMAT))


def register(body):
    items = body_to_dict(body)
    result = db.creat_user(username=items['user'], password=items['pass'])
    return stoc.register_message(result)


def login(body):
    items = body_to_dict(body)
    result = db.is_exist(username=items['user'], password=items['pass'])
    return stoc.login_message(result)


def group(body, connection):
    items = body_to_dict(body)
    clients[items['user']] = connection
    sleep(1)
    send_to_all(f"{items['user']} join the chat room.")
    send_to_all(f"Hi {items['user']}, welcome to the chat room.")


# method to handle the
# incoming messages
def handle(conn, addr):
    while True:
        # receive message
        message = conn.recv(1024).decode(FORMAT)
        flag = True
        result = ''
        body = message.split(' -Option ')
        command = body.pop(0)

        if command == 'Make':
            result = register(body=body)
        elif command == 'Connect':
            result = login(body=body)
        elif command == 'Group':
            group(body=body, connection=conn)
        elif command == 'Message':
            send_to_all(body[0])
        else:
            flag = False

        if flag:
            print(Fore.LIGHTCYAN_EX + f"{addr} to server : {message}")
            if result != '':
                conn.send(result.encode(FORMAT))
                print(Fore.BLUE + f"Server to {addr} : {result}")

    # close the connection
    # conn.close()


if __name__ == '__main__':
    # Create a new socket for
    # the server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind the address of the
    # server to the socket
    server.bind(ADDRESS)
    server.listen()

    while True:
        # accept connections and returns
        # a new connection to the client
        # and the address bound to it
        conn, addr = server.accept()
        # Start the handling thread
        thread = threading.Thread(target=handle, args=(conn, addr))
        thread.start()
