# -*- conding: utf-8 -*-
from tkinter import *
import tkinter.messagebox
from socket import *
from threading import Thread,Lock
import sys,re


Port_is_open = ""

class Port_Scan():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name

    #设置窗口
    def set_init_window(self):
        #设置名称
        self.init_window_name.title('简单的端口扫描工具')
        #设置窗体大小
        self.init_window_name.geometry('300x600+150+150')
        #设置图标
        self.init_window_name.iconbitmap('./panda_128px_1227690_easyicon.net.ico')
        #设置窗体背景颜色
        # self.init_window_name["background"] = "blue"
        #设置透明度
        # self.init_window_name.attributes("-alpha",0.8)
        #设置全全屏：True全屏，Flase正常显示（一般不设置）
        # self.init_window_name.attributes("-fullscreen",False)
        # 设置窗体置顶
        # self.init_window_name.attributes("-topmost",True)
        # 设置成脱离工具栏(一般不设置)
        # self.init_window_name.overrideredirect(False)


        # 获取屏幕的大小
        # screen_height = self.init_window_name.winfo_screenheight()
        # screen_width = self.init_window_name.winfo_screenwidth()
        # print("宽%d,高%d"%(screen_width,screen_height))

        # 获取窗体大小
        # win_height = self.init_window_name.winfo_height()
        # win_width = self.init_window_name.winfo_width()
        # print("宽%d,高%d" % (win_width, win_height))

        #获取窗体的位置
        # win_x = self.init_window_name.winfo_x()
        # win_y = self.init_window_name.winfo_y()
        # print("%d,%d" % (win_x, win_y))

        # 设置输入框 Entry
        label = Label(self.init_window_name,text ="IP:",anchor='c').grid(row=0)
        self.IP = Entry(self.init_window_name)
        self.IP.grid(row=0,column=1)

        #设置扫描按钮
        Button(self.init_window_name,text="开始扫描",anchor='c',command=self.Judgment_IP).grid(row=0,column=2)

    def Judgment_IP(self):
        # 判断输入的IP格式是否正确（正则）
        reg = '^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
        ip = re.match(reg,self.IP.get())
        if ip is not None:
            action(ip.group())
            Port_open_content = Label(self.init_window_name, text=Port_is_open)
            Port_open_content.grid(row=4,column=1)
        else:
            print("IP格式错误")
            tkinter.messagebox.showerror('错误', 'IP格式错误')


class mythread(Thread):
    def __init__(self, fun, args):
        Thread.__init__(self)
        self.fun = fun
        self.args = args

    def run(self):
        self.fun(*self.args)

def action(ip):
    def scan(h, p):
        global Port_is_open
        try:
            tcpCliSock = socket(AF_INET, SOCK_STREAM)
            tcpCliSock.connect((host, p))
            if lock.acquire():
                Port_is_open += ""+ str(p) + " -> opened\n"
                lock.release()
        except error:
            if lock.acquire():
                Port_is_open +=""+ str(p) + " -> not open\n"
                lock.release()
        finally:
            tcpCliSock.close()
            del tcpCliSock

    lock = Lock()
    ports = [21, 23, 25, 53, 69, 80, 135, 137, 139, 1521, 1433, 3306, 3389]
    host = ip
    mt = []
    for p in ports:
        t = mythread(scan,(host, p))
        mt.append(t)
    for m in mt:
        m.start()
    for m in mt:
        m.join()

    print(Port_is_open)

if __name__ == '__main__':
    init_window = Tk()
    scan = Port_Scan(init_window)
    scan.set_init_window()
    init_window.mainloop()