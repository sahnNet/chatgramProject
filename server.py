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


def send_to_all(from_user, message):
    for client in clients.values():
        client.send(stoc.gm_message(from_user, message).encode(FORMAT))
    print(Fore.LIGHTYELLOW_EX + f"{stoc.gm_message(from_user, message)}")


def send_to_person(from_user, to_user, message):
    for username, client in clients.items():
        if username == to_user:
            client.send(stoc.pm_message(from_user, to_user, message).encode(FORMAT))
            break
    print(
        Fore.WHITE + f"{stoc.pm_message(from_user, to_user, message)}")


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
    send_to_all('Server', f"{items['user']} join the chat room.")
    send_to_all('Server', f"Hi {items['user']}, welcome to the chat room.")


def gm(body):
    items = body_to_dict(body)
    send_to_all(items['from'], items['message_body'])


def pm(body):
    items = body_to_dict(body)
    send_to_person(items['from'], items['to'], items['message_body'])
    send_to_person(items['from'], items['from'], items['message_body'])


def get_users(body):
    items = body_to_dict(body)
    result = ""
    counter = len(clients.keys())
    for user_name in clients.keys():
        counter -= 1
        if user_name == items['user']:
            continue
        result += f"<{user_name}>"
        if counter > 1:
            result += "|"
    return stoc.list_users_message(result)


def exit_chatroom(body):
    items = body_to_dict(body)
    clients.pop(items['user'])
    send_to_all('Server', f"{items['user']} left the chat room.")


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
        elif command == 'GM':
            gm(body=body)
        elif command == 'PM':
            pm(body=body)
        elif command == 'Users':
            result = get_users(body=body)
        elif command == 'End':
            exit_chatroom(body=body)
            # close the connection
            conn.close()
        else:
            flag = False

        if flag:
            print(Fore.LIGHTCYAN_EX + f"{message}")
            if result != '':
                conn.send(result.encode(FORMAT))
                print(Fore.BLUE + f"{result}")


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
