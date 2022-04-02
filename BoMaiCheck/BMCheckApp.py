import yaml
from BoMaiCheck.toolbase import *
from BoMaiCheck.toolbase.my_dlg import *
from BoMaiCheck.ui import *
from BoMaiCheck._db import *
from BTSDK.btSdk import Bartender

from PySide2.QtCore import QByteArray, Qt, QTranslator, Signal, QObject
from PySide2.QtNetwork import QLocalSocket, QLocalServer
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtMultimedia import QMediaPlayer, QMediaContent
from threading import Thread


class DivSignal(QObject):
    show_sig = Signal(str)
    set_norm = Signal(str)
    change_tw = Signal(str, int)
    add_box_item = Signal(list)
    show_crr = Signal(str)
    btw_init_msg = Signal(str)


log = Log('log', 'runstate')
cfg = Cfgdbase("config/setup.cfg")
img = Img("config/ImgBase")
pfl = Pro_file()
dbs = DataBase('config/DataBase.db')
div = DivSignal()
mbx = Dlg_MSG()

try:
    with open('config/conf.yaml', encoding='utf-8')as _sql:
        yml = yaml.load(_sql, yaml.CLoader)
except Exception as _err:
    log.error(f'yaml cfg init err:{_err}')
    yml = {}


class Mdb:
    def __init__(self):
        self._mssql = MSSQL(yml.get('HOST'), yml.get('USER'), yml.get('PWD'), yml.get('DB'))

    def __enter__(self):
        return self._mssql

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._mssql.close()


# noinspection PyArgumentList
def get_b64image(_img64):
    """
    加载base64 图片
    :param _img64:
    :return: PySide2.QtGui.QPixmap.QPixmap
    """
    _ = QPixmap()
    _.loadFromData(QByteArray.fromBase64(_img64))
    return _


class Ser_Port(Ser):
    def __init__(self):
        super().__init__()
        self.func_ = None

    def connect(self, port=None, baudrate=None, bytesize=None, parity=None, stopbits=None, **kwargs):
        port = port if port else cfg.get(f'ser_port', "port", '')
        port = port if port else None
        baudrate = baudrate if baudrate else int(cfg.get(f'ser_port', "baudrate", '9600'))
        bytesize = bytesize if bytesize else int(cfg.get(f'ser_port', "bytesize", '8'))
        parity = parity if parity else get_paritys_dict().get(cfg.get(f'ser_port', "parity", "None"))
        stopbits = stopbits if stopbits else str2num(cfg.get(f'ser_port', "stopbits", '1'))
        timeout = int(cfg.get(f'ser_port', "timeout", '100')) / 1000
        try:
            self.open(port, baudrate, bytesize, parity, stopbits, timeout=timeout, **kwargs)
        except Exception as ser_err:
            mbx.warning('警告', f'端口打开失败: {ser_err}', Main.app.ui)
            return

        if self.func_ and self.isOpen():
            name = f'ser_port_thread'
            Thread(
                target=self.read_theard,
                args=(self.func_, ),
                daemon=True,
                name=name
            ).start()


class StartApp:
    def __init__(self):
        self.running = True
        self.num_err = 0
        self.app = _App()
        self.check = Check()
        self.ser = Ser_Port()

        self._later = QTimer()
        self._later.timeout.connect(lambda *x: self.after_load())
        self._later.start(500)
        self.player = QMediaPlayer()
        self.sound_d = {}

    def load(self):
        div.show_crr.connect(self.msg)
        self.ser.func_ = self.ser_recv
        Thread(target=self.play_sound, daemon=True).start()

    # noinspection PyArgumentList
    def after_load(self):
        self._later.stop()
        self.ser.connect()

    def stop(self):
        self.running = False
        dbs.close()
        img.close()
        pfl.close()
        cfg.close()
        self.ser.close()
        self.app.btw.close()
        log.shutdown()

    def run(self):
        self.load()
        self.app.run()

    def ser_recv(self, data):
        # print(data)
        args = data.split(';')
        print(args)
        try:
            self.check.check(*args)
        except CheckError as _crr:
            if f"{_crr}".startswith('数量错误') and self.num_err < 3:
                self.num_err += 1
                time.sleep(0.5)
                # self.ser.write_hex('16 54 0d')
                self.ser.write('RESCAN')
            else:
                self.num_err = 0
                div.show_crr.emit(f"{_crr}")
            return
        div.add_box_item.emit(args)

    def msg(self, _crr):
        pfl.add('NG')
        mbx.warning('提示', _crr, self.app.ui)

    # noinspection PyCallByClass,PyArgumentList
    def play_sound(self):
        self.sound_d = {
            "OK": QMediaContent(QUrl.fromLocalFile('config/OK2.wav')),
            "NG": QMediaContent(QUrl.fromLocalFile('config/NG.wav')),
        }

        while self.running:
            try:
                sound = self.sound_d.get(pfl.pop())
                self.player.setMedia(sound)
                self.player.play()
            except IndexError:
                time.sleep(0.1)
                continue


