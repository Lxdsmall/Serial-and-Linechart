import sys
import numpy
import matplotlib.pyplot
from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt
from PySide2 import QtWidgets, QtCore, QtGui

import Serial_Connect

serial_bps = ["1200", "2400", "4800", "9600", "19200", "38400", "57600", "115200"]
serial_date = ["5", "6", "7", "8"]
serial_check = ["偶校验", "奇校验", "高校验", "低校验", "无"]
serial_stop = ["1", "1.5", "2"]


class UiFrame(object):                                          # draw group box
    @staticmethod
    def setup_frame(frame):
        frame.setObjectName("frame")
        serial_group = QtWidgets.QGroupBox(frame)
        serial_group.setGeometry(QtCore.QRect(10, 5, 190, 245))
        serial_group.setObjectName("groupBox")
        serial_group.setTitle(QtWidgets.QApplication.translate("frame", "串口配置", None, -1))

        receive_group = QtWidgets.QGroupBox(frame)
        receive_group.setGeometry(QtCore.QRect(10, 255, 190, 170))
        receive_group.setObjectName("groupBox")
        receive_group.setTitle(QtWidgets.QApplication.translate("frame", "接收区设置", None, -1))

        group_box3 = QtWidgets.QGroupBox(frame)
        group_box3.setGeometry(QtCore.QRect(10, 430, 675, 130))
        group_box3.setObjectName("groupBox")
        group_box3.setTitle(QtWidgets.QApplication.translate("frame", "发送区设置", None, -1))

        QtCore.QMetaObject.connectSlotsByName(frame)


