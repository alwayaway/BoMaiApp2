import sys
import os

from PySide6.QtCore import QUrl, QObject, Slot, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtNetwork import QNetworkCookie
# 导入QWebChannel
from PySide6.QtWebChannel import QWebChannel

from BMAPP.js import JsMethods
from toolbase import *


ini = Cfgfile('config/setup.ini')
cfg = Cfgdbase('config/config.cfg')
log = Log('log', 'app')

Host = ini.get('Server', 'Host', '127.0.0.1')

# 定义一个类，其中包含一个槽函数，供JS代码调用来计算阶乘
class Factorial(QObject):
    # 将其定义为一个槽函数，参数类型为int，返回值类型为int
    @Slot(int, result=int)
    def factorial(self, n):
        if n == 0 or n == 1:
            return 1
        else:
            return self.factorial(n - 1) * n


# 定义一个channel全局对象，用于注册一些对象提供给html页面中的JS代码调用
channel = QWebChannel()
# 定义一个对象，其中包含槽函数，注册到channel可以传递给JS代码
factorial = Factorial()


class DemoWin(QWidget):

    def __init__(self):
        super(DemoWin, self).__init__()
        self.js = JsMethods()
        self.browser = QWebEngineView()
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.browser.loadFinished.connect(lambda *x: self.browser.page().runJavaScript(self.js.VueJs))
        self.browser.page().profile().cookieStore().cookieAdded.connect(lambda *x:print(x))
        session = QNetworkCookie()
        session.setName(b'sessionid')
        session.setValue(b's9faj6vt6pbrgth6t8m9jffn5dec08rr')
        session.setHttpOnly(True)
        session.setDomain(Host)
        session.setPath('/')
        self.browser.page().profile().cookieStore().setCookie(session)
        self.browser.page().profile().downloadRequested.connect(self.on_downloadRequested)  # 页面下载请求
        self.initUI()
        self.up_icon()

    def up_icon(self):
        url = f'http://{Host}:8000/media/logo.png'
        the_filename = 'icon.ico'
        the_sourceFile = 'images'
        _page = QWebEngineView()

        def _upd():
            app.setWindowIcon(QIcon("images/icon.ico"))
            _page.page().profile().downloadRequested.disconnect(up_icon)
            self.browser.page().profile().downloadRequested.connect(self.on_downloadRequested)

        def up_icon(_up):
            _up.setDownloadDirectory(the_sourceFile)
            _up.setDownloadFileName(the_filename)
            _up.accept()
            _up.isFinishedChanged.connect(_upd)

        self.browser.page().profile().downloadRequested.disconnect(self.on_downloadRequested)
        _page.page().profile().downloadRequested.connect(up_icon)
        _page.page().download(url, the_filename)


    def initUI(self):
        self.setWindowTitle("博迈UDI——APP")
        # 将窗口设置为动图大小
        self.resize(1280, 768)
        url = f'http://{Host}:8000/admin/'
        # self.browser.load(QUrl(url))
        # self.browser.setContextMenuPolicy(Qt.CustomContextMenu)
        self.load_loc_test(None)
        layout = QVBoxLayout(self)
        layout.addWidget(self.browser)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        # 添加窗口标题

    def load_loc_test(self, loaded):
        if not loaded:
            self.browser.load(QUrl.fromLocalFile(os.path.abspath('test.html')))
            # 将factorial对象注册到channel中，名字为obj，JS中使用这个名字来调用函数
            channel.registerObject("obj", factorial)
            # 将channel传递给html中的JS
            self.browser.page().setWebChannel(channel)

    def getFullName(self):
        # 传递参数value到JS函数
        value = "Hello World"
        # 调用JS中的fullName函数
        self.browser.page().runJavaScript('fullName("' + value + '");')

    # 支持页面下载按钮
    def on_downloadRequested(self, downloadItem):
        if downloadItem.isFinished() == False and downloadItem.state() == 0:
            the_filename = 'base.btw'
            the_sourceFile = 'base'
            downloadItem.setDownloadDirectory(the_sourceFile)
            downloadItem.setDownloadFileName(the_filename)
            downloadItem.accept()
            downloadItem.isFinishedChanged.connect(lambda *x: self.on_downloaded(downloadItem))
            # from PySide6.QtWebEngineCore import QWebEngineDownloadRequest

    # 下载结束触发函数
    def on_downloaded(self, downloadItem):
        downloadItem.deleteLater()
        js_string = self.js.success('下载成功!')
        self.browser.page().runJavaScript(js_string)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("images/icon.ico"))
    # 创建一个主窗口
    mainWin = DemoWin()
    # 显示
    mainWin.show()
    # 主循环
    sys.exit(app.exec())