class _App:
    def __init__(self):
        self.ui = MainUI()
        self.ui.setWindowTitle('博迈出库校验系统V2.0')
        # noinspection PyArgumentList
        self.ui.setWindowIcon(QIcon(get_b64image(img.get('检测'))))

        show_tit = {
            '产品名称': 160, '订单号': 100,
            '批次': 100, '出货数量': 70,
            '装箱数量': 70,
        }
        self.show_tit = show_tit

        self.ui.tW_show_code.setColumnCount(len(show_tit))
        self.ui.tW_show_code.setHorizontalHeaderLabels(list(show_tit.keys()))
        self.ui.tW_show_code.verticalHeader().setVisible(False)
        self.ui.tW_show_code.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tW_show_code.horizontalHeader().setStretchLastSection(True)

        widths = list(show_tit.values())
        for col, wdt in zip(range(len(widths)), widths):
            self.ui.tW_show_code.setColumnWidth(col, wdt)

        self.check_lots = {}
        self.fhd_code = cfg.get('check', 'code', '')
        self.box_code = None
        self.box_item = {}

        self.box_size = cfg.get('zx', 'size', '')
        self.box_numb = int(cfg.get('zx', 'numb', 0))

        self.btw = BtwEngine()

        self.btwPtList = []

    def run(self):
        self.set_cmd()
        self.load()
        self.ui.show()

    def load(self):
        # Thread(target=self.load_btw_thread, daemon=True).start()
        Thread(target=self.load_btw_thread).start()
        self.ui.lW_show_sacn.setColumnWidth(0, 160)
        self.ui.lW_show_boxs.setColumnWidth(0, 160)
        self.ui.sB_box_num.setValue(self.box_numb)
        self.ui.lE_box_size.setText(self.box_size)

        self.ui.pB_data_serch.hide()

        self.load_data()

    def load_btw_thread(self):
        try:
            self.btw.load_btw_engine()
        except Exception as btw_init_err:
            btw_init_err_str = f'打印引擎加载失败!\n{btw_init_err}'
            log.error(btw_init_err_str)
            div.btw_init_msg.emit(btw_init_err_str)

        if self.btw.engined():
            while Main.running:
                if self.btwPtList:
                    _pt: dict = self.btwPtList.pop(0)
                    log.info(f"{_pt}: {_pt.get('printer')(_pt.get('data', {}))}")
                else:
                    time.sleep(0.1)

    def load_btw(self, btw_init_err):
        mbx.critical('错误', btw_init_err, self.ui)
        self.ui.close()

    def set_cmd(self):
        self.ui.pB_data_serch.clicked.connect(Data_His)
        self.ui.pB_port_set.clicked.connect(Port_Set)
        self.ui.pB_rule_set.clicked.connect(Rule_Set)
        self.ui.pB_btw_set.clicked.connect(BtwSetDialog)
        self.ui.lE_code_chose.returnPressed.connect(
            lambda *x: self.load_data(self.ui.lE_code_chose.text())
        )
        div.change_tw.connect(self.change_tw)
        self.ui.lE_scan_lot.returnPressed.connect(self.check)
        self.ui.cLB_box.clicked.connect(self.box_in)
        div.add_box_item.connect(self.ser_add_box_item)

        self.ui.tB_box_num.clicked.connect(lambda *x: self.up_box_numb())
        self.ui.tB_box_size.clicked.connect(lambda *x: self.up_box_size())

        self.ui.sB_box_num.focusOutEvent = self.re_box_numb_show()
        self.ui.lE_box_size.focusOutEvent = self.re_box_size_show()

        self.ui.lW_show_boxs.contextMenuEvent = self.context_menu_event_show_box
        self.ui.lW_show_boxs.doubleClicked.connect(self.doubleclick_show_box)

        div.btw_init_msg.connect(self.load_btw)

    def doubleclick_show_box(self, item):
        row = item.row()
        box_code = self.ui.lW_show_boxs.item(item.row(), 0).text()
        if int(self.ui.lW_show_boxs.item(row, 1).text()) < self.box_numb:
            self.re_load_box_item(box_code)
        else:
            mbx.warning('提示', f"箱号为： {box_code} 的外箱 已经装满， 不可继续装箱！", self.ui)

    # noinspection PyArgumentList
    def context_menu_event_show_box(self, event):
        tw = self.ui.lW_show_boxs
        if tw.rowCount() <= 0:
            return

        row = tw.currentRow()
        box_code = tw.item(row, 0).text()

        menu = QMenu(self.ui)

        exp1 = menu.addAction("继续装箱") if int(tw.item(row, 1).text()) < self.box_numb else ...
        exp2 = menu.addAction("外箱补打")
        lots = {}
        for item in dbs.get_box_items(self.fhd_code, box_code):
            lot = item[0]
            lots[menu.addAction(f"批次补打: {lot}")] = lot

        action = menu.exec_(tw.mapToGlobal(event.pos()))

        if action == exp1:
            self.re_load_box_item(box_code)
        elif action == exp2:
            self.btw.print_wx(dbs.get_print_data_wx(self.fhd_code, box_code))
        elif action in lots:
            self.btw.print_mx(dbs.get_print_data_mx(
                    yml.get('DATA_FOR_BOX_ITEM'),
                    self.fhd_code, box_code, lots.get(action)
                )
            )
        else:
            return

    def re_load_box_item(self, box_code):
        self.box_code = box_code
        for da in dbs.get_box_items(self.fhd_code, box_code):
            self.box_item[da[0]] = da[1]
        self.ui.lW_show_sacn.setRowCount(0)
        for k in self.box_item.keys():
            self.up_scan_show(k)

    def re_box_numb_show(self):
        focusOutEvent = self.ui.sB_box_num.focusOutEvent

        def _focusOutEvent(event):
            focusOutEvent(event)
            st = time.time()
            while self.ui.sB_box_num.value() != self.box_numb:
                _app.processEvents()
                if time.time() - st > 0.5:
                    break
            self.ui.sB_box_num.setValue(self.box_numb)

        return _focusOutEvent

    def re_box_size_show(self):
        focusOutEvent = self.ui.lE_box_size.focusOutEvent

        def _focusOutEvent(event):
            focusOutEvent(event)
            st = time.time()
            while self.ui.lE_box_size.text() != self.box_size:
                _app.processEvents()
                if time.time() - st > 0.5:
                    break
            self.ui.lE_box_size.setText(self.box_size)

        return _focusOutEvent

    def up_box_numb(self):
        self.box_numb = self.ui.sB_box_num.value()
        cfg.set('zx', 'numb', self.box_numb)
        mbx.information('提示', f'更新装箱数成功： 当前装箱数为：{self.box_numb}', self.ui)

    def up_box_size(self):
        self.box_size = self.ui.lE_box_size.text()
        cfg.set('zx', 'size', self.box_size)
        mbx.information('提示', f'更新装箱尺寸成功： 当前装箱装箱尺寸为：{self.box_size}', self.ui)

    def load_data(self, codes=''):
        self.ui.lE_scan_lot.setFocus()
        code = None
        for _it in codes.split('@@'):
            if _it.startswith('SD.'):
                code = _it[3:]
                break
        if not code and codes:
            code = codes
        if code:
            auto = False
            if not dbs.is_full_checked(self.fhd_code):
                msg_box = QMessageBox(
                    QMessageBox.Question, '提示',
                    f"发货单{self.fhd_code}未全部校验，确定更换发货单码？",
                    parent=self.ui
                )
                # noinspection PyTypeChecker
                msg_box.addButton(self.ui.tr("确定"), QMessageBox.YesRole)
                # noinspection PyTypeChecker
                msg_box.addButton(self.ui.tr("取消"), QMessageBox.NoRole)
                msg_box.exec_()
                if msg_box.result() != 0:
                    return
        else:
            auto = True
            code = self.fhd_code

        # 读取本地发货单数据
        title = dbs.get_code_tit(code)
        MS_LOAD = True
        if title and title.get():
            MS_LOAD = False
            if not auto:
                if mbx.question(
                        '提示', f'发货单号：{code}在本地已存在， 是否从服务器重新更新？更新将重置当前已装箱数据',
                        parent=self.ui
                ).result() == 0:
                    if mbx.question('警告', '更新将重置当前已装箱数据？请再次确定！', parent=self.ui).result() == 0:
                        with Mdb() as ms:
                            transaction = ms.exec_with_transaction()
                            result = True
                            for ZX_COED_SET in [_[0] for _ in dbs.get_ZXDH_set(code)]:
                                result1 = transaction.exec_sql(yml.get('SQL_RE_BOX_DATA'), ZX_COED_SET)
                                result2 = transaction.exec_sql(yml.get('SQL_RE_BOX_ITEM'), ZX_COED_SET)
                                result = result1 and result1
                                if not result:
                                    break
                            if result:
                                transaction.commit()
                                delZx1, delZx2 = dbs.del_ZXDH_item(code)
                                if delZx1 and delZx2:
                                    log.info(f'重置发货单{code} 成功！')
                                    MS_LOAD = True
                                else:
                                    err_msg = delZx1.error() if not delZx1 else ''
                                    err_msg += delZx2.error() if not delZx2 else ''
                                    log.info(f'重置发货单{code} 失败!')
                                    log.error(f'重置发货单{code} 失败: \n\t{delZx1}\n\t{delZx2}')
                                    log.error(f'重置发货单{code} 失败: {err_msg}')
                                    mbx.warning('失败！', f"重置发货单{code} 失败:{err_msg}", self.ui)
                                    return
                            else:
                                transaction.rollback()
                                mbx.warning('失败！', f"服务端重置发货单{code} 失败:\n{result1.error()}\n"
                                                   f"{result2.error()}", self.ui)
                                return
            self.ui.lE_code_chose.setText(title[0][0])
            self.ui.lE_show_adr.setText(title[0][1])
            self.ui.lE_show_date.setText(title[0][2])
            cfg.set('check', 'code', code)
            self.fhd_code = code
        elif auto:
            return
        elif title:
            pass
        else:
            log.error(f"表头查询错误:{title.error()}\n{title}")
            return
        if MS_LOAD:
            # 读取服务端发货单数据
            with Mdb() as ms:
                data = ms.exec_query_dict(yml.get('SQL_GET_FH_DATA'), code)
            if data:
                if data.value:
                    log.info(f"从服务器加载发货单{code}成功：{data.value}")
                    res = dbs.add_codes(data)
                    if not res:
                        log.info(f"从服务器加载发货单{code}到本地失败：{res.error()}")
                        log.error(f"从服务器加载发货单{code}到本地失败：{res}")
                        log.error(f"从服务器加载发货单{code}到本地错误：{res.error()}")
                        mbx.warning('失败！', f"从服务器加载发货单{code}到本地失败：{res.error()}", self.ui)
                        return
                else:
                    mbx.warning('失败！', f"从服务器加载发货单{code}到本地失败：服务器无当前发货单数据", self.ui)
                    return
            else:
                log.info(f"从服务器加载发货单{code}失败：{data}")
                log.error(f"从服务器加载发货单{code}失败：{data}")
                log.error(f"从服务器加载发货单{code}错误：{data.error()}")
                mbx.warning('失败！', f"从服务器加载发货单{code}错误：{data}", self.ui)
                return

        data = dbs.get_code_data(code)
        if data:
            self.ui.tW_show_code.setRowCount(0)
            row = 0
            for d in data:
                self.ui.tW_show_code.insertRow(row)

                self.check_lots[d[2]] = (d[3], d[4], row)

                if d[4] == 0:
                    # noinspection PyArgumentList
                    color = QColor(0, 0, 200)   # 蓝色
                elif d[3] == d[4]:
                    # noinspection PyArgumentList
                    color = QColor(0, 200, 0)   # 绿色
                else:
                    # noinspection PyArgumentList
                    color = QColor(255, 140, 0)     # 黄色

                col = 0
                for c in d:
                    # noinspection PyArgumentList
                    _qti = QTableWidgetItem(f'{c}')
                    _qti.setTextColor(color)
                    self.ui.tW_show_code.setItem(row, col, _qti)
                    col += 1
                row += 1

            self.clean_box()
            self.load_box_code(code)

    def load_box_code(self, code):
        self.ui.lW_show_boxs.setRowCount(0)

        box_code = dbs.get_box_codes(code)
        if box_code:
            for row, item in enumerate(box_code):
                self.ui.lW_show_boxs.insertRow(row)
                for col, val in enumerate(item):
                    # noinspection PyArgumentList
                    self.ui.lW_show_boxs.setItem(row, col, QTableWidgetItem(str(val)))
        else:
            log.error(f'加载发货单{code}已经装箱数据失败: {box_code}')
            log.error(f'加载发货单{code}已经装箱数据失败: {box_code.error()}')
            mbx.warning('失败！', f"加载发货单{code}已经装箱数据失败:{box_code.error()}", self.ui)
            return

    def change_tw(self, lot: str, num: int):
        s_num, c_num, row = self.check_lots.get(lot)
        cols = len(self.show_tit)
        c_num += num
        if self.box_code is None:
            self.box_code = get_ZX_code()
            with Mdb() as ms:
                _XS = dbs.get_XS_code(self.fhd_code)[0][0]
                w2ms_SQL_ADD_ZX_DATA = ms.exec_sql(yml.get('SQL_ADD_ZX_DATA'), self.box_code, self.box_size, _XS, _XS)
            if w2ms_SQL_ADD_ZX_DATA:
                dbs.up_zx_num(num, self.box_code, lot)
            else:
                self.box_code = None
                log.error(f'更新服务器装箱单{self.fhd_code}失败！{w2ms_SQL_ADD_ZX_DATA}')
                log.error(f'更新服务器装箱单失败！{w2ms_SQL_ADD_ZX_DATA.error()}')
                mbx.warning('失败！', f'更新服务器装箱单{self.fhd_code}失败！{w2ms_SQL_ADD_ZX_DATA}', self.ui)
                return

        _res = dbs.up_code_num(self.fhd_code, lot, c_num)
        if _res:
            if s_num == c_num:
                # noinspection PyArgumentList
                color = QColor(0, 200, 0)
            else:
                # noinspection PyArgumentList
                color = QColor(255, 140, 0)
            self.ui.tW_show_code.item(row, 4).setText(f"{c_num}")
            for col in range(cols):
                self.ui.tW_show_code.item(row, col).setTextColor(color)
            with Mdb() as ms:
                if lot in self.box_item:
                    self.box_item[lot] += num
                    w2ms = ms.exec_sql(yml.get('SQL_UP_ZX_NUM'), num, self.box_code, lot)
                    if w2ms:
                        dbs.up_zx_num(num, self.box_code, lot)
                    else:
                        log.error(f'更新服务器装箱单{self.fhd_code}失败！{w2ms}')
                        log.error(f'更新服务器装箱单失败！{w2ms.error()}')
                        mbx.warning('失败！', f'更新服务器装箱单{self.fhd_code}失败！{w2ms}', self.ui)
                        return
                else:
                    self.box_item[lot] = num
                    _cp_data = dbs.get_zxd_item(self.fhd_code, lot)[0]
                    w2ms = ms.exec_sql(yml.get('SQL_ADD_ZX_ITEM'), self.box_code, self.box_code, *_cp_data, num)
                    if w2ms:
                        dbs.ct_zx_num(
                            self.fhd_code,
                            ms.exec_query_dict(yml.get('SQL_GET_ZX_DATA'), self.box_code, lot)[0]
                        )
                    else:
                        log.error(f'新增服务器装箱单失败！{w2ms}')
                        log.error(f'新增服务器装箱单失败！{w2ms.error()}')
                        mbx.warning('失败！', f'新增服务器装箱单失败！{w2ms}', self.ui)
                        return
        else:
            log.error(f'更新校验结果失败！:{_res.error()}')
            log.error(f'执行语句失败！:{_res}')
            msg_box = QMessageBox(QMessageBox.Critical, '警告',
                                  f"更新校验数据发送未知错误，请联系管理员进行维护！\n"
                                  f"错误代码：{_res.error()}",
                                  parent=self.ui)
            # noinspection PyTypeChecker
            msg_box.addButton(self.ui.tr("我知道了"), QMessageBox.YesRole)
            msg_box.exec_()
            return
        self.check_lots[lot] = (s_num, c_num, row)
        self.up_scan_show(lot)
        self.ui.update()

    def check(self):
        """手动USB扫描单个"""
        try:
            bar = self.ui.lE_scan_lot.text()
            Main.check.check(bar, UI=True)
            self.add_box_item(bar)
        except CheckError as _crr:
            div.show_crr.emit(f"{_crr}")
        self.ui.lE_scan_lot.clear()

    def check_full(self, data: dict):
        extra = []
        for lot, num in data.items():
            s_num, c_num, _ = self.check_lots.get(lot)
            check_num = s_num - c_num - num
            if check_num < 0:
                extra.append(lot)
        return extra

    def ser_add_box_item(self, data: list):
        """串口扫描校验成功后任务"""
        self.add_box_item(*data)

    def add_box_item(self, *args):
        """扫描校验成功后任务"""
        pfl.add('OK')
        log.info(f"SCAN DATA: {', '.join(args)}")
        # self.ui.ldN_num.display(sum(self.box_item.values()))

        if 0 < self.box_numb <= self.ui.ldN_num.value():
            self.box_print()
            self.clean_box()

    def up_box_code_show(self):
        box_code_ = f'<p><span style=" font-size:11pt; font-weight:600; color:#0055ff;">' \
                    f'{self.box_code if self.box_code else "..."}' \
                    f'</span></p>'
        self.ui.lb_show_box_code.setText(box_code_)

    def up_scan_show(self, lot):
        crt = True
        rows = self.ui.lW_show_sacn.rowCount()
        for row in range(rows):
            if self.ui.lW_show_sacn.item(row, 0).text() == lot:
                crt = False
                self.ui.lW_show_sacn.item(row, 1).setText(str(self.box_item.get(lot)))
                break
        if crt:
            self.ui.lW_show_sacn.insertRow(rows)
            # noinspection PyArgumentList
            self.ui.lW_show_sacn.setItem(rows, 0, QTableWidgetItem(str(lot)))
            # noinspection PyArgumentList
            self.ui.lW_show_sacn.setItem(rows, 1, QTableWidgetItem(str(self.box_item.get(lot, 0))))
        self.ui.ldN_num.display(sum(self.box_item.values()))
        self.up_box_code_show()

    def box_in(self):
        if self.box_code is None:
            msg_box = QMessageBox(QMessageBox.Warning, '警告', f"当前无装箱产品数据", parent=self.ui)
            # noinspection PyTypeChecker
            msg_box.addButton(self.ui.tr("我知道了"), QMessageBox.YesRole)
            msg_box.exec_()
            return
        self.box_print()
        self.clean_box()

    def clean_box(self):
        self.box_code = None
        self.box_item = {}
        self.ui.lW_show_sacn.setRowCount(0)
        self.ui.ldN_num.display(0)
        self.up_box_code_show()

    def box_print(self):
        self.load_box_code(self.fhd_code)
        if yml.get('BOX_PT_WX') is True:
            self.btwPtList.append({
                'printer': self.btw.print_wx,
                'data': dbs.get_print_data_wx(self.fhd_code, self.box_code)
            })
        if yml.get('BOX_PT_NX') is True:
            for lot in self.box_item.keys():
                self.btwPtList.append({
                    'printer': self.btw.print_mx,
                    'data': dbs.get_print_data_mx(yml.get('DATA_FOR_BOX_ITEM'), self.fhd_code, self.box_code, lot)
                })


