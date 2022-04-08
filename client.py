# import all the required modules
import socket
import clientToServer as ctos
import clientChatRoom
from tkinter import *
from tkinter import messagebox

##############################################
# Author : Sayed Ali Hosseini Nasab (SAHN)   #
# Developed : Python3 and Library tkinter    #
# Student ID : 9817503                       #
# Telegram Channel : @sahnTeach              #
##############################################

PORT = 50000
SERVER = "localhost"
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
FONT = ('Times', 14)


class Main(Tk):

    # Initialize to create object of class
    def __init__(self):
        # Specify the title and size of the program box and specify the properties of the widgets inside the program box
        super(Main, self).__init__()
        # Create a new client socket
        # and connect to the server
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDRESS)
        self.title("Client Application")
        self.resizable(False, False)
        self.login_frame()

    # Create and specify widgets in the application box
    def login_frame(self, last_frame=None):
        if last_frame is not None:
            last_frame.destroy()

        login_frame = Frame(
            self,
            bd=2,
            bg='#CCCCCC',
            relief=SOLID,
            padx=10,
            pady=10
        )
        Label(
            login_frame,
            text="Enter username",
            bg='#CCCCCC',
            font=FONT
        ).grid(row=0, column=0, sticky=W, pady=10)

        Label(
            login_frame,
            text="Enter password",
            bg='#CCCCCC',
            font=FONT
        ).grid(row=1, column=0, sticky=W, pady=10)

        username_entry = Entry(
            login_frame,
            font=FONT
        )
        password_entry = Entry(
            login_frame,
            font=FONT,
            show='*'
        )
        login_button = Button(
            login_frame,
            width=15,
            text='Login',
            font=FONT,
            relief=SOLID,
            cursor='hand2',
            command=lambda: self.login_server(last_frame=login_frame, username=username_entry.get(),
                                              password=password_entry.get()),
        )
        register_button = Button(
            login_frame,
            width=15,
            text='Register',
            font=FONT,
            relief=SOLID,
            cursor='hand2',
            command=lambda: self.register_frame(last_frame=login_frame),
        )

        username_entry.grid(row=0, column=1, pady=10, padx=20)
        password_entry.grid(row=1, column=1, pady=10, padx=20)
        register_button.grid(row=2, column=0, pady=10, padx=20)
        login_button.grid(row=2, column=1, pady=10, padx=20)
        login_frame.pack()

    def login_server(self, *args, **kwargs):
        for k, v in kwargs.items():
            if v == '':
                messagebox.showerror("Error", f"{k} can't be empty")
                return

        self.client.send(ctos.login_message(username=kwargs['username'], password=kwargs['password']).encode(FORMAT))

        message = self.client.recv(1024).decode(FORMAT)

        if message.split(' -Option ')[0] == 'Connected':
            kwargs['last_frame'].destroy()
            self.chat_room(kwargs['username'])
        else:
            messagebox.showerror("Error", f"Login failed")

    def register_frame(self, last_frame=None):
        if last_frame is not None:
            last_frame.destroy()

        register_frame = Frame(
            self,
            bd=2,
            bg='#CCCCCC',
            relief=SOLID,
            padx=10,
            pady=10
        )

        Label(
            register_frame,
            text="Enter username",
            bg='#CCCCCC',
            font=FONT
        ).grid(row=0, column=0, sticky=W, pady=10)

        Label(
            register_frame,
            text="Enter password",
            bg='#CCCCCC',
            font=FONT
        ).grid(row=1, column=0, sticky=W, pady=10)

        Label(
            register_frame,
            text="Re-Enter password",
            bg='#CCCCCC',
            font=FONT
        ).grid(row=2, column=0, sticky=W, pady=10)

        username_entry = Entry(
            register_frame,
            font=FONT
        )

        password_entry = Entry(
            register_frame,
            font=FONT,
            show='*'
        )
        password_again_entry = Entry(
            register_frame,
            font=FONT,
            show='*'
        )

        login_button = Button(
            register_frame,
            width=15,
            text='Login',
            font=FONT,
            relief=SOLID,
            cursor='hand2',
            command=lambda: self.login_frame(register_frame),
        )

        register_button = Button(
            register_frame,
            width=15,
            text='Register',
            font=FONT,
            relief=SOLID,
            cursor='hand2',
            command=lambda: self.register_server(last_frame=register_frame, username=username_entry.get(),
                                                 password=password_entry.get(), re_password=password_again_entry.get())
        )

        username_entry.grid(row=0, column=1, pady=10, padx=20)
        password_entry.grid(row=1, column=1, pady=10, padx=20)
        password_again_entry.grid(row=2, column=1, pady=10, padx=20)
        login_button.grid(row=3, column=0, pady=10, padx=20)
        register_button.grid(row=3, column=1, pady=10, padx=20)
        register_frame.pack()

    def register_server(self, *args, **kwargs):
        for k, v in kwargs.items():
            if v == '':
                messagebox.showerror("Error", f"{k} can't be empty")
                return
        if len(kwargs['username']) < 6:
            messagebox.showerror("Error", "User name must be at least 6 characters long")
            return
        elif len(kwargs['password']) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long")
            return
        elif kwargs['password'] != kwargs['re_password']:
            messagebox.showerror("Error", "password != re_password")
            return

        self.client.send(ctos.register_message(username=kwargs['username'], password=kwargs['password']).encode(FORMAT))

        message = self.client.recv(1024).decode(FORMAT)

        if message.split(' -Option ')[0] == 'User Accepted':
            kwargs['last_frame'].destroy()
            self.chat_room(kwargs['username'])
        else:
            messagebox.showerror("Error", f"Register failed")

    def chat_room(self, name):
        def action_user_chat_button():
            if user_chat_button['text'] == "Send to user off":
                user_chat_button['text'] = "Send to user on"
            else:
                user_chat_button['text'] = "Send to user off"

            chat_room.send_pv_message(user_chat_entry.get())

        def action_exit_chatroom_button():
            self.client.send(ctos.exit_chatroom_message(name).encode(FORMAT))
            chat_room.window.destroy()
            del chat_room
            self.login_frame()

        chat_room = clientChatRoom.ChatRoom(Tk(), name, self.client)

        home_frame = Frame(
            self,
            bd=2,
            bg='#CCCCCC',
            relief=SOLID,
            padx=10,
            pady=10
        )
        head_label = Label(home_frame,
                           bg="#17202A",
                           fg="#EAECEE",
                           text=f"Welcome {name}",
                           font=FONT,
                           )

        user_chat_entry = Entry(
            home_frame,
            font=FONT,
        )
        user_chat_button = Button(
            home_frame,
            width=15,
            text='Send to user off',
            font=FONT,
            relief=SOLID,
            cursor='hand2',
            command=action_user_chat_button,
        )

        exit_chatroom_button = Button(
            home_frame,
            width=15,
            text='Exit chatroom',
            font=FONT,
            relief=SOLID,
            cursor='hand2',
            command=action_exit_chatroom_button,
        )

        list_users_button = Button(
            home_frame,
            width=15,
            text='List users',
            font=FONT,
            relief=SOLID,
            cursor='hand2',
            command=lambda: self.client.send(ctos.list_users_message(name).encode(FORMAT)),
        )

        head_label.grid(row=0, column=1, sticky=EW)
        user_chat_entry.grid(row=1, column=0, pady=10, padx=20)
        user_chat_button.grid(row=1, column=2, pady=10, padx=20)
        exit_chatroom_button.grid(row=2, column=0, pady=10, padx=20)
        list_users_button.grid(row=2, column=2, pady=10, padx=20)
        home_frame.pack()

        chat_room.window.mainloop()

    def destroy(self):
        super(Main, self).destroy()
        self.client.close()


if __name__ == '__main__':
    # Create object from class
    root = Main()


    # Put a graphical box in the run cycle
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()


    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
