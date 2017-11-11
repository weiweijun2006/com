import sys
import serial
import threading
import binascii
from PyQt5 import QtCore, QtGui, QtWidgets
import serial.tools.list_ports
from com_ui import Ui_mainWindow
import chardet
import time
class MyWindow(QtWidgets.QMainWindow,Ui_mainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.ser = serial.Serial()
        self.pushButton_5.clicked.connect(self.send_data)
        self.pushButton_4.clicked.connect(self.clean_data)
        self.pushButton_3.clicked.connect(self.port_cheak)
        self.pushButton_2.clicked.connect(self.port_close)
        self.pushButton.clicked.connect(self.port_open)


    def getCoding(self,strInput):
        #print(strInput)
        data=chardet.detect(strInput)
        if(data['encoding']=='ascii'):
         return 'ascii'
        elif(data['encoding']=='GB2312' ):
         return 'gb2312'
        elif ( data['encoding']=='ISO-8859-1'):
         return 'gbk'



    def port_open(self):
     try:
        self.ser.port = self.comboBox_4.currentText()
        self.ser.baudrate = 115200
        self.ser.bytesize = 8
        self.ser.stopbits = 1
        self.ser.parity = 'N'
        self.ser.open()
        if (self.ser.isOpen()):
            self.pushButton.setEnabled(False)
            self.label_12.setText("打开成功")
            self.t1 = threading.Thread(target=self.receive_data)
            self.t1.setDaemon(True)
            self.t1.start()
        else:
            self.label_12.setText("打开失败")
     except BaseException as e:
        print(e)



    def port_close(self):
        self.ser.close()
        if (self.ser.isOpen()):
            self.label_12.setText("关闭失败")
        else:
            self.pushButton.setEnabled(True)
            self.label_12.setText("关闭成功")


    def send_data(self):
        try:
         if (self.ser.isOpen()):
            if (self.checkBox_2.isChecked()):
                self.ser.write(binascii.a2b_hex(self.textEdit.toPlainText()))
            else:
                self.ser.write(self.textEdit.toPlainText().encode('utf-8'))
            self.label_12.setText("发送成功")
            #       self.ser.flushOutput()
         else:
            self.label_12.setText("发送失败")
        except BaseException as e:
         print(e)



    def receive_data(self):
        print("The receive_data threading is start")
        res_data = ''
        num = 0
        while (self.ser.isOpen()):
            size = self.ser.inWaiting()
            if size:
                res_data = self.ser.read_all()

                print(self.getCoding(res_data))
                if (self.checkBox.isChecked()):
                    self.textBrowser.append(binascii.b2a_hex(res_data).decode())
                else:
                    if self.getCoding(res_data)=='ascii':
                        self.textBrowser.append(res_data.decode())
                    elif self.getCoding(res_data)=='gb2312':
                         self.textBrowser.append(res_data.decode(encoding='gb2312',errors='ignore'))
                    elif self.getCoding(res_data)=='gbk':
                        self.textBrowser.append(res_data.decode(encoding='gbk',errors='ignore'))


                self.textBrowser.moveCursor(QtGui.QTextCursor.End)
                self.ser.flushInput()
                num += 1
                self.label_12.setText("接收：" + str(num))
                time.sleep(0.2)


    def clean_data(self):
        self.textBrowser.setText("")
        self.label_12.setText("接收清空")


    def port_cheak(self):
        print(1)
        Com_List = []
        port_list = list(serial.tools.list_ports.comports())
        self.comboBox_4.clear()
        for port in port_list:
            Com_List.append(port[0])
            self.comboBox_4.addItem(port[0])
        if (len(Com_List) == 0):
            self.label_12.setText("没串口")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myshow=MyWindow()
    myshow.show()
    sys.exit(app.exec_())
