# coding:utf-8

"""
Time:     ${DATE} ${TIME}
Author:   alwayaway
e-mail: alwayaway@foxmail.com
Version:  V 1.1
File:     ${NAME}.py
Describe: Config by sqlite3 or  file[.ini/.conf]
"""

import serial
import time
from serial.tools import list_ports


def get_paritys_dict():
    return {
        'None': 'N',
        'Even': 'E',
        'Odd': 'O',
        'Mark': 'M',
        'Space': 'S',
    }


def get_bytesizes_list():
    return '5', '6', '7', '8'


def get_stopbitses_list():
    return '1', '1.5', '2'


def get_baudrates_list():
    return ('50', '75', '110', '134', '150', '200', '300', '600', '1200', '1800', '2400', '4800',
            '9600', '19200', '38400', '57600', '115200', '230400', '460800', '500000', '576000', '921600',
            '1000000', '1152000', '1500000', '2000000', '2500000', '3000000', '3500000', '4000000')


def get_port_list():
    """获取本机可用端口列表"""
    PORT_LIST = [list(i)[0] for i in list_ports.comports()]
    return PORT_LIST


class Ser:
    def __init__(self, port=None, baudrate=9600, bytesize=8, parity='N', stopbits=1, **kwargs):
        """
        串口读写类
        :param port: 端口名称
        :param baudrate: 波特率
        :param bytesize: 数据位
        :param parity: 校验位
        :param stopbits: 停止位
        timeout=None,
        xonxoff=False,
        rtscts=False,
        write_timeout=None,
        dsrdtr=False,
        inter_byte_timeout=None,
        exclusive=None,
        """
        self.read_fps = 0.03  # 为防止影响整体性能，限制读取帧数，默认30fps
        self.com = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=bytesize,
            parity=parity,
            stopbits=stopbits,
            **kwargs
        )

    def open(self, port=None, baudrate=9600, bytesize=8, parity='N', stopbits=1, **kwargs):
        self.com = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=bytesize,
            parity=parity,
            stopbits=stopbits,
            **kwargs
        )

    def set_fps(self, fps: int):
        self.read_fps = 1 / fps
        self.com.read_all()

    def write(self, data: str or bytes, encoding='utf-8', errors='strict'):
        """
        write data to serial
        :param errors:  'ignore', 'replace', 'xmlcharrefreplace', 'backslashreplace' or codecs.register_error()
        :param encoding: 字符编码
        :param data: 字节或字符串
        :return: data -> bytes
        """
        try:
            if type(data) is not bytes:
                data = data.encode(encoding=encoding, errors=errors)
            self.com.write(data)
            return _Semantide(msg=data)
        except Exception as e:
            return _Semantide(False, msg=e)

    def write_hex(self, data: str):
        """
        write hex to serial
        e.g : 00 FF 0A 0C 0D
        :param data: 16进制字符串
        :return: data -> bytes
        """
        try:
            self.com.write(bytes().fromhex(data))
            return _Semantide(msg=data)
        except Exception as e:
            return _Semantide(False, e)

    def close(self):
        self.com.close()

    def read_theard(self, func, *args, rdhex=False, _log=None, **kwargs):
        """
        使用线程启动该函数，重复读取端口数据并执行传入方法，传入方法的第一个参数为端口读取的参数
        :param _log:    外部传入接收错误信号
        :param rdhex:   开启读取16进制，默认关闭
        :param func:    接收数据后处理函数
        :param args:    函数参数
        :param kwargs:  函数参数
        :return:
        """
        if rdhex:
            reader = self.readhex
        else:
            reader = self.read
        while self.com.is_open:
            data = reader()
            if data:
                try:
                    func(data, *args, **kwargs)
                except Exception as _e:
                    if _log:
                        _log(f"{func.__name__}执行发生错误:\n\t参数：{args}{kwargs}\n\tError:{_e}")

    def read(self, timeout=0):
        """
        单次读取串口数据， 返回字符串
        :param timeout: 超时设置
        :return: 返回读取数据或超时后返回 TimeoutError
        """
        while self.com.is_open:
            if self.com.in_waiting > 0:
                if self.com.timeout is None:
                    return self.com.readline().decode(errors='ignore').strip()
                else:
                    return self.com.readall().decode(errors='ignore').strip()
            else:
                time.sleep(self.read_fps)

    def readhex(self, timeout=0):
        """
        单次读取串口数据， 返回16进制字符串
        :param timeout: 超时设置
        :return: 返回读取的16进制或超时后返回 TimeoutError
        """
        start = time.time()
        while True:
            if self.com.in_waiting > 0:
                if self.com.timeout is None:
                    return self.com.readline().hex().strip()
                else:
                    return self.com.readall().hex().strip()
            if timeout > 0 and time.time() >= start + timeout:
                return TimeoutError
            else:
                time.sleep(self.read_fps)

    def timeout(self, t=None):
        """
        设置读取超时, 当串口传入数据间隔低于该时长时，立即返回已读数据
        :param t:
        :return: timeout
        """
        if t is None:
            return self.com.timeout
        self.com.timeout = t

    def isOpen(self):
        return self.com.is_open


class _Semantide:
    """信息载体类"""

    def __init__(self, _bool=True, msg=None):
        self.__bool = _bool
        self.__msg = msg

    def __bool__(self):
        return self.__bool

    def __str__(self):
        return self.__msg


if __name__ == '__main__':
    port_list = get_port_list()
    print(f"本机可用端口： {port_list}")
    if port_list:
        c1 = Ser(port_list[0], baudrate=115200)
        c1.timeout(0.1)
        if c1.com.is_open:
            c1.read_theard(lambda value: print(value.replace('', '')), rdhex=False)
        c1.close()
    else:
        print("This computer has no serial port available!")