class GUIConfigSerial(QMainWindow, UiFrame):
    def __init__(self, parent=None):
        super(GUIConfigSerial, self).__init__(parent)
        self.setObjectName("GUIConfigSerial")
        self.resize(700, 570)
        self.setWindowTitle(r"串口助手定制版")
        self.setWindowIcon(QIcon("icon/Window_Icon.png"))
        # self.setWindowFlags(Qt.FramelessWindowHint)                           # 无边框
        # self.setWindowFlags(Qt.SubWindow)                                     # 有边框

        layout = QtWidgets.QGridLayout()

        UiFrame.setup_frame(self)                                               # 绘制GroupBox
        self.serial_widgets(layout)                                             # 串口配置
        self.receive_widgets(layout)                                            # 接收区配置
        self.send_widgets(layout)                                               # 发送区配置

        tabs = QTabWidget(self)                                                 # 两个Tab界面
        tabs.move(215, 10)
        tabs.resize(470, 410)
        self.date_re = QTextEdit()                                              # tab1是text edit
        self.line_set = QWidget()

        tabs.addTab(self.date_re, u"接收显示")
        tabs.addTab(self.line_set, u"图标设置")

        self.date_re.setText("123456\n")
        self.date_re.setText("234567\n")

        self.setStyleSheet("QGroupBox{color:green;}"                            # 设置全局stylesheet
                           "GUIConfigSerial{border-image:url(icon/background.jpg);}"              
                           "QLabel{color:red;font:16px;font-family:'宋体';font-weight:bold;}"
                           "QCheckBox{color:red;font:16px;font-family:'宋体';font-weight:bold;}"
                           "QTabBar:tab{width:100px;height:25px;font:16px '楷体';font-weight:bold;color:green;}")
        self.setLayout(layout)

    def serial_widgets(self, lay):
        global serial_combobox
        global baud_combobox
        global date_combobox
        global check_combobox
        global stop_combobox
        global open_btn

        serial_label = QtWidgets.QLabel(self)
        serial_label.setText("串口号:")
        serial_label.move(20, 25)
        lay.addWidget(serial_label)

        serial_combobox = QtWidgets.QComboBox(self)
        serial_combobox.setMaxVisibleItems(6)
        serial_combobox.resize(100, 28)
        serial_combobox.move(90, 25)
        connect = Serial_Connect.SerialInformation()
        free_com = connect.get_free_com()
        if len(free_com) > 5:
            serial_combobox.addItems(free_com)
        else:
            serial_combobox.addItem(free_com)
        # serial_combobox.currentIndexChanged.connect(lambda: self.string_sheet_event())
        lay.addWidget(serial_combobox)

        baud_label = QtWidgets.QLabel(self)
        baud_label.setText("波特率:")
        baud_label.move(20, 60)
        lay.addWidget(baud_label)

        baud_combobox = QtWidgets.QComboBox(self)
        baud_combobox.setMaxVisibleItems(6)
        baud_combobox.resize(100, 28)
        baud_combobox.move(90, 60)
        baud_combobox.addItems(serial_bps)
        baud_combobox.setCurrentText("9600")
        # baud_combobox.currentIndexChanged.connect(lambda: self.string_sheet_event())
        lay.addWidget(baud_combobox)

        date_label = QtWidgets.QLabel(self)
        date_label.setText("数据位:")
        date_label.move(20, 95)
        lay.addWidget(date_label)

        date_combobox = QtWidgets.QComboBox(self)
        date_combobox.setMaxVisibleItems(6)
        date_combobox.resize(100, 28)
        date_combobox.move(90, 95)
        date_combobox.addItems(serial_date)
        date_combobox.setCurrentText("8")
        # date_combobox.currentIndexChanged.connect(lambda: self.string_sheet_event())
        lay.addWidget(date_combobox)

        check_label = QtWidgets.QLabel(self)
        check_label.setText("校验位:")
        check_label.move(20, 130)
        lay.addWidget(check_label)

        check_combobox = QtWidgets.QComboBox(self)
        check_combobox.setMaxVisibleItems(6)
        check_combobox.resize(100, 28)
        check_combobox.move(90, 130)
        check_combobox.addItems(serial_check)
        check_combobox.setCurrentText("无")
        # check_combobox.currentIndexChanged.connect(lambda: self.string_sheet_event())
        lay.addWidget(check_combobox)

        stop_label = QtWidgets.QLabel(self)
        stop_label.setText("停止位:")
        stop_label.move(20, 165)
        lay.addWidget(stop_label)

        stop_combobox = QtWidgets.QComboBox(self)
        stop_combobox.setMaxVisibleItems(6)
        stop_combobox.resize(100, 28)
        stop_combobox.move(90, 165)
        stop_combobox.addItems(serial_stop)
        stop_combobox.setCurrentText("1")
        # stop_combobox.currentIndexChanged.connect(lambda: self.string_sheet_event())
        lay.addWidget(stop_combobox)

        open_btn = QtWidgets.QPushButton(self)
        open_btn.resize(170, 35)
        open_btn.setText("打开串口")
        open_btn.setStyleSheet("QPushButton{"  # normal statue style
                               "background-color:skyblue;"  # background(also use picture)
                               "border-style:outset;"  # border style(inset/outset)
                               "border-width:3px;"  # border width
                               "border-radius:8px;"  # border radius
                               "font-family:'楷体';"
                               "border-color:rgba(255,255,255,200);"  # border color
                               "font:bold 22px;"  # font & size
                               "color:rgba(0,0,0,200);"  # font color
                               "padding:3px;"  # padding
                               "}"
                               "QPushButton:pressed{"  # Mouse pressed style
                               "background-color:rgba(35,140,44,1);"
                               "border-color:rgba(255,255,255,30);"
                               "border-style:inset;"
                               "color:rgba(0,0,0,100);"
                               "}")
        open_btn.clicked.connect(lambda: self.open_btn_event())
        open_btn.move(20, 205)

    def receive_widgets(self, lay):
        global display_check
        global pause_check
        global save_check
        global save_line

        display_check = QtWidgets.QCheckBox(self)
        display_check.setText("十六进制显示")
        display_check.resize(160, 28)
        # display_check.stateChanged.connect(lambda: self.select_func(check_string.text()))
        display_check.move(20, 275)

        pause_check = QtWidgets.QCheckBox(self)
        pause_check.setText("暂停接收显示")
        pause_check.resize(160, 28)
        # pause_check.stateChanged.connect(lambda: self.select_func(check_string.text()))
        pause_check.move(20, 310)

        save_check = QtWidgets.QCheckBox(self)
        save_check.setText("保存到文件")
        save_check.resize(160, 28)
        # save_check.stateChanged.connect(lambda: self.select_func(check_string.text()))
        save_check.move(20, 345)

        save_line = QtWidgets.QLineEdit(self)
        save_line.resize(170, 25)
        save_line.move(20, 385)
        save_line.setPlaceholderText("Output folder")
        save_line.returnPressed.connect(lambda: self.public_export_event(save_line.text(), "returnPressed"))
        lay.addWidget(save_line)

        save_btn = QtWidgets.QPushButton(self)
        save_btn.setText('...')
        save_btn.setFixedSize(30, 23)
        save_btn.setStyleSheet("color:black;background:transparent;")
        # save_btn.clicked.connect(lambda: self.public_export_event(browse_btn.text(), "textChange"))
        save_line.setTextMargins(0, 0, save_btn.width(), 0)
        layout_1 = QHBoxLayout()
        layout_1.setContentsMargins(0, 0, 0, 0)
        layout_1.addWidget(save_btn, 0, Qt.AlignRight)
        save_line.setLayout(layout_1)
        layout_2 = QHBoxLayout()
        layout_2.addWidget(save_line)

    def send_widgets(self, lay):
        global style_check
        global alarm_check
        global send_check
        global send_line

        style_check = QtWidgets.QCheckBox(self)
        style_check.setText("十六进制发送")
        style_check.resize(160, 28)
        # style_check.stateChanged.connect(lambda: self.select_func(check_string.text()))
        style_check.move(20, 450)

        alarm_check = QtWidgets.QCheckBox(self)
        alarm_check.setText("定时发送")
        alarm_check.resize(160, 28)
        # alarm_check.stateChanged.connect(lambda: self.select_func(check_string.text()))
        alarm_check.move(20, 485)

        send_line = QtWidgets.QLineEdit(self)
        send_line.resize(130, 25)
        send_line.move(120, 485)
        send_line.setPlaceholderText("Enter time")
        send_line.returnPressed.connect(lambda: self.public_export_event(send_line.text(), "returnPressed"))
        lay.addWidget(send_line)

        time_label = QtWidgets.QLabel(self)
        time_label.setText("ms")
        time_label.move(260, 485)
        lay.addWidget(time_label)

        send_check = QtWidgets.QCheckBox(self)
        send_check.setText("发送文件")
        send_check.resize(160, 28)
        # file_check.stateChanged.connect(lambda: self.select_func(check_string.text()))
        send_check.move(20, 520)

        file_line = QtWidgets.QLineEdit(self)
        file_line.resize(170, 25)
        file_line.move(120, 520)
        file_line.setPlaceholderText("input file")
        file_line.returnPressed.connect(lambda: self.public_export_event(file_line.text(), "returnPressed"))
        lay.addWidget(file_line)

        file_btn = QtWidgets.QPushButton(self)
        file_btn.setText('...')
        file_btn.setFixedSize(30, 23)
        file_btn.setStyleSheet("color:black;background:transparent;")
        # send_btn.clicked.connect(lambda: self.public_export_event(browse_btn.text(), "textChange"))
        file_line.setTextMargins(0, 0, file_btn.width(), 0)
        layout_1 = QHBoxLayout()
        layout_1.setContentsMargins(0, 0, 0, 0)
        layout_1.addWidget(file_btn, 0, Qt.AlignRight)
        file_line.setLayout(layout_1)
        layout_2 = QHBoxLayout()
        layout_2.addWidget(file_line)

        send_line = QtWidgets.QPlainTextEdit(self)
        send_line.resize(370, 50)
        send_line.move(300, 450)
        send_line.setPlaceholderText("Enter date")
        # send_line.returnPressed.connect(lambda: self.public_export_event(send_line.text(), "returnPressed"))
        lay.addWidget(send_line)

        rxd_label = QtWidgets.QLabel(self)
        rxd_label.setText("接收:" + "1000")
        rxd_label.move(300, 500)
        lay.addWidget(rxd_label)

        txd_label = QtWidgets.QLabel(self)
        txd_label.setText("发送:" + "1000")
        txd_label.move(300, 525)
        lay.addWidget(txd_label)

        clear_label = QtWidgets.QLabel(self)
        clear_label.setText("清空计数")
        clear_label.move(400, 525)
        lay.addWidget(clear_label)

        send_btn = QtWidgets.QPushButton(self)
        send_btn.resize(150, 35)
        send_btn.setText("发送")
        # on_off_btn.setStyleSheet("QPushButton{"  # normal statue style
        #                            "background-color:skyblue;"  # background(also use picture)
        #                            "border-style:outset;"  # border style(inset/outset)
        #                            "border-width:3px;"  # border width
        #                            "border-radius:8px;"  # border radius
        #                            "border-color:rgba(255,255,255,200);"  # border color
        #                            "font:bold 14px;"  # font & size
        #                            "color:rgba(0,0,0,200);"  # font color
        #                            "padding:3px;"  # padding
        #                            "}"
        #                            "QPushButton:hover{"  # Mouse hover style
        #                            "background-color:deepskyblue;"
        #                            "border-color:rgba(255,255,255,200);"
        #                            "color:rgba(0,0,0,200);"
        #                            "}"
        #                            "QPushButton:pressed{"  # Mouse pressed style
        #                            "background-color:royalblue;"
        #                            "border-color:rgba(255,255,255,30);"
        #                            "border-style:inset;"
        #                            "color:rgba(0,0,0,100);"
        #                            "}")
        # on_off_btn.clicked.connect(lambda: self.public_gen_event())
        send_btn.move(520, 515)

    def open_btn_event(self):
        if open_btn.text() == "打开串口":
            open_btn.setText("关闭串口")
            open_btn.setStyleSheet("QPushButton{"  # normal statue style
                                   "background-color:rgba(35,140,44,1);"
                                   "border-color:rgba(255,255,255,30);"
                                   "border-width:3px;"  # border width
                                   "border-radius:8px;"  # border radius
                                   "border-color:rgba(255,255,255,200);"  # border color
                                   "font:bold 22px;"  # font & size
                                   "font-family:'楷体';"
                                   "padding:3px;"  # padding
                                   "}"
                                   "QPushButton:pressed{"  # Mouse pressed style
                                   "background-color:skyblue;"  # background(also use picture)
                                   "border-style:outset;"  # border style(inset/outset)
                                   "color:rgba(0,0,0,200);"  # font color
                                   "}")
        else:
            open_btn.setText("打开串口")
            open_btn.setStyleSheet("QPushButton{"  # normal statue style
                                   "background-color:skyblue;"  # background(also use picture)
                                   "border-style:outset;"  # border style(inset/outset)
                                   "border-width:3px;"  # border width
                                   "border-radius:8px;"  # border radius
                                   "border-color:rgba(255,255,255,200);"  # border color
                                   "font:bold 22px;"  # font & size
                                   "font-family:'楷体';"
                                   "color:rgba(0,0,0,200);"  # font color
                                   "padding:3px;"  # padding
                                   "}"
                                   "QPushButton:pressed{"  # Mouse pressed style
                                   "background-color:rgba(35,140,44,1);"
                                   "border-color:rgba(255,255,255,30);"
                                   "border-style:inset;"
                                   "color:rgba(0,0,0,100);"
                                   "}")

    def line_setting(self):
        lay = QGridLayout()

        name_label = QtWidgets.QLabel(self)
        name_label.setText("图表名称:")
        name_label.move(20, 60)
        lay.addWidget(name_label)

        x_label = QtWidgets.QLabel(self)
        x_label.setText("X轴名称:")
        x_label.move(20, 60)
        lay.addWidget(x_label)

        y_label = QtWidgets.QLabel(self)
        y_label.setText("Y轴名称:")
        y_label.move(20, 60)
        lay.addWidget(y_label)


        baud_combobox = QtWidgets.QComboBox(self)
        baud_combobox.setMaxVisibleItems(6)
        baud_combobox.resize(100, 28)
        baud_combobox.move(90, 60)
        baud_combobox.addItems(serial_bps)
        baud_combobox.setCurrentText("9600")
        # baud_combobox.currentIndexChanged.connect(lambda: self.string_sheet_event())
        lay.addWidget(baud_combobox)

        self.line_set.setLayout(lay)

    def line_display(self):                                                     # 折线图输出
        x = numpy.linspace(0, 2, 100)                                           # 设置X轴范围和点数

        matplotlib.pyplot.plot(x, x, label='linear')                            # 三个函数 label是函数名
        matplotlib.pyplot.plot(x, x ** 2, label='quadratic')
        matplotlib.pyplot.plot(x, x ** 3, label='cubic')

        matplotlib.pyplot.xlabel('x label')                                     # X轴名称
        matplotlib.pyplot.ylabel('y label')                                     # Y轴名称
        matplotlib.pyplot.title("Simple Plot")                                  # 图表名称

        matplotlib.pyplot.legend()

        matplotlib.pyplot.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = GUIConfigSerial()
    window.show()
    sys.exit(app.exec_())