class BtwSetDialog:
    def __init__(self):
        self.ui = BtwSet()
        self.ui.setWindowTitle('模板管理')
        self.ui.setWindowFlags(Qt.WindowCloseButtonHint)
        # noinspection PyArgumentList
        self.ui.setWindowIcon(QIcon(get_b64image(img.get('检测'))))
        self.btw = Main.app.btw
        self.run()

    def load(self):
        # noinspection PyArgumentList
        self.ui.lb_show_wx.setPixmap(QPixmap(self.btw.get_view_wx()))
        # noinspection PyArgumentList
        self.ui.lb_show_nx.setPixmap(QPixmap(self.btw.get_view_mx()))

    def run(self):
        self.set_cmd()
        self.load()
        self.ui.exec_()

    def set_cmd(self):
        self.ui.pB_edit_wx.hide()
        self.ui.pB_edit_nx.hide()
        self.ui.pB_imp_wx.clicked.connect(self.imp_btw_wx)
        self.ui.pB_imp_nx.clicked.connect(self.imp_btw_mx)

    def imp_btw_wx(self):
        file_, type_ = QFileDialog.getOpenFileName(self.ui, "选择模板文件, 导入外箱模板", "C:", "btw Files (*.btw)")
        if not file_:
            return
        self.btw.imp_btw('BOX_OUT_LAB', file_)
        # noinspection PyArgumentList
        self.ui.lb_show_wx.setPixmap(QPixmap(self.btw.get_view_wx()))

    def imp_btw_mx(self):
        file_, type_ = QFileDialog.getOpenFileName(self.ui, "选择模板文件, 导入装箱明细模板", "C:", "btw Files (*.btw)")
        if not file_:
            return
        self.btw.imp_btw('BOX_ITEM_LAB', file_)
        # noinspection PyArgumentList
        self.ui.lb_show_nx.setPixmap(QPixmap(self.btw.get_view_mx()))


