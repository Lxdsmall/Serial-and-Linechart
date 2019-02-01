import sys
import time
from PySide2 import QtWidgets
import Serial_Gui
from Serial_Gui import GUIConfigSerial
from Serial_Function import SerialFunction
from multiprocessing import Queue, Process


def serial_gui(flag_serial):
    print("开始线程：Serial_Gui")
    app = QtWidgets.QApplication(sys.argv)
    _window = GUIConfigSerial(flag_serial)
    _window.show()
    flag_serial.put("Start")
    app.exec_()
    flag_serial.put("Exit")
    print("退出线程：Serial_Gui")


def serial_receive(flag_serial):
    time.sleep(2)
    if not flag_serial.empty():
        flag = flag_serial.get()
        if flag == "Start":
            print("开始线程：Thread_Receive")
            while True:
                if flag == "Serial_opened":
                    n_receive = SerialFunction.serial_wating()
                    if n_receive > 0:
                        str_buffer = SerialFunction.serial_readline()
                        # str_buffer = "234567\n"
                        # GUIConfigSerial.text_edit_write(str_buffer, "DEC")
                        print(str_buffer)
                else:
                    if not flag_serial.empty():
                        flag = flag_serial.get()

                if not flag_serial.empty():                                  # 取信号前先判断信号池是否为空，否则会timeout
                    if flag_serial.get() == "Exit":
                        break
            print("退出线程：Thread_Receive")


if __name__ == "__main__":
    flag_serial = Queue(maxsize=20)                # 消息队列

    # 创建线程
    thread_1 = Process(target=serial_gui, args=(flag_serial,))
    thread_2 = Process(target=serial_receive, args=(flag_serial,))

    # 启动线程
    thread_1.start()
    thread_2.start()
    print("开始线程  " + time.strftime("%H:%M:%S", time.localtime()))

    # 等待线程结束
    thread_1.join()
    thread_2.join()
    print("退出主线程  " + time.strftime("%H:%M:%S", time.localtime()))
