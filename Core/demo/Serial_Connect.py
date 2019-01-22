import sys
import serial
import serial.tools.list_ports


class SerialInformation:
    def __init__(self):
        pass

    def get_free_com(self):
        plist = list(serial.tools.list_ports.comports())

        if len(plist) <= 0:
            serial_name = ''
            # print("没有发现端口!")
        else:
            plist_0 = list(plist[0])
            serial_name = plist_0[0]
            # serialFd = serial.Serial(serialName, 9600, timeout=60)
            # print("可用端口名>>>", serialFd.name)
        return serial_name