class Data_His:
    def __init__(self):
        self.ui = Data_View()
        self.ui.setWindowTitle('数据查询')
        self.ui.setWindowFlags(Qt.WindowCloseButtonHint)
        # noinspection PyArgumentList
        self.ui.setWindowIcon(QIcon(get_b64image(img.get('检测'))))
        self.run()

    def load(self):
        pass

    def run(self):
        self.set_cmd()
        self.load()
        self.ui.exec_()

    def load_box_item(self):
        pass

    def set_cmd(self):
        pass


class Port_Set:
    def __init__(self):
        self.ui = PortSet()
        self.ui.setWindowTitle('端口设置')
        self.ui.setWindowFlags(Qt.WindowCloseButtonHint)
        # noinspection PyArgumentList
        self.ui.setWindowIcon(QIcon(get_b64image(img.get('检测'))))

        self.run()

    def load(self):
        self.ui.cB_port.addItems(get_port_list())
        self.ui.cB_baudrates.addItems(get_baudrates_list())
        self.ui.cB_paritys.addItems(list(get_paritys_dict().keys()))
        self.ui.cB_bytesizes.addItems(get_bytesizes_list())
        self.ui.cB_stopbitses.addItems(get_stopbitses_list())

        self.ui.cB_port.setCurrentText(cfg.get(f'ser_port', "port", ''))
        self.ui.cB_baudrates.setCurrentText(cfg.get(f'ser_port', "baudrate", '9600'))
        self.ui.cB_paritys.setCurrentText(cfg.get(f'ser_port', "parity", "None"))
        self.ui.cB_bytesizes.setCurrentText(cfg.get(f'ser_port', "bytesize", '8'))
        self.ui.cB_stopbitses.setCurrentText(cfg.get(f'ser_port', "stopbits", '1'))

    def run(self):
        self.set_cmd()
        self.load()
        self.switch(True)
        self.ui.exec_()

    def set_cmd(self):
        self.ui.cLB_connect.clicked.connect(self.switch)
        self.ui.cLB_save.clicked.connect(self.save_cfg)

    def switch(self, auto=False):
        if auto:
            pass
        elif Main.ser.isOpen():
            Main.ser.close()
        else:
            port = self.ui.cB_port.currentText()
            bdt = int(self.ui.cB_baudrates.currentText())
            pts = get_paritys_dict().get(self.ui.cB_paritys.currentText())
            bts = int(self.ui.cB_bytesizes.currentText())
            stp = str2num(self.ui.cB_stopbitses.currentText())
            Main.ser.connect(port=port, baudrate=bdt, parity=pts, bytesize=bts, stopbits=stp)

        enable = not Main.ser.isOpen()
        self.ui.cB_port.setEnabled(enable)
        self.ui.cB_baudrates.setEnabled(enable)
        self.ui.cB_paritys.setEnabled(enable)
        self.ui.cB_bytesizes.setEnabled(enable)
        self.ui.cB_stopbitses.setEnabled(enable)
        self.ui.cLB_connect.setIcon(get_b64image(img.get('port_conn' if enable else 'port_conn_close')))
        self.ui.cLB_connect.setText('连接' if enable else '断开')

    def save_cfg(self):
        cfg.set(f'ser_port', "port", self.ui.cB_port.currentText())
        cfg.set(f'ser_port', "baudrate", self.ui.cB_baudrates.currentText())
        cfg.set(f'ser_port', "parity", self.ui.cB_paritys.currentText())
        cfg.set(f'ser_port', "bytesize", self.ui.cB_bytesizes.currentText())
        cfg.set(f'ser_port', "stopbits", self.ui.cB_stopbitses.currentText())
        mbx.information('提示', '保存成功！', self.ui)


