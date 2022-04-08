# import all the required modules
import threading
import clientToServer as ctos
from tkinter import *

FORMAT = "utf-8"


def body_to_dict(body):
    items = {}
    for b in body:
        k, v = b.split(':')
        k = k.split('<')[-1]
        v = v.split('>')[0]
        items[k] = v
    return items


# GUI class for the chat
class ChatRoom:
    # constructor method
    def __init__(self, window, name, client):
        super().__init__()

        self.flag_pv_user = False
        self.window = window
        self.name = name
        self.client = client

        self.layout()
        self.client.send(ctos.group_message(self.name).encode(FORMAT))
        # the thread to receive messages
        rcv = threading.Thread(target=self.receive)
        rcv.start()

    # The main layout of the chat
    def layout(self):
        # to show chat window
        self.window.deiconify()
        self.window.title("CHATROOM")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=470, height=550, bg="#17202A")
        self.head_label = Label(self.window,
                                bg="#17202A",
                                fg="#EAECEE",
                                text=self.name,
                                font="Helvetica 13 bold",
                                pady=5)

        self.head_label.place(relwidth=1)
        self.line = Label(self.window,
                          width=450,
                          bg="#ABB2B9")

        self.line.place(relwidth=1,
                        rely=0.07,
                        relheight=0.012)

        self.cons_text = Text(self.window,
                              width=20,
                              height=2,
                              bg="#17202A",
                              fg="#EAECEE",
                              font="Helvetica 14",
                              padx=5,
                              pady=5)

        self.cons_text.place(relheight=0.745,
                             relwidth=1,
                             rely=0.08)

        self.bottom_label = Label(self.window,
                                  bg="#ABB2B9",
                                  height=80)

        self.bottom_label.place(relwidth=1,
                                rely=0.825)

        self.message_entry = Entry(self.bottom_label,
                                   bg="#2C3E50",
                                   fg="#EAECEE",
                                   font="Helvetica 13")

        # place the given widget
        # into the gui window
        self.message_entry.place(relwidth=0.74,
                                 relheight=0.06,
                                 rely=0.008,
                                 relx=0.011)

        self.message_entry.focus()

        # create a Send Button
        self.message_button = Button(self.bottom_label,
                                     text="Send",
                                     font="Helvetica 10 bold",
                                     width=20,
                                     bg="#ABB2B9",
                                     command=lambda: self.send_button(self.message_entry.get()))

        self.message_button.place(relx=0.77,
                                  rely=0.008,
                                  relheight=0.06,
                                  relwidth=0.22)

        self.cons_text.config(cursor="arrow")

        # create a scroll bar
        scrollbar = Scrollbar(self.cons_text)

        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight=1,
                        relx=0.974)

        scrollbar.config(command=self.cons_text.yview)

        self.cons_text.config(state=DISABLED)

    # function to basically start the thread for sending messages
    def send_button(self, msg):
        self.cons_text.config(state=DISABLED)
        self.msg = msg
        self.message_entry.delete(0, END)
        snd = threading.Thread(target=self.send_message)
        snd.start()

    # function to receive messages
    def receive(self):
        while True:
            message = self.client.recv(1024).decode(FORMAT)
            body = message.split(' -Option ')
            command = body.pop(0)

            # if the messages from the server is NAME send the self.client's name
            if command == 'GM' or command == 'PM':
                items = body_to_dict(body)
                # insert messages to text box
                self.cons_text.config(state=NORMAL)
                self.cons_text.insert(END, f"{items['from']}: {items['message_body']}" + "\n\n")

                self.cons_text.config(state=DISABLED)
                self.cons_text.see(END)
            elif command == 'USERS':
                # insert messages to text box
                self.cons_text.config(state=NORMAL)
                self.cons_text.insert(END, f"{body[0]}" + "\n\n")

                self.cons_text.config(state=DISABLED)
                self.cons_text.see(END)

    # function to send messages
    def send_message(self):
        self.cons_text.config(state=DISABLED)
        if self.flag_pv_user:
            self.client.send(ctos.pm_message(self.name, self.pv_user, self.msg).encode(FORMAT))
        else:
            self.client.send(ctos.gm_message(self.name, self.msg).encode(FORMAT))

    def send_pv_message(self, user):
        self.pv_user = user
        self.flag_pv_user = not self.flag_pv_user
