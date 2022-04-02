import win32clipboard
import win32con
import win32api
from threading import Thread
from socket import *


def clipboardSetText(aString):
    _w = win32clipboard
    _w.OpenClipboard()
    _w.EmptyClipboard()
    # _w.SetClipboardData(win32con.CF_UNICODETEXT, aString)
    _w.SetClipboardData(13, aString)
    _w.CloseClipboard()


def paste():
    # Ctrl + V
    win32api.keybd_event(17, 0, 0, 0)
    win32api.keybd_event(86, 0, 0, 0)
    win32api.keybd_event(86, 0, 2, 0)
    win32api.keybd_event(17, 0, 2, 0)
    # 回车
    win32api.keybd_event(13, 0, 0, 0)
    win32api.keybd_event(13, 0, 2, 0)


def copy_paste(aString):
    clipboardSetText(aString)
    paste()


class TcpClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.tcp_client_socket: socket = socket(AF_INET, SOCK_STREAM)
        self.recv_func = lambda _: print(_)
        self.is_open = False
        self.error = None
        self.tout = 0

    def connect(self, host: str = None, port: int = None):
        self.host = host if host else self.host
        self.port = port if port else self.port
        try:
            self.close()
            self.tcp_client_socket = socket(AF_INET, SOCK_STREAM)
            self.timeout()
            self.tcp_client_socket.connect((self.host, self.port))
            self.is_open = True
        except Exception as _err:
            self.is_open = False
            raise _err

        if self.is_open:
            Thread(target=self.recv, daemon=True).start()

        return 200

    def recv(self):
        recvData = b''
        while self.is_open:
            try:
                recvData += self.tcp_client_socket.recv(1024)
                if recvData:
                    raise timeout
                else:
                    self.is_open = False
                    while not self.is_open:
                        try:
                            self.connect()
                            break
                        except timeout:
                            continue
                    break
            except timeout:
                if recvData:
                    data = recvData.decode('utf-8').strip()
                    self.recv_func(data)
                    recvData = b''
            except OSError:
                print('OSError')
                self.close()
            except Exception as _recv_err:
                print("_recv_err", _recv_err)
                self.close()

    def timeout(self, t=None):
        if t:
            self.tout = t
        self.tcp_client_socket.settimeout(self.tout)

    def close(self):
        if self.is_open:
            self.is_open = False
            self.tcp_client_socket.close()

    def isOpen(self):
        return self.is_open


if __name__ == '__main__':
    import time

    # 创建socket
    tcp_client_socket = TcpClient('192.168.1.125', 8080)
    tcp_client_socket.timeout(1)
    tcp_client_socket.connect()
    input()
    tcp_client_socket.close()