class Rule_Set:
    def __init__(self):
        self.ui = RuleSet()
        self.ui.setWindowTitle('规则配置')
        self.ui.setWindowFlags(Qt.WindowCloseButtonHint)
        # noinspection PyArgumentList
        self.ui.setWindowIcon(QIcon(get_b64image(img.get('检测'))))

        mix_tit = ['数据长度', '批次区间', '数量区间', '编辑', '删除']

        self.ui.tW_rule.setColumnCount(5)
        self.ui.tW_rule.setHorizontalHeaderLabels(mix_tit)
        self.ui.tW_rule.verticalHeader().setVisible(False)
        self.ui.tW_rule.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tW_rule.horizontalHeader().setSectionResizeMode(3, QHeaderView.Fixed)
        self.ui.tW_rule.horizontalHeader().setSectionResizeMode(4, QHeaderView.Fixed)
        self.ui.tW_rule.setColumnWidth(3, 40)
        self.ui.tW_rule.setColumnWidth(4, 40)

        self.rules = eval(cfg.get('rule', 'rules', '[]'))
        self.run()

    # noinspection PyArgumentList
    def load(self):
        rows = len(self.rules)
        for row in range(rows):
            col = 0
            self.ui.tW_rule.insertRow(row)
            for c in self.rules[row]:
                self.ui.tW_rule.setItem(row, col, QTableWidgetItem(f'{c}'))
                col += 1
            edit = QPushButton('编辑')
            _del = QPushButton('删除')
            self.ui.tW_rule.setCellWidget(row, col, edit)
            self.ui.tW_rule.setCellWidget(row, col + 1, _del)
            edit.clicked.connect(self.edit_rule)
            _del.clicked.connect(self.del_rule)

    def run(self):
        self.set_cmd()
        self.load()
        self.ui.exec_()

    def set_cmd(self):
        self.ui.cLB_add_rule.clicked.connect(lambda *x: self.edit_rule(True))

    def del_rule(self):
        index = self.ui.tW_rule.currentIndex().row()
        self.ui.tW_rule.removeRow(index)
        self.up_rule()

    def edit_rule(self, add=True):
        dlg_edit = RuleEdit()
        dlg_edit.setWindowFlags(Qt.FramelessWindowHint)

        if not add:
            index = self.ui.tW_rule.currentIndex().row()
            dlg_edit.sB_len.setValue(int(self.ui.tW_rule.item(index, 0).text()))
            sB_lot = self.ui.tW_rule.item(index, 1).text().split('-')
            sB_num = self.ui.tW_rule.item(index, 2).text().split('-')
            dlg_edit.sB_lot_pre.setValue(int(sB_lot[0]))
            dlg_edit.sB_lot_suf.setValue(int(sB_lot[1]))
            dlg_edit.sB_num_pre.setValue(int(sB_num[0]))
            dlg_edit.sB_num_suf.setValue(int(sB_num[1]))

        # noinspection PyArgumentList
        def save():
            length = dlg_edit.sB_len.value()
            lot = f"{dlg_edit.sB_lot_pre.value()}-{dlg_edit.sB_lot_suf.value()}"
            num = f"{dlg_edit.sB_num_pre.value()}-{dlg_edit.sB_num_suf.value()}"

            if add:
                row = self.ui.tW_rule.rowCount()
                self.ui.tW_rule.insertRow(row)
                self.ui.tW_rule.setItem(row, 0, QTableWidgetItem(f'{length}'))
                self.ui.tW_rule.setItem(row, 1, QTableWidgetItem(f'{lot}'))
                self.ui.tW_rule.setItem(row, 2, QTableWidgetItem(f'{num}'))
                edit = QPushButton('编辑')
                _del = QPushButton('删除')
                self.ui.tW_rule.setCellWidget(row, 3, edit)
                self.ui.tW_rule.setCellWidget(row, 4, _del)
                edit.clicked.connect(self.edit_rule)
                _del.clicked.connect(self.del_rule)
            else:
                self.ui.tW_rule.item(index, 0).setText(f'{length}')
                self.ui.tW_rule.item(index, 1).setText(f'{lot}')
                self.ui.tW_rule.item(index, 2).setText(f'{num}')
            dlg_edit.close()
            self.up_rule()

        dlg_edit.lE_norm.textChanged.connect(
            lambda d: dlg_edit.sB_len.setValue(len(d))
        )
        dlg_edit.sB_lot_pre.valueChanged.connect(
            lambda pre: dlg_edit.lE_show_lot.setText(
                dlg_edit.lE_norm.text()[pre: dlg_edit.sB_lot_suf.value()]
            )
        )
        dlg_edit.sB_lot_suf.valueChanged.connect(
            lambda suf: dlg_edit.lE_show_lot.setText(
                dlg_edit.lE_norm.text()[dlg_edit.sB_lot_pre.value(): suf]
            )
        )

        dlg_edit.sB_num_pre.valueChanged.connect(
            lambda pre: dlg_edit.lE_show_num.setText(
                dlg_edit.lE_norm.text()[pre: dlg_edit.sB_num_suf.value()]
            )
        )
        dlg_edit.sB_num_suf.valueChanged.connect(
            lambda suf: dlg_edit.lE_show_num.setText(
                dlg_edit.lE_norm.text()[dlg_edit.sB_num_pre.value(): suf]
            )
        )

        dlg_edit.lE_norm.returnPressed.connect(dlg_edit.sB_lot_pre.setFocus)
        dlg_edit.lE_norm.setFocus()
        dlg_edit.cLB_save.clicked.connect(save)
        dlg_edit.cLB_cancle.clicked.connect(dlg_edit.close)
        dlg_edit.exec_()

    def up_rule(self):
        self.rules = []
        for row in range(self.ui.tW_rule.rowCount()):
            self.rules.append((
                self.ui.tW_rule.item(row, 0).text(),
                self.ui.tW_rule.item(row, 1).text(),
                self.ui.tW_rule.item(row, 2).text(),
            ))
        cfg.set('rule', 'rules', f'{self.rules}')
        Main.check.up_rule()


