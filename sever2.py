import socket
import threading
import json
import tkinter
from tkinter import *
from tkinter import messagebox
import tkinter.font as font
from PIL import Image, ImageTk

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050
HEADER = 64
FORMAT = "utf-8"
bkg = "#F9A8A8"
DISCONNECT_MESSAGE = "x"
Addr = (HOST, PORT)
with open('account.json') as f:
    data = json.load(f)

sever = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sever.bind(Addr)

def disconnectClient():
    if messagebox.askyesno("Warning!!","Tất cả các client sẽ ngắt kết nối. Bạn có chắc chắn?"):
        global clients
        while len(clients) > 0:
            send_msg(clients[0][0],DISCONNECT_MESSAGE)
            insertText(f"{clients[0][1]} Đã ngắt kết nối!!",mainText)
            clients[0][0].close()
            clients.pop(0)
        updateActiveAccount()
        return True
    else:
        return False
    

def close_window():
    global run
    if disconnectClient() :
        run = False
        window.destroy()
        sever.close()

def GUI():
    global window, Width, Height, run
    run = True
    window = Tk()
    window.protocol("WM_DELETE_WINDOW", close_window)
    title = "ADMIN"
    Width = 650
    Height = 470
    bkgColor = bkg
    window.title(title)
    window.geometry(f"{Width}x{Height}")
    window.configure(bg =bkgColor)
    window.resizable(width=False, height= False)


def receive_msg(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT) 
    msg_length = int(msg_length)
    msg = conn.recv(msg_length).decode(FORMAT)
  #  conn.send("OK".encode(FORMAT))
    return msg


def send_msg(conn, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)
   # t = conn.recv(1024).decode(FORMAT)

def check_account(username, pwd):
    # return 0: There is no account with that username
    # return 1 : Wrong password
    # return 2: login successful
    for account in data['accounts']:
        if username == account['name'] and pwd == account['pwd'] : return "2";
        elif username == account['name'] and pwd != account['pwd']: return "1";
    return "0"

def signin(connection): 
    name = receive_msg(connection)
    password = receive_msg(connection)
    check = check_account(name, password)
    send_msg(connection, check)
    print(check)

def updateAccount(username, pwd):
    data['accounts'].append({"name": username, "pwd": pwd})
    with open('account.json', 'w') as fo:
        json.dump(data, fo, indent = 2)

def signup(connection):
        name = receive_msg(connection)
        password = receive_msg(connection)
        check = check_account(name, password)
        if check =="0" :
            updateAccount(name, password);
            send_msg(connection, check)
            print(check)
        else:
            send_msg(connection, check)

def hadle_client(conn, addr):
    clients.append((conn,addr))
    updateActiveAccount()
    s = f"[NEW CONNECTION]: {addr} đã kết nối!"
    insertText(s, mainText)
    connected = True
    while connected:
        try:
            msg = receive_msg(conn)
            print(msg)
            if msg == "sign in" : signin(conn)
            elif msg == "sign up": signup(conn)
            elif msg == DISCONNECT_MESSAGE:
                connected = False
        except:
            connected = False
    try:
        conn.close()
        clients.remove((conn,addr))
        s = f"{addr} Đã ngắt kết nối!!"
        insertText(s, mainText)
        updateActiveAccount()
    except:
        pass #disconnect by server, conn has already closed
     
       

def listenClient():
    sever.listen()
    while run:
        try:
            conn, addr = sever.accept()
            handleCLientThread = threading.Thread(target=hadle_client, args=(conn,addr))
            handleCLientThread.start()
        except:
            pass
    

def insertText(s, text):
    if run == False: return
    text.config(state=NORMAL)
    s+= "\n"
    text.insert(END,s)
    text.config(state=DISABLED)

def updateActiveAccount():
    if run == False: return
    global textCountActive, clients
    textCountActive.config(state=NORMAL)
    textCountActive.delete("1.0", "end")
    textCountActive.config(state=DISABLED)
    strCountActive = f"[Số users đang online]: {len(clients)}"
    insertText(strCountActive,textCountActive)

def createGUI():
    global textCountActive, mainText, run
    run = True
    GUI()
    frame = Frame(window, bg=bkg, width = Width, height=50)
    frame.pack()
    frame.pack_propagate(0)
    textCountActive = Text(frame)
    textCountActive.pack(padx=25, pady=10)
    updateActiveAccount()

    mainText = Text(window)
    s = f"[LISTENING]: Server đang lắng nghe với địa chỉ {Addr}"
    mainText.pack( padx=25)
    insertText(s, mainText)

    QuitButton = Button(window, text="Ngắt kết nối tất cả client", bg="red", fg="white", command=disconnectClient)
    QuitButton.pack()


clients = []
createGUI()
threadListenClient = threading.Thread(target=listenClient)
threadListenClient.start()
window.mainloop()

