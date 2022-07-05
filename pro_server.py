from tkinter import *
from socket import *
import _thread
import time


def initialize_server():
    print("\nWelcome to Chat Room\n")
    print("Initialising....\n")
    time.sleep(1)
    
    s = socket(AF_INET, SOCK_STREAM)
    host =gethostbyname(gethostname())
    port = 1234
    s.bind((host, port))

    global name
    name = input(str("Enter your name: "))
    print("Your IP address Is:",host)
    s.listen(1)
    print("\nWaiting for Clients To join...\n")
    conn, addr = s.accept()
    print("Received connection from ", addr[0], "(", addr[1], ")\n")

    global s_name
    s_name = conn.recv(1024)
    s_name = s_name.decode()
    print(s_name, " has connected to the chat room")
    conn.send(name.encode())

    return conn


def update_chat(msg, state):
    chatlog.config(state=NORMAL)
    if state==0:
        chatlog.insert(END, 'Me: ' + msg)
    else:
        chatlog.insert(END, s_name+': ' + msg)
    chatlog.config(state=DISABLED)
    chatlog.yview(END)


def send():
    msg = textbox.get("0.0", END)
    update_chat(msg, 0)
    conn.send(msg.encode('ascii'))
    textbox.delete("0.0", END)

def receive():
    while 1:
        try:
            data = conn.recv(1024)
            msg = data.decode('ascii')
            if msg != "":
                update_chat(msg, 1)
        except:
            pass

def press(event):
    send()

# GUI function
def GUI():
    global chatlog
    global textbox
    gui = Tk()
    gui.title(name)
    gui.geometry("380x430")

    chatlog = Text(gui, bg='#C6CBDD')
    chatlog.config(state=DISABLED)
    
    sendbutton = Button(gui, bg='black', fg='white', text='SEND', command=send)
    textbox = Text(gui, bg='white')

    chatlog.place(x=6, y=6, height=386, width=370)
    textbox.place(x=6, y=401, height=20, width=265)
    sendbutton.place(x=300, y=401, height=20, width=50)
    
    textbox.bind("<KeyRelease-Return>", press)
    
    _thread.start_new_thread(receive, ())
    
    gui.mainloop()


if __name__ == '__main__': 
    conn = initialize_server()
    GUI()
