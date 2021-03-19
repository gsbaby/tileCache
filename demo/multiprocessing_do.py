# coding:utf-8
# 打包
# pyinstaller -F -i D:/gaosong/Work_Demo/修改服务配置信息/FunnyTool/GIS_Tools/tileCache/1.ico D:/gaosong/Work_Demo/修改服务配置信息/FunnyTool/GIS_Tools/tileCache/multiprocessing_do.py
import os
import logging
import datetime,time
import multiprocessing as mp
import gdal2tiles
import tkinter
import tkinter.messagebox
import tkinter.filedialog
from tkinter.filedialog import askdirectory

def gdal_generate_tiles(input_file, output_dir, option):
    # 参数：
    # input_file （str）：输入文件的路径。
    # output_folder （str）：输出文件夹的路径。
    # options：图块生成选项。
    gdal2tiles.generate_tiles(input_file, output_dir, **option)


def Start():
    inputFileName = entry_input_link.get()
    if(inputFileName==''):
        tkinter.messagebox.showwarning('提示', '请输入或选择影像文件')
        return
    outputFileName = entry_output_link.get()
    if(outputFileName==''):
        tkinter.messagebox.showwarning('提示', '请输入或选择切片存放文件夹')
        return
    startLevel = int(startValue.get().strip())
    stopLevel = int(stopValue.get().strip())
    if(startLevel<1 or stopLevel<1):
        tkinter.messagebox.showwarning('提示','切片级别需要≥1')
        return
    if(startLevel > stopLevel):
        tkinter.messagebox.showwarning('提示','切片结束级别≤开始级别')
        return
    coresGo = int(cores_go.get().strip())
    logging.info('inputFileName：'+inputFileName)
    logging.info('outputFileName：'+outputFileName)
    logging.info('startLevel：'+startValue.get()+',stopLevel：'+stopValue.get())
    logging.info('cores：'+cores_go.get())
    startTime = time.localtime(time.time())
    logging.info(time.strftime('%Y-%m-%d %H:%M:%S', startTime))
    zoom = (startLevel, stopLevel)
    if(coresGo > num_cores):
        logging.info('coresGo>num_cores')
        tkinter.messagebox.showwarning("提示", '核心数大于系统核心数')
        cores_go.set(1)
    else:
        option = {
            'zoom': zoom,
            'resume': True,
            'verbose': True,
            'nb_processes':coresGo
        }
        # 此处在使用路径的时候不能有中文路径！
        gdal_generate_tiles(inputFileName, outputFileName, option)
        logging.info('Finish,and the time is:')
        startTime = time.localtime(time.time())
        logging.info(time.strftime('%Y-%m-%d %H:%M:%S', startTime))

def fileInputSelect():
    file_path = tkinter.filedialog.askopenfilename(title=u'选择影像文件',
                                                   initialdir=(os.path.expanduser(default_dir)),
                                                   filetypes = [
                                                       ("Raster", "*.png;*.tif;*.img;*.dat;*.pg2"),("All","*")
                                                   ]
                                                   )
    input_text.set(file_path)

def fileOutputSelect():
    # file_path = tkinter.filedialog.asksaveasfilename(title=u'保存地址', initialdir=(os.path.expanduser(default_dir)))
    file_path = tkinter.filedialog.askdirectory(title=u'保存地址', initialdir=(os.path.expanduser(default_dir)))
    output_text.set(file_path)


if __name__ == '__main__':
    default_dir = r"I:/T"
    # 日志
    LOG_FILE_NAME = "./info.log"
    logging.basicConfig(filename=LOG_FILE_NAME, level=logging.INFO)
    logging.basicConfig(filename=LOG_FILE_NAME, level=logging.ERROR)
    logging.info('Start,and the time is :')
    startTime = time.localtime(time.time())
    logging.info(time.strftime('%Y-%m-%d %H:%M:%S', startTime))

    # 计算核心数
    num_cores = int(mp.cpu_count())

    root = tkinter.Tk()
    root.title("影像切片")
    root['width'] = 500
    root['height'] = 300

    input_text = tkinter.StringVar()
    input_text.set('')
    output_text = tkinter.StringVar()
    output_text.set('')
    start_value = tkinter.StringVar()
    start_value.set(1)
    stop_value = tkinter.StringVar()
    stop_value.set(10)
    cores_go = tkinter.StringVar()
    cores_go.set(1)

    lab_input_link = tkinter.Label(root, text='影像文件位置：')
    lab_input_link.place(x=20, y=10, width=100, height=20)
    entry_input_link = tkinter.Entry(root, textvariable=input_text)
    entry_input_link.place(x=130, y=10, width=300, height=20)
    button_input_select = tkinter.Button(root, text="...", command=fileInputSelect)
    button_input_select.place(x=440, y=10, width=20, height=20)


    lab_level = tkinter.Label(root, text='切片级别：')
    lab_level.place(x=20, y=40, width=100, height=20)
    startValue = tkinter.Entry(root, textvariable=start_value)
    startValue.place(x=130, y=40, width=30, height=20)
    guodu = tkinter.Label(root,text = '~')
    guodu.place(x=160,y=40,width=20,height=20)
    stopValue = tkinter.Entry(root,textvariable = stop_value)
    stopValue.place(x=190,y=40,width=30,height = 20)
    lllable = tkinter.Label(root,text='切片级别需要≥1，开始级别≤结束级别(最大32)')
    lllable.place(x=230,y=40,width=260,height=20)

    lab_output_link = tkinter.Label(root, text='输出切片位置：')
    lab_output_link.place(x=20, y=70, width=100, height=20)
    entry_output_link = tkinter.Entry(root, textvariable=output_text)
    entry_output_link.place(x=130, y=70, width=300, height=20)
    button_output_select = tkinter.Button(root, text="...", command=fileOutputSelect)
    button_output_select.place(x=440, y=70, width=20, height=20)

    coreslabel = '本机核心数：'+str(num_cores)
    cores_label = tkinter.Label(root, text='核心数')
    cores_label.place(x=20, y=100, width=100, height=20)
    cores_value = tkinter.Entry(root, textvariable=cores_go)
    cores_value.place(x=130, y=100, width=30, height=20)
    cores_label2 = tkinter.Label(root, text=coreslabel)
    cores_label2.place(x=150, y=100, width=100, height=20)

    button_start = tkinter.Button(root, text="开始切片", command=Start)
    button_start.place(x=140, y=150, width=200, height=40)

    # # 创建一个背景色为白色的矩形
    # canvas = canvas(root, width=170, height=26, bg="white")
    # # 创建一个矩形外边框（距离左边，距离顶部，矩形宽度，矩形高度），线型宽度，颜色
    # out_line = canvas.create_rectangle(2, 2, 180, 27, width=1, outline="black")
    # canvas.grid(row=0, column=1, ipadx=5)

    root.mainloop()