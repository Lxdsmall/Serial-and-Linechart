import os
import numpy
import matplotlib.pyplot
from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt
from PySide2 import QtWidgets, QtCore
import Serial_Function

default_path = "D:/"


class UiFrame(object):                                                          # draw group box
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
    def __init__(self, flag_serial):
        super(GUIConfigSerial, self).__init__()
        self.setObjectName("GUIConfigSerial")
        self.resize(700, 570)
        self.setWindowTitle(r"串口助手定制版")
        self.setWindowIcon(QIcon("icon/Window_Icon.png"))
        # self.setWindowFlags(Qt.FramelessWindowHint)                           # 无边框
        # self.setWindowFlags(Qt.SubWindow)                                     # 有边框

        layout = QtWidgets.QGridLayout()

        UiFrame.setup_frame(self)                                               # 绘制GroupBox
        self.serial_widgets(layout, flag_serial)                                # 串口配置
        self.receive_widgets(layout)                                            # 接收区配置
        self.send_widgets(layout)                                               # 发送区配置

        tabs = QTabWidget(self)                                                 # 两个Tab界面
        tabs.move(215, 10)
        tabs.resize(470, 410)
        # tabs.setStyleSheet("background:green;")
        self.date_re = QTextEdit()                                              # tab1是text edit
        self.line_set = QWidget()
        self.line_setting()

        tabs.addTab(self.date_re, u"接收显示")
        tabs.addTab(self.line_set, u"图标设置")

        self.setStyleSheet("QGroupBox{color:green;}"                            # 设置全局stylesheet
                           "GUIConfigSerial{border-image:url(icon/background.jpg);}"              
                           "QLabel{color:red;font:16px;font-family:'宋体';font-weight:bold;}"
                           "QCheckBox{color:red;font:16px;font-family:'宋体';font-weight:bold;}"
                           "QTabBar:tab{width:100px;height:25px;font:16px '楷体';font-weight:bold;color:green;}")
        self.setLayout(layout)

    def serial_widgets(self, lay, _flag_serial):
        global serial_combobox
        global baud_combobox
        global date_combobox
        global check_combobox
        global stop_combobox
        global open_btn
        global _serial

        serial_label = QtWidgets.QLabel(self)
        serial_label.setText("串口号:")
        serial_label.move(20, 25)
        lay.addWidget(serial_label)

        serial_combobox = QtWidgets.QComboBox(self)
        serial_combobox.setMaxVisibleItems(6)
        serial_combobox.resize(100, 28)
        serial_combobox.move(90, 25)

        _serial = Serial_Function.SerialFunction()
        free_coms = _serial.get_free_com()
        _len = len(free_coms[0])
        for free_com in free_coms:
            serial_combobox.addItem(free_com)
            if _len >= len(free_com):
                pass
            else:
                _len = len(free_com)

        serial_combobox.view().setFixedWidth(_len * 0.75 * 9 + 10)              # Comobox下拉列表长度自适应
        lay.addWidget(serial_combobox)

        baud_label = QtWidgets.QLabel(self)
        baud_label.setText("波特率:")
        baud_label.move(20, 60)
        lay.addWidget(baud_label)

        baud_combobox = QtWidgets.QComboBox(self)
        baud_combobox.setMaxVisibleItems(6)
        baud_combobox.resize(100, 28)
        baud_combobox.move(90, 60)
        baud_combobox.addItems(Serial_Function.serial_bps)
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
        date_combobox.addItems(Serial_Function.serial_date)
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
        check_combobox.addItems(list(Serial_Function.serial_check.keys()))
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
        stop_combobox.addItems(Serial_Function.serial_stop)
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
        open_btn.clicked.connect(lambda: open_btn_event(open_btn.text(), _flag_serial))
        open_btn.move(20, 205)

    def receive_widgets(self, lay):
        global display_check
        global pause_check
        global save_check
        global save_line
        global save_btn

        display_check = QtWidgets.QCheckBox(self)
        display_check.setText("十六进制显示")
        display_check.resize(160, 28)
        display_check.stateChanged.connect(lambda: self.check_box_event(display_check.text()))
        display_check.move(20, 275)

        pause_check = QtWidgets.QCheckBox(self)
        pause_check.setText("暂停接收显示")
        pause_check.resize(160, 28)
        pause_check.stateChanged.connect(lambda: self.check_box_event(pause_check.text()))
        pause_check.move(20, 310)

        save_check = QtWidgets.QCheckBox(self)
        save_check.setText("保存到文件")
        save_check.resize(160, 28)
        save_check.stateChanged.connect(lambda: self.check_box_event(save_check.text()))
        save_check.move(20, 345)

        save_line = QtWidgets.QLineEdit(self)
        save_line.resize(170, 25)
        save_line.move(20, 385)
        save_line.setPlaceholderText("Output folder")
        save_line.setReadOnly(True)
        save_line.setStyleSheet("background-color:darkgray")
        save_line.clear()
        save_line.returnPressed.connect(lambda: self.save_export_event(save_line.text(), "returnPressed"))
        lay.addWidget(save_line)

        save_btn = QtWidgets.QPushButton(self)
        save_btn.setText('...')
        save_btn.setFixedSize(30, 23)
        save_btn.setStyleSheet("color:black;background:transparent;")
        save_btn.setDisabled(True)
        save_btn.clicked.connect(lambda: self.save_export_event(save_line.text(), "textChange"))
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
        global alarm_line
        global file_line
        global file_btn

        style_check = QtWidgets.QCheckBox(self)
        style_check.setText("十六进制发送")
        style_check.resize(160, 28)
        style_check.stateChanged.connect(lambda: self.check_box_event(style_check.text()))
        style_check.move(20, 450)

        alarm_check = QtWidgets.QCheckBox(self)
        alarm_check.setText("定时发送")
        alarm_check.resize(160, 28)
        alarm_check.stateChanged.connect(lambda: self.check_box_event(alarm_check.text()))
        alarm_check.move(20, 485)

        alarm_line = QtWidgets.QLineEdit(self)
        alarm_line.resize(130, 25)
        alarm_line.move(120, 485)
        alarm_line.setPlaceholderText("Enter time")
        alarm_line.setReadOnly(True)
        alarm_line.setStyleSheet("background-color:darkgray")
        alarm_line.clear()
        alarm_line.returnPressed.connect(lambda: self.send_time_event(alarm_line.text()))
        lay.addWidget(alarm_line)

        alarm_label = QtWidgets.QLabel(self)
        alarm_label.setText("ms")
        alarm_label.move(260, 485)
        lay.addWidget(alarm_label)

        send_check = QtWidgets.QCheckBox(self)
        send_check.setText("发送文件")
        send_check.resize(160, 28)
        send_check.stateChanged.connect(lambda: self.check_box_event(send_check.text()))
        send_check.move(20, 520)

        file_line = QtWidgets.QLineEdit(self)
        file_line.resize(170, 25)
        file_line.move(120, 520)
        file_line.setPlaceholderText("input file")
        file_line.setReadOnly(True)
        file_line.setStyleSheet("background-color:darkgray")
        file_line.clear()
        file_line.returnPressed.connect(lambda: self.send_file_event(file_line.text(), "returnPressed"))
        lay.addWidget(file_line)

        file_btn = QtWidgets.QPushButton(self)
        file_btn.setText('...')
        file_btn.setFixedSize(30, 23)
        file_btn.setDisabled(True)
        file_btn.setStyleSheet("color:black;background:transparent;")
        file_btn.clicked.connect(lambda: self.send_file_event(file_btn.text(), "textChange"))
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
        send_btn.clicked.connect(lambda: self.send_dat_event(send_line.document().toPlainText()))
        send_btn.move(520, 515)

    def text_edit_write(self, dat):
        self.date_re.setText(dat)

    def line_setting(self):
        lay = QtWidgets.QGridLayout()
        for i in range(0, 20):                                                  # 设置出20x20的格局,目的是把固定空间等分空间
            lay.setColumnStretch(i, 1)
        for i in range(0, 100):
            lay.setRowStretch(i, 1)

        name_label = QtWidgets.QLabel(self)
        name_label.setText("图表名称:")
        lay.addWidget(name_label, 2, 1)

        name_line = QtWidgets.QLineEdit(self)
        name_line.resize(170, 25)
        name_line.setPlaceholderText("This chart name")
        name_line.returnPressed.connect(lambda: self.public_export_event(name_line.text(), "returnPressed"))
        lay.addWidget(name_line, 2, 3)

        x_label = QtWidgets.QLabel(self)
        x_label.setText("X轴名称:")
        lay.addWidget(x_label, 8, 1)

        x_line = QtWidgets.QLineEdit(self)
        x_line.resize(170, 25)
        x_line.setPlaceholderText("X axis name")
        x_line.returnPressed.connect(lambda: self.public_export_event(x_line.text(), "returnPressed"))
        lay.addWidget(x_line, 8, 5)

        y_label = QtWidgets.QLabel(self)
        y_label.setText("Y轴名称:")
        lay.addWidget(y_label, 14, 1)

        y_line = QtWidgets.QLineEdit(self)
        y_line.resize(170, 25)
        y_line.setPlaceholderText("Y axis name")
        y_line.returnPressed.connect(lambda: self.public_export_event(y_line.text(), "returnPressed"))
        lay.addWidget(y_line, 14, 5)

        chart_label = QtWidgets.QLabel(self)
        chart_label.setText("曲线数:")
        lay.addWidget(chart_label, 20, 1)

        chart_combobox = QtWidgets.QComboBox(self)
        chart_combobox.setMaxVisibleItems(6)
        chart_combobox.resize(200, 28)
        chart_combobox.addItems(Serial_Function.chart_num)
        chart_combobox.setCurrentText("1")
        # chart_combobox.currentIndexChanged.connect(lambda: self.string_sheet_event())
        lay.addWidget(chart_combobox, 20, 5)

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

    def save_export_event(self, export_folder, category):
        global default_path
        global export_path

        if os.path.exists(export_folder):
            catch_path = export_folder
        else:
            if os.path.isdir(default_path):
                catch_path = default_path
            else:
                catch_path = os.path.dirname(default_path[0])
        if category == "returnPressed":
            pass
        elif category == "textChange":
            catch_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select export folder", catch_path)
        if catch_path != "":
            save_line.setText(str(catch_path))
            export_path = catch_path
            default_path = catch_path
        else:
            pass

    def check_box_event(self, check_func):
        if check_func == "十六进制显示":
            if display_check.isChecked() is True:
                a = 0
            else:
                a = 0

        elif check_func == "暂停接收显示":
            if pause_check.isChecked() is True:
                a = 0
            else:
                a = 0

        elif check_func == "保存到文件":
            if save_check.isChecked() is True:
                save_line.setReadOnly(False)
                save_line.setStyleSheet("background-color:white")
                save_btn.setEnabled(True)
            else:
                save_line.setReadOnly(True)
                save_line.setStyleSheet("background-color:darkgray")
                save_line.clear()
                save_btn.setDisabled(True)

        elif check_func == "十六进制发送":
            if style_check.isChecked() is True:
                a = 0
            else:
                a = 0

        elif check_func == "定时发送":
            if alarm_check.isChecked() is True:
                alarm_line.setReadOnly(False)
                alarm_line.setStyleSheet("background-color:white")
            else:
                alarm_line.setReadOnly(True)
                alarm_line.setStyleSheet("background-color:darkgray")
                alarm_line.clear()

        elif check_func == "发送文件":
            if send_check.isChecked() is True:
                file_line.setReadOnly(False)
                file_line.setStyleSheet("background-color:white")
                file_btn.setEnabled(True)
            else:
                file_line.setReadOnly(True)
                file_line.setStyleSheet("background-color:darkgray")
                file_line.clear()
                file_btn.setDisabled(True)
        else:
            pass

    def send_dat_event(self, send_byte):
        _serial.serial_write(send_byte, "DEC")

    def send_file_event(self, input_file, category):
        global default_path
        global input_path

        if os.path.exists(input_file):
            catch_path = input_file
        else:
            catch_path = default_path

        if category == "returnPressed":
            pass
        elif category == "textChange":
            catch_path = QtWidgets.QFileDialog.getOpenFileName(self, "Open File Dialog", catch_path,
                                                               "Source file (*.txt)")[0]
            if catch_path != "":
                file_line.setText(str(catch_path))
                input_path = catch_path
                default_path = catch_path
        else:
            pass

    def send_time_event(self, send_time):
        global time_send

        time_send = send_time


