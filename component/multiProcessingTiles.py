# coding:utf-8
import sys
import os
import logging
import time
import gdal2tiles
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
from tiles import Ui_MainWindow
import multiprocessing as mp

class myMainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        # 初始化几个参数：输入文件，切片起始级别；输出文件夹和核心数
        self.inputFileName = ''
        self.startLevel = 1
        self.stopLevel = 1
        self.outFile = ''
        self.do_num_cores = 1
        self.num_cores = int(mp.cpu_count())# 计算总核心数

        super(Ui_MainWindow, self).__init__()
        self.cwd = os.getcwd()# 获取当前程序文件位置
        self.setupUi(self)
        self.button_input_select.clicked.connect(self.fileInputSelect)  # 打开文件按钮
        self.button_output_select.clicked.connect(self.fileOutputSelect) #选择保存的文件夹地址

        self.cores_label2.setText('本机核心数：' + str(self.num_cores))

        self.button_start.clicked.connect(self.tileStart)

    def fileInputSelect(self):
        file_path = QFileDialog.getOpenFileName(self,
                                                "选择影像文件",
                                                self.cwd,
                                                "影像文件 (*.png;*.tif;*.img;*.dat;*.pg2);;所有文件 (*)")
        self.entry_input_link.setPlainText(file_path[0])
        self.inputFileName = file_path[0]

    def fileOutputSelect(self):
        file_path = QFileDialog.getExistingDirectory(self,
                                    "选取文件夹",
                                    self.cwd)
        self.entry_output_link.setPlainText(file_path)
        self.outFile = file_path

    # 判断是否为数字符号
    def is_number(self,s):
        if s.count(".") == 1:  # 小数的判断
            if s[0] == "-":
                s = s[1:]
            if s[0] == ".":
                return False
            s = s.replace(".", "")
            for i in s:
                if i not in "0123456789":
                    return False
            else:  # 这个else与for对应的
                return True
        elif s.count(".") == 0:  # 整数的判断
            if s[0] == "-":
                s = s[1:]
            for i in s:
                if i not in "0123456789":
                    return False
            else:
                return True
        else:
            return False

    def btn_warn_cb(self,infomations):
        # ss = QMessageBox.information(self, "提示", infomations, QMessageBox.Yes)
        res = QMessageBox.warning(self, "警告", infomations, QMessageBox.Yes | QMessageBox.No)
        if (QMessageBox.Yes == res):
            print(infomations+"[warn] 点击Yes!")
            logging.info(infomations+'点击Yes')
        elif (QMessageBox.No == res):
            print(infomations+"[warn] 点击No!")
            logging.info(infomations+'点击No')

    def gdal_generate_tiles(self,input_file, output_dir, option):
        # 参数：
        # input_file （str）：输入文件的路径。
        # output_folder （str）：输出文件夹的路径。
        # options：图块生成选项。
        gdal2tiles.generate_tiles(input_file, output_dir, **option)

    def tileStart(self):
        if (self.inputFileName == ''):
            self.btn_warn_cb('请输入或选择影像文件')
            return
        if (self.outFile == ''):
            self.btn_warn_cb('请输入或选择切片存放文件夹')
            return
        if self.is_number(self.startValue.toPlainText()):
            if self.is_number(self.stopValue.toPlainText()):
                startLevel = int(self.startValue.toPlainText().strip())
                stopLevel = int(self.stopValue.toPlainText().strip())
                if (startLevel < 1 or stopLevel < 1):
                    self.btn_warn_cb('切片级别需要≥1')
                    return
                if (startLevel > stopLevel):
                    self.btn_warn_cb('切片结束级别≤开始级别')
                    return
                if(stopLevel > 32):
                    self.btn_warn_cb('切片最高级别为32级')
                    return

                logging.info('inputFileName：' + self.inputFileName)
                logging.info('outputFileName：' + self.outFile)
                logging.info('startLevel：' + self.startValue.toPlainText() + ',stopLevel：' + self.stopValue.toPlainText())
                logging.info('cores：' + self.coresValue.toPlainText())
                startTime = time.localtime(time.time())
                logging.info(time.strftime('%Y-%m-%d %H:%M:%S', startTime))
                # 判断核心数量
                coresGo = int(self.coresValue.toPlainText().strip())
                if (coresGo > self.num_cores):
                    self.btn_warn_cb('核心数大于系统核心数')
                    logging.info('coresGo>num_cores')
                    self.coresValue.setPlainText(1)
                else:
                    zoom = (startLevel, stopLevel)
                    # verbose和quiet参数都为False可以开启切图精度条
                    # verbose和quiet参数都为True可以开启详细
                    option = {
                        'zoom': zoom,
                        'resume': True,
                        'verbose': False,
                        'quiet':False,
                        'nb_processes': coresGo
                    }
                    # 此处在使用路径的时候不能有中文路径！
                    self.gdal_generate_tiles(self.inputFileName, self.outFile, option)
                    logging.info('Finish,and the time is:')
                    startTime = time.localtime(time.time())
                    logging.info(time.strftime('%Y-%m-%d %H:%M:%S', startTime))
            else:
                print('输入的切片结束级别不是数字类型')
                logging.info('输入的切片结束级别不是数字类型')
        else:
            print('输入的切片开始级别不是数字类型')
            logging.info('输入的切片开始级别不是数字类型')



if __name__ == '__main__':
    # 日志
    LOG_FILE_NAME = "./info.log"
    logging.basicConfig(filename=LOG_FILE_NAME, level=logging.INFO)
    logging.basicConfig(filename=LOG_FILE_NAME, level=logging.ERROR)
    logging.info('Start,and the time is :')
    startTime = time.localtime(time.time())
    logging.info(time.strftime('%Y-%m-%d %H:%M:%S', startTime))

    app = QApplication(sys.argv)
    vieo_gui = myMainWindow()
    vieo_gui.show()
    sys.exit(app.exec_())