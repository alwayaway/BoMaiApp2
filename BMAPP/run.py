# -*- coding:utf-8 -*
import cgitb

import json
import sys

import win32api
from PySide2.QtCore import QDir, QFile, QObject, QTranslator, QUrl, Slot, Qt
from PySide2.QtGui import QIcon
from PySide2.QtNetwork import QLocalServer, QLocalSocket, QNetworkCookie
from PySide2.QtWebChannel import QWebChannel
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtWidgets import QApplication, QFileDialog, QMessageBox, QVBoxLayout, QWidget

from subprocess import Popen
from threading import Thread

from BMAPP.js import JsMethods
from BMAPP.Qtool import tool
from toolbase import *

cgitb.enable(logdir='log', format="text")

check_dir(('log', 'images', 'base'))
ini = Cfgfile('config/setup.ini')
cfg = Cfgdbase('config/config.cfg')
log = Log('log', 'app')

Host = ini.get('Server', 'Host', '127.0.0.1')
Port = ini.get('Server', 'Port', '8000')

Api = tool.HttpTool()

__APP__ = '博迈UDI管理系统'
__VERSION__ = 'V1.0.1'


def geturl(url: str):
    host = f'http://{Host}'
    if Port:
        host += f':{Port}'
    if url.startswith('/'):
        return host + url
    else:
        return f'{host}/{url}'


class Factorial(QObject):
    def __init__(self, *args, **kwargs):
        super(Factorial, self).__init__(*args, **kwargs)
        self.btwFile = 'base/base.btw'
        self.Writer = lambda data, row: tool.XlsxWriter('base/data.xlsx', json.loads(data), row)
        self.btSdk = {
            "x86": "service/x86/BtService_x86.exe",
            "x64": "service/x64/BtService_x64.exe",
        }

    @staticmethod
    def result(lod: bool, msg: str):
        return json.dumps({
            "res": lod, "msg": msg
        }, ensure_ascii=False)

    @Slot(str, result=str)
    def btSelector(self, path):
        file_, type_ = QFileDialog.getOpenFileName(mainWin, "选中bt执行器", QDir.homePath(), "exe Files (*.exe)")
        return file_ if file_ else path

    @Slot(str, result=bool)
    def saveConf(self, conf):
        print(f'conf:{conf}')
        conf = json.loads(conf)
        if conf:
            for k, v in conf.items():
                cfg.set('app', k, v)
            mainWin.browser.page().runJavaScript('reLoadCfg()')
            return True
        else:
            return False

    @Slot(str, str, str, result=str)
    def getConf(self, key, sel, init):
        val = cfg.get(key, sel, init)
        print(val)
        return val

    @Slot(str, result=str)
    def getCfgSet(self, sel):
        val = cfg.getOpts(sel)
        val = json.dumps(val, ensure_ascii=False)
        print(val)
        return val

    @Slot(str, result=str)
    def loadBase(self, base):
        try:
            bty = cfg.get('@btwBase', base)
            if bty:
                msg = '从本地加载'
                with open(self.btwFile, mode='wb')as _wb:
                    _wb.write(bty)
                lod = True
            else:
                msg = '从服务器加载'
                url = f'api/verify/GetBtwByName?btw={base}'
                downer = tool.DownLoader(url=geturl(url), file=self.btwFile, http=Api)
                downer.finished = lambda: self.saveBtw(base)
                downer.start()
                downer.wait(5)
                if not downer.error():
                    lod = True
                else:
                    msg = f'加载失败{downer.error()}'
                    lod = False
        except Exception as _load_err:
            lod = False
            msg = f'加载失败{_load_err}'
        return json.dumps({
            "res": lod, "msg": msg, "file": os.path.abspath(self.btwFile)
        }, ensure_ascii=False)

    @Slot(str, result=str)
    def reloadBase(self, base):
        url = f'api/verify/GetBtwByName?btw={base}'
        downer = tool.DownLoader(url=geturl(url), file=self.btwFile, http=Api)
        downer.finished = lambda: self.saveBtw(base)
        downer.start()
        downer.wait(5)
        if not downer.error():
            msg = f'从服务器加载模板 {base} 成功!'
            lod = True
        else:
            msg = f'加载失败{downer.error()}'
            lod = False
        return json.dumps({
            "res": lod, "msg": msg
        }, ensure_ascii=False)

    def saveBtw(self, base):
        with open(self.btwFile, mode='rb')as _rb:
            cfg.set('@btwBase', base, _rb.read())

    @Slot(str, result=str)
    def editBtw(self, base):
        _editor = Thread(target=self._editBtw, args=(base,), daemon=True)
        _editor.start()
        time.sleep(0.5)
        if _editor.is_alive():
            return self.result(True, f'编辑模板{base}')
        else:
            return self.result(False, f'未知原因，无法执行编辑进程！')

    def _editBtw(self, base):
        try:
            _exe = cfg.get('app', '@BtExe', '')
            if not os.path.exists(_exe):
                mainWin.runJavaScript(mainWin.js.error("未找到bt执行器，请到本地参数配置页面配置执行器后再次尝试操作"))
                return
            cmd = [
                _exe,
                self.btwFile
            ]
            shell = ini.get('cmd', 'shell', '0')
            shell = True if shell == '1' else False
            _run = Popen(cmd, shell=shell)
            _run.wait()
            self.saveBtw(base)
            mainWin.runJavaScript(mainWin.js.success('模板自动保存成功！'))
        except Exception as _edit_err:
            mainWin.runJavaScript(mainWin.js.error(f"{_edit_err}"))

    @Slot(str, int, result=str)
    def prtBtw(self, data, num):
        try:
            print(num)
            # return self.result(False, f'测试{num}， {type(num)}')
            print(data)
            self.Writer(data, num)
            _exe = cfg.get('app', '@BtExe', '')
            if not os.path.exists(_exe):
                return self.result(False, f"未找到bt执行器，请到本地参数配置页面配置执行器后再次尝试操作")
            cmd = [
                _exe,
                self.btwFile, '/p', '/x', '/C=1'
            ]
            shell = ini.get('cmd', 'shell', '0')
            shell = shell == '1'
            _run = Popen(cmd, shell=shell)
            time.sleep(0.5)
            if _run.pid:
                return self.result(True, f'打印进程PID： {_run.pid}')
            else:
                return self.result(False, f'未知原因，无法执行编辑进程！')
        except Exception as _prt_err:
            return self.result(False, f"{_prt_err}")

    @Slot()
    def reload(self):
        _app.exit(0)

    @Slot(str, str, result=bool)
    def setIniCfg(self, host, port):
        # noinspection PyBroadException
        try:
            ini.set('Server', 'Host', host)
            ini.set('Server', 'Port', port)
        except:
            return False
        return True


