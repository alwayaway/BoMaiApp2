# -*- coding: utf-8 -*-
import sys
import re
import win32api
import pyperclip

from PySide2.QtGui import QIcon
from PySide2.QtNetwork import QLocalServer, QLocalSocket
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QTableWidgetItem
from PySide2.QtCore import QFile, QIODevice, QObject, QTimer, QTranslator, QUrl, Qt, Signal
from PySide2.QtMultimedia import QMediaPlayer

from toolbase import *
from toolbase.my_dlg import DlgMSG
from toolbase.my_ymal import Yml
from COSMO.ScanToText import TcpClient, paste


class DivSignal(QObject):
    recv = Signal(dict)


log = Log(base_path('log'), 'message')
cfg = Cfgdbase(base_path("config/setup.cfg"))
img = Img(base_path("config/img.db"))
ini = Cfgfile(base_path('config/setup.ini'))
pfl = Pro_file()
cpl = Pro_file()
mbx = DlgMSG()
sgl = DivSignal()

__APP__ = "扫描助手"
__VERSION__ = "V1.0.0"

try:
    yml = Yml('config/conf.yaml')
except Exception as _err:
    log.error(f'yaml cfg init err:{_err}')
    yml = {}


def UiLoader(ui_file_name, parent=None):
    ui_file = QFile(ui_file_name)
    if not ui_file.open(QIODevice.ReadOnly):
        raise FileNotFoundError(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
    loader = QUiLoader()
    ui = loader.load(ui_file, parent)
    ui_file.close()
    if not ui:
        raise AttributeError(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
    return ui


class Player:
    def __init__(self):
        self.player = QMediaPlayer()

        self.sound_d = {
            True: QUrl.fromLocalFile('config/OK.wav'),
            False: QUrl.fromLocalFile('config/NG.wav'),
        }

        # self.play(True)

    def play(self, key):
        sound = self.sound_d.get(key)
        self.player.setMedia(sound)
        self.player.play()


player = Player()


class StartApp:
    def __init__(self):
        self.main = AreaUi()
        self._later = QTimer()
        self._later.timeout.connect(lambda *x: self.after_load())
        self._later.start(500)
        self.player = QMediaPlayer()
        self.sound_d = {}
        self.server = TcpClient(yml.get('HOST', "192.168.1.125"), yml.get('PORT', 8080))
        self.server.timeout(yml.get('TIMEOUT', 100) / 1000)
        self.area = re.compile(yml.get('RE_AREA_XY', '([0-9])\\+([0-9])\\+(.*?)$'))
        self.server.recv_func = self.recv
        self.running = True

    def load(self):
        pass

    def after_load(self):
        """启动后加载事件"""
        self._later.stop()
        try:
            self.server.connect()
        except Exception as __init__error:
            log.error(f"init__error{__init__error}")
            mbx.warning('错误', f"{__init__error}", self.main.ui)

    def recv(self, data: str):
        area = {}
        for da in data.split('\n'):
            re_area = re.match(self.area, da)
            if re_area:
                _x, _y, _d = re_area.groups()
                area[_x + _y] = _d.strip()
            else:
                continue
        getattr(sgl.recv, "emit")(area)

    def run(self):
        self.load()
        self.main.show()

    def end(self):
        self.running = False
        self.server.close()
        self.main.items.clear()
        self.main.clock.stop()
        self.player.deleteLater()


class AreaUi:
    def __init__(self):
        self.ui = UiLoader('uic/AreaUi.ui')
        self.ui.setWindowIcon(QIcon(base_path('config/pt.ico')))
        # self.ui.setWindowFlags(Qt.WindowCloseButtonHint)
        self.ui.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.ui.setWindowTitle(f"{__APP__} {__VERSION__}")

        self.areaSet = {
            k: getattr(self.ui, f'lb_area_{k}') for k in ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J')
        }
        self.areaXY = yml.get('Area', {
            'AA': '11', 'AB': '12', 'BA': '13', 'BB': '14', 'CA': '15',
            'CB': '31', 'DA': '32', 'DB': '33', 'EA': '34', 'EB': '35',
            'FA': '21', 'FB': '22', 'GA': '23', 'GB': '24', 'HA': '25',
            'HB': '41', 'IA': '42', 'IB': '43', 'JA': '44', 'JB': '45'
        })

        self.ui_attr('cLB_area_cfg').hide()

        self.check_d = {
            "A": {"len": 0, "re": re.compile('.*?$')},
            "B": {"len": 0, "re": re.compile('.*?$')},
        }

        self.clock = QTimer()
        self.clock.timeout.connect(lambda *x: self.clock.stop())
        self.items, self.pasting = [], False

        self.rule_name = yml.get('RE_RULE_NAME', '默认配置')
        self.rule: dict = ...

    def change_rule(self):
        self.ui_attr('cLB_change_re').setText(f'【点击切换】>>当前使用配置：{self.rule_name}')
        self.rule = eval(
            cfg.get('@U_rule', self.rule_name, '{"lenA": 0, "reA": "^[A-Z0-9]+$", "lenB": 0, "reB": "^[A-Z0-9]+$"}')
        )
        rule = self.rule
        self.check_d = {
            "A": {"len": int(rule.get("lenA")), "re": re.compile(rule.get("reA"))},
            "B": {"len": int(rule.get("lenB")), "re": re.compile(rule.get("reB"))},
        }

    def cl_change_rule(self):
        rules = cfg.getOpts('@U_rule')
        rules_name = list(rules.keys())
        name, ok = mbx.getItem('切换配置', '请选择要使用的配置', self.ui, rules_name, rules_name.index(self.rule_name))
        if name and ok:
            self.rule_name = name
            yml.set('RE_RULE_NAME', name)
            self.change_rule()

    def ui_attr(self, attr):
        return getattr(self.ui, attr)

    def show(self):
        self.setCmd()
        self.load()
        self.ui.show()

    def load(self):
        self.change_rule()

    def setCmd(self):
        getattr(sgl.recv, "connect")(self.recv)
        self.ui_attr('cLB_change_re').clicked.connect(self.cl_change_rule)
        self.ui_attr('cLB_config_set').clicked.connect(CfgSet)

    @staticmethod
    def check_err_msg(v):
        return f'<p align="center"><span style=" font-size:12pt; font-weight:600; color:#ffff00;">{v}</span></p>'

    @staticmethod
    def check_ok_msg(v):
        return f'<p align="center"><span style=" font-size:12pt; font-weight:600; color:#0000ff;">{v}</span></p>'

    def re_check(self, key, aString: str):
        if not aString or aString == yml.get('NG', 'NoRead'):
            return False, self.check_err_msg(f'{key}码采集异常')

        rule = self.check_d.get(key)

        if 0 < rule.get('len') != len(aString):
            return False, self.check_err_msg(f'{key}码长度异常')
        tmp = re.match(rule.get('re'), aString)
        if tmp and tmp.group() == aString:
            return True, self.check_ok_msg(f'{key}码采集成功')
        else:
            return False, self.check_err_msg(f'{key}码匹配异常')

    def sleep(self, t):
        self.clock.start(t)
        while self.clock.isActive():
            app.processEvents()

    def recv(self, data: dict):
        items, up = [], True
        if len(data) < 20:
            up = False
        for _k, _w in self.areaSet.items():
            vA = data.get(self.areaXY.get(f"{_k}A"))
            vB = data.get(self.areaXY.get(f"{_k}B"))
            cA, mA = self.re_check('A', vA)
            cB, mB = self.re_check('B', vB)
            items.append([vA, vB])
            if cA and cB:
                getattr(_w, 'setStyleSheet')(u"background-color: rgb(0, 210, 0);")
            else:
                up = False
                getattr(_w, 'setStyleSheet')(u"background-color: rgb(255, 0, 0);")
            getattr(_w, 'setText')(mA + mB)

        # pfl.add(up)
        player.play(up)

        if up:
            self.items.extend(items)
            self.cp_ps() if not self.pasting else None

    def cp_ps(self):
        self.pasting = True
        while self.items:
            item = self.items.pop(0)
            for idx, d in enumerate(item):
                if idx > 0:
                    self.sleep(yml.get('MS_BOX_IN', 100))
                pyperclip.copy(d)
                paste()
            self.sleep(yml.get('MS_BOX_OUT', 300))
        self.pasting = False


class CfgSet:
    def __init__(self):
        self.ui = UiLoader('uic/CfgSet.ui')
        self.ui.setWindowIcon(QIcon(base_path('config/pt.ico')))
        self.ui.setWindowFlags(Qt.WindowCloseButtonHint)
        self.ui.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.ui.setWindowTitle("设置")

        self.rule_name = yml.get('RE_RULE_NAME', '默认配置')
        self.rule = {}

        self.run()

    def ui_attr(self, attr):
        return getattr(self.ui, attr)

    def load(self):
        self.ui_attr('sB_box_in').setValue(yml.get('MS_BOX_IN', 100))
        self.ui_attr('sB_box_out').setValue(yml.get('MS_BOX_OUT', 300))
        self.ui_attr('lE_tcp_host').setText(yml.get('HOST', '192.168.1.125'))
        self.ui_attr('sB_tcp_port').setValue(yml.get('PORT', 8080))

        self.load_rules()
        self.change_rule()

    def setCmd(self):
        self.ui_attr('cLK_tcp_conn').clicked.connect(self.tcp_conn)
        self.ui_attr('cLK_save').clicked.connect(self.save)
        self.ui_attr('pB_re_add').clicked.connect(self.add_rule)
        self.ui_attr('pB_re_save').clicked.connect(self.sav_rule)
        self.ui_attr('pB_re_del').clicked.connect(self.del_rule)
        self.ui_attr('tW_rule').doubleClicked.connect(self.db_change_rule)

    def save(self):
        yml['MS_BOX_IN'] = self.ui_attr('sB_box_in').value()
        yml['MS_BOX_OUT'] = self.ui_attr('sB_box_out').value()
        yml['HOST'] = self.ui_attr('lE_tcp_host').text()
        yml.set('PORT', self.ui_attr('sB_tcp_port').value())
        mbx.information('提示', '\t保存成功\t\t', self.ui)

    def load_rules(self):
        rules = cfg.getOpts('@U_rule')
        self.ui_attr('tW_rule').setRowCount(0)
        for row, tit in enumerate(rules.keys()):
            self.ui_attr('tW_rule').insertRow(row)
            self.ui_attr('tW_rule').setItem(row, 0, QTableWidgetItem(f'{tit}'))

    def change_rule(self):
        self.ui_attr('lb_rule_name').setText(self.rule_name)
        self.rule: dict = eval(cfg.get('@U_rule', self.rule_name, '{}', False))
        self.ui_attr('sB_len_A').setValue(self.rule.get('lenA', 0))
        self.ui_attr('sB_len_B').setValue(self.rule.get('lenB', 0))
        self.ui_attr('lE_re_A').setText(self.rule.get('reA', ''))
        self.ui_attr('lE_re_B').setText(self.rule.get('reB', ''))

    def tcp_conn(self):
        host = self.ui_attr('lE_tcp_host').text()
        port = self.ui_attr('sB_tcp_port').value()
        try:
            app_run.server.connect(host, port)
            mbx.information('提示', '\t连接成功\t', self.ui)
        except Exception as _tcp_re_conn_err:
            log.error(_tcp_re_conn_err)
            mbx.warning('提示', f'连接失败: {_tcp_re_conn_err}', self.ui)

    def db_change_rule(self, idx):
        self.rule_name = self.ui_attr('tW_rule').item(idx.row(), idx.column()).text()
        self.change_rule()

    def add_rule(self):
        name, ok = mbx.getStr('名称', '请输入保存的规则名称！', self.ui)
        if name and ok:
            rule = {
                "lenA": self.ui_attr('sB_len_A').value(),
                "reA": self.ui_attr('lE_re_A').text(),
                "lenB": self.ui_attr('sB_len_B').value(),
                "reB": self.ui_attr('lE_re_B').text(),
            }
            cfg.set('@U_rule', name, str(rule))
            self.rule_name = name
            self.load_rules()
            self.change_rule()
            mbx.information('提示', f'新增校验规则: {name} 成功!', self.ui)

    def del_rule(self):
        if self.rule_name == yml.get('RE_RULE_NAME', '默认配置'):
            mbx.warning('警告', f'校验规则: {self.rule_name} 正在使用， 不可删除!', self.ui)
            return
        cfg.remove('@U_rule', self.rule_name)
        self.rule_name = ''
        self.load_rules()
        self.change_rule()
        mbx.information('提示', f'校验规则: {self.rule_name} 删除成功!', self.ui)

    def sav_rule(self):
        rule = {
            "lenA": self.ui_attr('sB_len_A').value(),
            "reA": self.ui_attr('lE_re_A').text(),
            "lenB": self.ui_attr('sB_len_B').value(),
            "reB": self.ui_attr('lE_re_B').text(),
        }
        cfg.set('@U_rule', self.rule_name, str(rule))
        mbx.information('提示', f'校验规则: {self.rule_name} 修改成功!', self.ui)

    def run(self):
        self.setCmd()
        self.load()
        self.ui_attr('exec')()
        self.ui.deleteLater()


try:
    try:
        app = QApplication()
    except RuntimeError:
        app = QApplication.instance()
    app.setStyle('Fusion')
    # noinspection PyArgumentList
    translator = QTranslator()
    # noinspection PyArgumentList
    translator.load('qml/qt_zh_CN.qm')
    app.installTranslator(translator)
    serverName = 'ScanService'
    _skt = QLocalSocket()
    _skt.connectToServer(serverName)
    if _skt.waitForConnected(500):
        win32api.MessageBox(0, f"程序已经启动一个实例", "提示！", 48)
        app.quit()
        sys.exit(sys.argv[0])
    _skt.close()
    _skt = QLocalServer()
    _skt.listen(serverName)
    app_run = StartApp()
except AttributeError as _attr_err:
    log.error(_attr_err)
    win32api.MessageBox(0, f"程序启动失败：\tError MSG: Ui组件损坏， 请联系管理员修复！", "错误！", 48)
    sys.exit(sys.argv[0])
except Exception as e:
    log.error(e)
    win32api.MessageBox(0, f"程序启动失败：\tError MSG:{e}", "错误！", 48)
    # sys.exit(sys.argv[0])
    raise e

try:
    app_run.run()
    app.exec_()
    app_run.end()
except Exception as _e:
    # print(_e)
    app_run.end()
finally:
    _skt.close()
    sys.exit(0)
