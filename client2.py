import socket
import  json
import tkinter
from tkinter import *
from tkinter import messagebox
import tkinter.font as font
from PIL import Image, ImageTk
import threading

############# GUI FUNCTION #######################

class Window:
    def __init__(self, window_width, window_height, bkgColor, Title = "My window"):
        self.window = Tk()
        self.title = Title
        self.width = window_width
        self.height = window_height
        self.bkgColor = bkgColor
        self.window.title(Title)
        self.window.geometry(f"{self.width}x{self.height}")
        self.window.configure(bg =bkgColor)
        self.window.resizable(width=False, height= False)


class img:
    def __init__(self, left, top, imgName,  root, button_command =""):
        self.left = left
        self.top = top
        self.imgName = imgName
        self.photo = PhotoImage(file = imgName)
        if button_command == "":
            self.lbl = Label(root.window, image= self.photo, bg = root.bkgColor)
            self.lbl.image = self.photo
            self.lbl.place(x =left, y =top)
        else:
            self.btn = Button(root.window, image=self.photo, bg = root.bkgColor, bd = 0, command=button_command)
            self.btn.image = self.photo
            self.btn.place(x = left, y = top)

class textBox(img):
    def __init__(self, left, top, imgName, root, Show = ''):
        super().__init__(left, top, imgName, root)
        self.Box = Entry(root.window, bd = 0, bg = '#FFF3F3', show = Show)
        self.Box.place(x =self.left +20, y = self.top+15, width=self.photo.width()-30)
    def text(self):
        txt = self.Box.get()
        return txt
    def destroy(self):
        self.Box.destroy()
        self.lbl.destroy()
class button(img):
    def __init__(self, left, top, imgName, root, button_command):
        super().__init__(left, top, imgName, root, button_command)

############################ Button command ###################################   
def cannotConnect():
    global client
    if messagebox.askyesno("Retry connected?","Không thể kết nối đến Sever! Kết nối lại?"):
        try:
            client.close()
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(Addr)
            messagebox.showinfo("Conneted", f"Connected to Sever {Addr}")
        except:
            cannotConnect()
    else:
       pass
   

def getHostIP():
    global HOST, PORT, Addr,client
    HOST = BoxIP.text()
    Addr = (HOST, PORT)
    try:
        client.connect(Addr)
        getHost.window.destroy()
        print(f"Connected to {Addr}")
        signinAndSignUp()
    except:
        messagebox.showerror("Error", "Không thể kết nối đến Sever")

def signin_command():
    userName = textBoxUserName.text()
    password = textBoxPassWord.text()
    msg = "sign in"
    try:
        send_msg(client, msg)
        send_msg(client,userName)
        send_msg(client, password)
        response = get_msg_from_server()
        print(response)
        if response == "0":
            messagebox.showerror("Error", "Tên tài khoản không tồn tại")
        elif response == "1":
            messagebox.showerror("Error", "Sai mật khẩu")
        else:
            messagebox.showinfo("Information", "Đăng nhập thành công")
    except:
        cannotConnect()

def signup_command():
    userName = textBoxUserName.text()
    password = textBoxPassWord.text()
    checkpwd = textBoxcheckpwd.text()
    if checkpwd != password:
        messagebox.showerror("Error","Mật khẩu không khớp")
        checkpwd = textBoxcheckpwd.text()
    msg = "sign up"
    try:
        send_msg(client, msg)
        send_msg(client,userName)
        send_msg(client, password)
        response = get_msg_from_server()
        if response == "0":
            messagebox.showinfo("Infomation", "Đăng ký thành công!!");
        else:
            messagebox.showerror("Error", "Tên tài khoản đã tồn tại")
    except:
        cannotConnect()