def open_btn_event(current_text, __flag_serial):
    if current_text == "打开串口":
        _como = serial_combobox.currentText().split("(")
        try:
            port = _como[1].rstrip(")")
        except:
            pass
        else:
            baudrate = int(baud_combobox.currentText())
            bytesize = int(date_combobox.currentText())
            parity = Serial_Function.serial_check[check_combobox.currentText()]
            stopbits = int(stop_combobox.currentText())

            _serial.get_serial(port, baudrate, bytesize, parity, stopbits)
            if _serial.open_serial() is True:
                open_btn.setText("关闭串口")
                open_btn.setStyleSheet("background-color:rgba(35,140,44,1);"
                                       "border-color:rgba(255,255,255,30);"
                                       "border-width:3px;"                  # border width
                                       "border-radius:8px;"                 # border radius
                                       "border-color:rgba(255,255,255,200);"  # border color
                                       "font:bold 22px;"                    # font & size
                                       "font-family:'楷体';"
                                       "padding:3px;")                      # padding
                __flag_serial.put("Serial_opened")

    elif current_text == "关闭串口":
        if _serial.close_serial() is True:
            open_btn.setText("打开串口")
            open_btn.setStyleSheet("background-color:skyblue;"          # background(also use picture)
                                   "border-style:outset;"               # border style(inset/outset)
                                   "border-width:3px;"                  # border width
                                   "border-radius:8px;"                 # border radius
                                   "border-color:rgba(255,255,255,200);"  # border color
                                   "font:bold 22px;"                    # font & size
                                   "font-family:'楷体';"
                                   "color:rgba(0,0,0,200);"             # font color
                                   "padding:3px;")                      # padding
            __flag_serial.put("Serial_closed")
    else:
        pass
