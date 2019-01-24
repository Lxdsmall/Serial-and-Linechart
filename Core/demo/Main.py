import sys
import time
import threading
from PySide2 import QtWidgets
import Serial_Gui
import Serial_Function

class Thread_Gui(threading.Thread):
    def __init__(self, thread_id, thread_name):
        threading.Thread.__init__(self)
        self.threadid = thread_id
        self.threadname = thread_name

    def run(self):
        print("开始线程：" + self.threadname)
        app = QtWidgets.QApplication(sys.argv)
        window = Serial_Gui.GUIConfigSerial()
        window.show()
        sys.exit(app.exec_())
        # print("退出线程：" + self.threadname)


class Thread_Receive(threading.Thread):
    def __init__(self, thread_id, thread_name):
        threading.Thread.__init__(self)
        self.threadid = thread_id
        self.threadname = thread_name

    def run(self):
        print("开始线程：" + self.threadname)
        _serial = Serial_Function.SerialFunction()
        flag = Serial_Function.flag_open_serial
        if flag == 1:
            str_buffer = _serial.serial_read()
            str_buffer = "234567\n"
            print(str_buffer)
        else:
            flag = Serial_Function.flag_open_serial
        # print("退出线程：" + self.threadname)


if __name__ == "__main__":
    thread_1 = Thread_Gui(1, "Serial_Gui")
    thread_2 = Thread_Receive(2, "Thread_Receive")

    thread_1.setDaemon(True)
    thread_2.setDaemon(True)
    thread_1.start()
    thread_2.start()

    thread_1.join()
    thread_2.join()
    print("退出主线程")
