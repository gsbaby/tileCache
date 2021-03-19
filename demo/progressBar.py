import tkinter
from tkinter import *
from tkinter.ttk import *
import time
scale = 100
def running():                   # 开始Progressbar动画
    btn.configure(text="系统忙碌中...",state=DISABLED)
    print("\n"*2)
    print("执行开始".center(scale+28,'-'))
    start = time.perf_counter()
    for i in range(scale+1):
        pb["value"] = i      # 每次更新1
        root.update()            # 更新画面
        a = '*' * i
        b = '.' * (scale - i)
        c = (i/scale)*100
        input_text.set(str(c)+"%")
        t = time.perf_counter() - start
        print("\r任务进度:{:>3.0f}% [{}->{}]消耗时间:{:.2f}s".format(c,a,b,t),end="")
        time.sleep(0.03)
    print("\n"+"执行结束".center(scale+28,'-'))
    btn.configure(text="重启任务",state=NORMAL)

root = Tk()
root.geometry("300x100+600+300")
root.title("任务进度可视化")

# 使用默认设置创建进度条
pb = Progressbar(root,length=200,mode="determinate",orient=HORIZONTAL)
pb.place(x=20, y=20, width=200, height=20)
pb["maximum"] = 100
pb["value"] = 0

input_text = StringVar()
input_text.set('')

cores_label2 = Label(root, textvariable=input_text)
cores_label2.place(x=240, y=20, width=50, height=20)


btn = Button(root,text="启动任务",command=running)
btn.place(x=50, y=50, width=100, height=30)

root.mainloop()