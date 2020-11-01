import sqlite3
import threading
import requests
import time
import json
from tkinter import *
from tkinter import messagebox
from tkinter import ttk


class SMS:
    def __init__(self,number,text,token):
        self.number = number
        self.text = text
        self.token = token


    def send_sms(self):
        r = requests.get(f"https://semysms.net/api/3/sms.php?token={self.token}&device=active&phone=%2B{self.number}&msg={self.text}")
        print(r.json())


root = Tk()
# Отправка СМС
def send_to(token,msg):
    if var.get():
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        cur.execute("UPDATE info SET token = ? , checkbox = ? WHERE key = ?",(token,True,1))
        con.commit()
        cur.close()
        con.close()
    else:
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        cur.execute("UPDATE info SET token = ? , checkbox = ? WHERE key = ?",("none",False,1))
        con.commit()
        cur.close()
        con.close()

    with open("numbers.txt","r") as f:
        for phone in f:
            message = SMS(phone,msg,token)
            message.send_sms()


def create_task(token,msg):
    task = threading.Thread(target=send_to,name='Spam ',args=(token,msg))
    task.start()





var = BooleanVar()
con = sqlite3.connect('data.db')
cur = con.cursor()
cur.execute("SELECT * FROM info WHERE key = ?",(1,))
info = cur.fetchone()
cur.close()
con.close()
if info[0]:
    var.set(1)
else:
    var.set(0)

root.title("Рассылка смс")
root.geometry('360x180')
# Ключ
api = Label(root,text=f'Токен:', justify=LEFT,font = 25)
api.place(x=10, y=10)
api_field = Entry(root, width = 40)
api_field.grid(row=0, column=0, columnspan=5)
api_field.place(x=10,y=35)
if info[1] != 'none':
    api_field.insert(END,info[1])
# Текст сообщения
msg_field = Label(root,text=f'Текст сообщения:', justify=LEFT,font = 25)
msg_field.place(x=10, y=70)
msg_field = Entry(root, width = 40)
msg_field.grid(row=0, column=0, columnspan=5)
msg_field.place(x=10,y=95)
# Чекбокс
check = Checkbutton(root, text="Запомнить токен",
                 variable=var,
                 onvalue=1, offvalue=0)
check.place(x = 160, y = 35)
# Кнопка старат
button_start = Button(root,text='Начать', command = lambda:create_task(str(api_field.get()),str(msg_field.get())))
button_start.place(x=90,y=150)
root.mainloop()