channel = QWebChannel()
factorial = Factorial()


class DemoWin(QWidget):
    def __init__(self):
        super(DemoWin, self).__init__()
        self.loadDOM = True
        self.js = JsMethods()
        self.browser = QWebEngineView()
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.page = self.browser.page()
        self.profile = self.browser.page().profile()
        self.browser.loadFinished.connect(lambda *x: self.browser.page().runJavaScript(self.js.VueJs))
        self.profile.cookieStore().deleteAllCookies()
        self.profile.cookieStore().cookieAdded.connect(self.get_cookie)
        self.profile.cookieStore().cookieRemoved.connect(self.del_cookie)
        self.profile.downloadRequested.connect(self.on_downloadRequested)  # 页面下载请求
        self.cookies: dict = eval(cfg.get('cookie', Host, '{}'))
        self.setStyleSheet(f'background:white')
        self.reloaded = 0

        self.up_icon()

        self.initCookie()
        self.initUI()

    def runJavaScript(self, js_string):
        self.browser.page().runJavaScript(js_string)

    @staticmethod
    def up_icon():
        file = 'images/icon.ico'
        if not os.path.exists(file):
            url = f'http://{Host}:{Port}/media/logo.png'
            loader = tool.DownLoader(url, file)
            loader.finished = lambda: _app.setWindowIcon(QIcon(file))
            loader.start()

    def initCookie(self):

        for _i in self.cookies.values():
            cookie = QNetworkCookie()
            for k, v in _i.items():
                exec(f'cookie.{k}(v)')
            if cookie.name() == b'sessionid':
                Api.setCookie(name=cookie.name().data().decode(), domain=cookie.domain(),
                              path=cookie.path(), value=cookie.value().data().decode())
                continue
            else:
                self.profile.cookieStore().setCookie(cookie)

    def get_cookie(self, cookie: QNetworkCookie):
        # print(cookie)
        cookie_d = {
            'setName': cookie.name().data(),
            'setValue': cookie.value().data(),
            'setDomain': cookie.domain(),
            'setPath': cookie.path(),
            'setHttpOnly': cookie.isHttpOnly(),
        }
        self.cookies[f'{cookie.name()}'] = cookie_d
        cfg.set('cookie', Host, f"{self.cookies}")
        if cookie.name() == b'sessionid':
            Api.setCookie(name=cookie.name().data().decode(), domain=cookie.domain(),
                          path=cookie.path(), value=cookie.value().data().decode())

    def del_cookie(self, cookie: QNetworkCookie):
        print(cookie)
        self.cookies.pop(f'{cookie.name()}')
        cfg.set('cookie', Host, f"{self.cookies}")
        if cookie.name() == b'sessionid':
            Api.cookie.clear(name=cookie.name().data().decode(), domain=cookie.domain(), path=cookie.path())

    def initUI(self):
        self.setWindowTitle(__APP__ + __VERSION__)
        # 将窗口设置为动图大小
        self.resize(1280, 768)
        self.browser.setHidden(True)
        url = f'http://{Host}:{Port}/AppMain/'
        self.browser.setContextMenuPolicy(Qt.CustomContextMenu)
        self.browser.load(QUrl(url))
        self.setWebF()

        layout = QVBoxLayout(self)
        layout.addWidget(self.browser)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.loadDOM = False
        # 添加窗口标题

    def setWebF(self):
        channel.registerObject("obj", factorial)
        self.browser.page().setWebChannel(channel)
        self.browser.loadFinished.connect(self._loaded)

    def _loaded(self, res):
        if self.reloaded < 3:
            self.reloaded += 1
            if res:
                self.browser.setHidden(False)
            else:
                file = os.path.abspath('html/empty.html')
                self.browser.load(QUrl.fromLocalFile(file))
                self.setWebF()
        else:
            pass

    def on_downloadRequested(self, downloadItem):
        if downloadItem.isFinished() == False and downloadItem.state() == 0:
            file_, type_ = QFileDialog.getSaveFileName(self, "文件下载", QDir.homePath(),
                                                       "Btw File (*.btw);;All File (*.*)")

            if QFile.exists(file_):
                ret = QMessageBox.question(
                    self,
                    "File exists",
                    "Do you want to overwrite the file ?",
                    QMessageBox.Yes | QMessageBox.No,
                )
                if ret == QMessageBox.No:
                    js_string = self.js.information('取消下载!')
                    self.browser.page().runJavaScript(js_string)
                    return

                QFile.remove(file_)

            if not file_:
                js_string = self.js.information('取消下载!')
                self.browser.page().runJavaScript(js_string)
                return
            file_ = file_.split('/')
            the_filepath, the_filename = '/'.join(file_[:-1]), file_[-1]
            downloadItem.setDownloadFileName(the_filename)
            downloadItem.setDownloadDirectory(the_filepath)
            downloadItem.accept()
            downloadItem.isFinishedChanged.connect(lambda *x: self.on_downloaded(downloadItem))

    # 下载结束触发函数
    def on_downloaded(self, downloadItem):
        if downloadItem.state() == 2:
            js_string = self.js.success('下载成功!')
        elif downloadItem.state() == 3:
            js_string = self.js.information('取消下载!')
        else:
            js_string = self.js.error('下载失败!')
        downloadItem.deleteLater()
        self.browser.page().runJavaScript(js_string)