class Check:
    def __init__(self):
        self.rules = {}
        self.up_rule()

    def up_rule(self):
        rules = eval(cfg.get('rule', 'rules', '[]'))
        self.rules.clear()
        for rule in rules:
            length = int(rule[0])
            value = ([int(_) for _ in rule[1].split('-')], [int(_) for _ in rule[2].split('-')])
            if length in self.rules:
                self.rules[length].append(value)
            else:
                self.rules[length] = [value, ]

    def check(self, *args, UI=False):
        nums, data = 0, {}
        for d in args:
            rules = self.rules.get(len(d))
            if not rules:
                raise CheckError(f'数据: {d}\n长度{len(d )}未配置检测规则')

            no_lot = True
            for rule in rules:
                lot = d[rule[0][0]:rule[0][1]]
                if lot in Main.app.check_lots:
                    pre, suf = rule[1][0], rule[1][1]
                    if pre == suf == 0:
                        num = 1
                    else:
                        num = int(d[pre: suf])
                    nums += num
                    if lot in data:
                        data[lot] += num
                    else:
                        data[lot] = num
                    no_lot = False
                    break
                else:
                    continue
            if no_lot:
                raise CheckError(f'数据：{d} 通过检测规则获取Lot与单据信息不符！')

        if nums != 10 and not UI:
            raise CheckError(f'数量错误，仅检测到{nums}个产品，不足10个,请检查或手动扫描录入')

        extra = Main.app.check_full(data)
        if len(extra) > 0:
            _sp = " \n"
            raise CheckError(f'批次为:\n{_sp.join(extra)}\n的产品超出发货数量，请检查！！！')

        for k, v in data.items():
            div.change_tw.emit(k, v)

        return data, nums


