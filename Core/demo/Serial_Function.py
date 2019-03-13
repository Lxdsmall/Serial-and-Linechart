import sys
import time
import serial
import binascii
import serial.tools.list_ports


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
        ports = []
        if len(plist) <= 0:
            serial_name = ''
            print("没有发现端口!")
        else:
            for port in plist:
                serial_name = port[1]
                ports.append(str(port[1]))
                print("可用端口名>>>", serial_name)
        return ports

    def get_serial(self, serial_port, serial_baudrate, serial_bytesize, serial_parity, serial_stopbits):
        global serial_com
        # serial_com = serial.Serial(port=serial_port, baudrate=serial_baudrate, bytesize=serial_bytesize,
        #                            parity=serial_parity, stopbits=serial_stopbits)

        serial_com = serial.Serial()
        serial_com.port = serial_port
        serial_com.baudrate = serial_baudrate
        serial_com.bytesize = serial_bytesize
        serial_com.parity = serial_parity
        serial_com.stopbits = serial_stopbits
        serial_com.timeout = 0.5
        serial_com.writeTimeout = 0.5

    def get_serial_mode(self):
        if serial_com.isOpen() is True:
            return True
        else:
            return False

    def open_serial(self):
        if serial_com.isOpen() is True:
            serial_com.close()
        else:
            pass
        serial_com.open()
        print("串口名: " + str(serial_com.port))                                    # 串口名
        print("波特率: " + str(serial_com.baudrate))                                # 波特率
        print("字节数: " + str(serial_com.bytesize))                                # 字节大小
        print("校验位: " + str(serial_com.parity))                                  # 校验位N－无校验，E－偶校验，O－奇校验
        print("停止位: " + str(serial_com.stopbits))                                # 停止位
        print("读超时: " + str(serial_com.timeout))                                 # 读超时设置
        print("写超时: " + str(serial_com.writeTimeout))                            # 写超时
        print("软件流控: " + str(serial_com.xonxoff))                               # 软件流控
        print("硬件流控: " + str(serial_com.rtscts))                                # 硬件流控
        print("硬件流控: " + str(serial_com.dsrdtr))                                # 硬件流控
        print("字符间隔超时: " + str(serial_com.interCharTimeout))                   # 字符间隔超时
        return self.get_serial_mode()

    def close_serial(self):
        if serial_com.isOpen() is True:
            serial_com.close()
        else:
            pass

        if self.get_serial_mode() is True:
            return False
        else:
            return True

    def serial_wating(self):
        return serial_com.inWaiting()

    def serial_read(self, size):
        return serial_com.read(size)

    def serial_readline(self):
        return serial_com.readline()

    def serial_write(self, send_buf, send_type):
        if send_type == "DEC":
            serial_com.write(send_buf.encode("utf-8"))

        elif send_type == "HEX":
            if (len(send_buf) % 2) == 0:
                pass
            else:                                # 需要注意一点，如果字符串list的长度为奇数，则decode会报错，可以按照实际情况，用字符串的切片操作，在字符串的开头或结尾加一个'0'
                send_buf = '0' + send_buf

            buf = bytes.fromhex(send_buf)
            serial_com.write(buf)

        else:
            pass