try:
    _args = sys.argv
    debug__port: str = ini.get('debug', 'port', '9600')
    if debug__port.isdigit() and int(debug__port) > 9600:
        _args.append(f'--remote-debugging-port={debug__port}')
    try:
        _app = QApplication(_args)
    except RuntimeError:
        _app = QApplication.instance()
    _app.setStyle('Fusion')
    # noinspection PyArgumentList
    _trans = QTranslator()
    # noinspection PyArgumentList
    _trans.load('config/ZH_CN')
    _app.installTranslator(_trans)
    serverName = 'BoMainApp'
    _skt = QLocalSocket()
    _skt.connectToServer(serverName)
    if _skt.waitForConnected(500):
        win32api.MessageBox(0, f"程序已经启动一个实例", "提示！", 48)
        _app.quit()
        sys.exit(sys.argv[0])
    _skt.close()
    _skt = QLocalServer()
    _skt.listen(serverName)
    _app.setWindowIcon(QIcon("images/icon.ico"))
    # 创建一个主窗口
    mainWin = DemoWin()
    # 显示
    mainWin.show()
    _app.exec_()
    _app.exit(0)
except Exception as e:
    win32api.MessageBox(0, f"程序启动失败：\tError MSG:{e}", "错误！", 48)
    sys.exit(sys.argv[0])
