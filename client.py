# import all the required modules
import socket
import threading
import clientToServer as ctos
from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from time import sleep

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
        self.title("client Application")
        self.resizable(False, False)
        self.fun_login_frame()

    # Create and specify widgets in the application box
    def fun_login_frame(self, last_frame=None):
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
            command=lambda: self.fun_register_frame(last_frame=login_frame),
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
        else:
            messagebox.showerror("Error", f"Login failed")

    def fun_register_frame(self, last_frame=None):
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
            command=lambda: self.fun_login_frame(register_frame),
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
        if kwargs['password'] != kwargs['re_password']:
            messagebox.showerror("Error", "password != re_password")
            return

        self.client.send(ctos.register_message(username=kwargs['username'], password=kwargs['password']).encode(FORMAT))

        message = self.client.recv(1024).decode(FORMAT)

        if message.split(' -Option ')[0] == 'User Accepted':
            kwargs['last_frame'].destroy()
        else:
            messagebox.showerror("Error", f"Register failed")

    def fun_home_frame(self):
        home_frame = Frame(
            self,
            bd=2,
            bg='#CCCCCC',
            relief=SOLID,
            padx=10,
            pady=10
        )

        home_frame.pack()

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