#---------------------GET HOST WINDOW--------------------------
def getSeverIP():
    global BoxIP, getHost
    
    getHost = Window(350,200, '#383C5B', "Nhập IP Sever")
    myFont = font.Font(weight="bold", size = 12, family="tahoma")
    BoxIP = textBox(33, 56, 'textbox.png', getHost)
    lblIP = Label(getHost.window, text = "Sever IP : ", bg ="#383C5B", fg = "#FFFFFF", font = myFont)
    lblIP.place(x = 55, y = 26)
    btnOK = button(120, 130, 'OK.png', getHost, getHostIP)
    getHost.window.mainloop()
#-----------------------------LOGIN WINDOW-----------------------------
def signinAndSignUp():
    global windowLogin, myFont
    windowLogin = Window(850, 550, "#ABCDEF", "CẬP NHẬT SỐ CA NHIỄM COVID")
    myFont = font.Font(weight="bold", size = 12, family="tahoma")
    logo_bo_y_te = img(588, 45, 'logo_bo_y_te.png', windowLogin)
    #logo_bo_y_te
    bkgImg = img(-10,0 ,'bkgImg.png', windowLogin)
    #background image
    createSignIn()
    windowLogin.window.mainloop()
   
#--------------------------------------------------
def receive_msg(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT) 
    msg_length = int(msg_length)
    msg = conn.recv(msg_length).decode(FORMAT)
   # conn.send('OK'.encode(FORMAT))
    if msg == DISCONNECT_MESSAGE:
        messagebox.showinfo("DISCONNECTED", "Sever đã ngắt kết nối")
    return msg

def send_msg(conn, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)
   # t = conn.recv(1024).decode(FORMAT)

def back_to_sign_in():
    backToSignin.btn.destroy()
    signup.btn.destroy()
    lblcheckpwd.destroy()
    textBoxcheckpwd.destroy()
    createSignIn()

def signupInterface():
    global backToSignin, signup, lblcheckpwd, textBoxcheckpwd
    signin.btn.destroy()
    noAccount.destroy()
    textBoxcheckpwd = textBox(520, 400, 'textbox.png', windowLogin, '*')
    lblcheckpwd = Label(windowLogin.window, text="Nhập lại mật khẩu: ", bg = windowLogin.bkgColor, font=myFont)
    lblcheckpwd.place(x = 530, y = 375)
    signup = button(692, 475, 'singupButton.png', windowLogin, signup_command)
    backToSignin = button(520, 475, 'singinButton.png', windowLogin, back_to_sign_in)


def createSignIn():
    global textBoxUserName, textBoxPassWord, lblUserName, lblPassword, noAccount, signin
    textBoxUserName = textBox(520, 235, 'textbox.png', windowLogin )
    lblUserName = Label(windowLogin.window,text = "Tên Đăng Nhập: ", bg = windowLogin.bkgColor, font= myFont).place(x = 530, y = 210)
    textBoxPassWord = textBox(520, 315,  'textbox.png', windowLogin,'*')
    lblPassword = Label(windowLogin.window, text = "Mật khẩu: ", bg = windowLogin.bkgColor, font= myFont).place(x = 530, y = 290)
    #username and password
    noAccount = Button(windowLogin.window, bg = windowLogin.bkgColor, bd = 0, text="Chưa có tài khoản?", font =myFont, command= signupInterface)
    noAccount.place(x = 520, y =385)
    signin = button(607, 445, 'singinButton.png', windowLogin, signin_command)

def get_msg_from_server():
    global check_received, msg_from_sever
    msg = ''
    while check_received == False:
        pass
    msg = msg_from_sever
    check_received = False
    return msg

def receviveFromSever():
    global msg_from_sever, check_received
    check_received = False
    while True:
        if check_received == False:
            try:
                msg_from_sever = receive_msg(client)
                print("MSG:", msg_from_sever)
                if msg_from_sever != DISCONNECT_MESSAGE:
                    check_received = True
            except:
                check_received = False


HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "x"
PORT = 5050
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
thread_receive_msg = threading.Thread(target=receviveFromSever)
thread_receive_msg.setDaemon(True)
thread_receive_msg.start()
getSeverIP()