class BtwEngine:
    def __init__(self):
        self.engine: Bartender = ...
        self.btw_wx: Bartender.BtFile = ...
        self.btw_mx: Bartender.BtFile = ...
        self.btw_wx_file = os.path.abspath('btw/BOX.btw')
        self.btw_mx_file = os.path.abspath('btw/ITEM.btw')

    def load_btw_engine(self):
        _btw_path = yml.get('BT_INSTALL_PATH')
        if _btw_path and os.path.exists(_btw_path):
            _btw_sdk_path = os.path.join(_btw_path, 'SDK/Assemblies')
            try:
                self.engine = Bartender(_btw_sdk_path)
                print('打印引擎加载成功')
                log.info('Init Btw Engine: 打印引擎加载成功')
            except FileNotFoundError as _engine_load_err:
                raise ModuleNotFoundError(f'未能成功加载BT SDK!\n {_engine_load_err}')
        else:
            raise FileNotFoundError(f'Btw Engine init error! :>> Can not found path: {_btw_path}')
        self.open_wx()
        self.open_mx()

    def open_wx(self):
        if self.btw_wx in self.engine.btFormats:
            self.btw_wx.close_btw()
        self.btw_wx = self.engine.open_btw(self.btw_wx_file, 'BOX_OUT_LAB')
        print('BTW BOX_OUT_LAB LOADED!')

    def open_mx(self):
        if self.btw_mx in self.engine.btFormats:
            self.btw_mx.close_btw()
        self.btw_mx = self.engine.open_btw(self.btw_mx_file, 'BOX_ITEM_LAB')
        print('BTW BOX_ITEM_LAB LOADED!')

    def engined(self):
        return self.engine is not Ellipsis

    def close(self):
        if self.engined():
            self.engine.close()

    def print_wx(self, data):
        self.btw_wx.set_data_dict(data)
        res = f"外箱标签打印：{self.btw_wx.btFormat.Print()}, 打印参数：{data}"
        # print(res)
        log.info(res)
        # print(self.btw_wx.get_data_dict())

    def print_mx(self, data):
        self.btw_mx.set_data_dict(data)
        res = f"装箱明细标签打印：{self.btw_mx.btFormat.Print()}, 打印参数：{data}"
        # print(res)
        log.info(res)
        # print(self.btw_mx.get_data_dict())

    def imp_btw(self, typ, path):
        if typ == 'BOX_OUT_LAB':
            file = self.btw_wx_file
            self.btw_wx.close_btw()
            op = self.open_wx
        elif typ == 'BOX_ITEM_LAB':
            file = self.btw_mx_file
            self.btw_mx.close_btw()
            op = self.open_mx
        else:
            return False
        with open(path, mode="rb")as _rb:
            with open(file, mode='wb')as _wb:
                _wb.write(_rb.read())
        op()
        return True

    def get_view_wx(self):
        png = os.path.abspath('btw/BOX_OUT_LAB.png')
        self.btw_wx.btw_image(png)
        return png

    def get_view_mx(self):
        png = os.path.abspath('btw/BOX_ITEM_LAB.png')
        self.btw_mx.btw_image(png)
        return png


try:
    _app = QApplication()
    _app.setStyle('Fusion')
    _trans = QTranslator()
    _trans.load('config/ZH_CN')
    _app.installTranslator(_trans)
    serverName = 'BoMaiAPP2'
    _skt = QLocalSocket()
    _skt.connectToServer(serverName)
    if _skt.waitForConnected(500):
        win32api.MessageBox(0, f"程序已经启动一个实例", "错误！", 48)
        _app.quit()
        sys.exit(sys.argv[0])
    _skt.close()
    _skt = QLocalServer()
    _skt.listen(serverName)
    Main = StartApp()
    Main.run()
    _app.exec_()
    Main.stop()
except Exception as e:
    win32api.MessageBox(0, f"程序启动失败：\tError MSG:{e}", "错误！", 48)
    # raise e
    sys.exit(sys.argv[0])
