import sys
import serial
import serial.tools.list_ports

global flag_open_serial                                     # 串口打开标志位

flag_open_serial = 0
serial_bps = ["1200", "2400", "4800", "9600", "19200", "38400", "57600", "115200"]
serial_date = ["5", "6", "7", "8"]
serial_check = {"偶校验": "E", "奇校验": "O", "高校验": "M", "低校验": "S", "无": "N"}
serial_stop = ["1", "1.5", "2"]
chart_num = ["1", "2", "3", "4"]
# BAUDRATES = {"1200": 1200, "1800": 1800, "2400": 2400, "4800": 4800, "9600": 9600, "19200": 19200, "38400": 38400, "57600": 57600, "115200": 115200}
# BYTESIZES = {"FIVEBITS": "5", "SIXBITS": "6", "SEVENBITS": "7", "EIGHTBITS": "8"}
# PARITIES = {"PARITY_NONE": "偶校验", "PARITY_EVEN": "奇校验", "PARITY_ODD": "高校验", "PARITY_MARK": "低校验", "PARITY_SPACE": "无"}
# STOPBITS = {"STOPBITS_ONE": "1", "STOPBITS_ONE_POINT_FIVE": "1.5", "STOPBITS_TWO": "2"}


class SerialFunction:
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
            # print("可用端口名>>>", serialFd.name)
        return serial_name

    def open_serial(self, serial_port, serial_baudrate, serial_bytesize, serial_parity, serial_stopbits):
        global serial_com
        serial_com = serial.Serial(port=serial_port, baudrate=serial_baudrate, bytesize=serial_bytesize,
                                   parity=serial_parity, stopbits=serial_stopbits)
        if serial_com.isOpen() is True:
            flag_open_serial = 1
            return True
        else:
            return False

    def close_serial(self):
        serial_com.close()
        if serial_com.isOpen() is True:
            return False
        else:
            flag_open_serial = 0
            return True

    # def get_serial_statu(self):
    #     if serial_com.isOpen() is True:
    #         return True
    #     else:
    #         return False

    def serial_read(self, size):
        return serial_com.read(size)

    def serial_write(self, send_buf, send_type):
        if send_type == "DEC":
            serial_com.write(send_buf)

        elif send_type == "HEX":
            lang = len(send_buf)
            if (lang % 2) == 0:
                pass
            else:                                # 需要注意一点，如果字符串list的长度为奇数，则decode会报错，可以按照实际情况，用字符串的切片操作，在字符串的开头或结尾加一个'0'
                send_buf = send_buf + '0'
                buf = send_buf.decode("hex")
                serial_com.write(buf)
        else:
            pass
