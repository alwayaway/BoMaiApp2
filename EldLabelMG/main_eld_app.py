import cgitb
import traceback
from toolbase import *

cgitb.enable(logdir='log', format="text")

loaded_splash('LOADING')
try:
    from math import ceil
    from threading import Thread

    import win32api
    from PySide2.QtCore import QObject, QTranslator, Qt
    from PySide2.QtGui import QIcon, QPixmap
    from PySide2.QtNetwork import QLocalServer, QLocalSocket
    from PySide2.QtWidgets import QApplication

    from BTSDK.bartend import Bartender
    from EldLabelMG import btwbase, ui
    from toolbase.fmt import FmtTime
    from toolbase.my_dlg import DlgMSG
except Exception as _init_err:
    loaded_close()
    raise _init_err


__APP__ = 'ELD LABEL PRINT MANAGER'
__VERSION__ = 'V1.0.0'

check_dir(('log', 'config', 'base', 'images'))
log = Log('log', 'run_log')
ini = Cfgfile('config/setup.ini')
cfg = Cfgdbase('config/cfg.db')
btw = btwbase.BtwBase('config/data.db')
mbx = DlgMSG()

UNIQUE = "@唯一约束"


class MySignal(QObject):
    loading = ui.Signal()
    showMsg = ui.Signal(str)


signal = MySignal()


class MainApp:
    def __init__(self):
        self.is_running = False
        self.engine: Bartender = ...
        self.ui: _AppUi = ...

    def run(self):
        self.is_running = True
        self.init()
        self.ui = _AppUi(self)
        self.ui.show()

    def init(self):
        print(self.load_btw_engine())

    def load_btw_engine(self, path='C:/Program Files (x86)/Seagull/BarTender Suite/'):
        _btw_path = ini.get('bartender', 'path', path)
        if _btw_path and os.path.exists(_btw_path):
            try:
                self.engine = Bartender(_btw_path)
                log.info(f'Init btw sdk successful! :>> path is {path}')
                return 0, 'Init btw sdk successful!'
            except FileNotFoundError as _engine_load_err:
                log.info(f'{_engine_load_err} :>> path is {path}')
                return -1, _engine_load_err
        log.error(f'UnKnown engine init error! :>> path is {path}')
        return -1, 'UnKnown engine init error!'

    def engined(self):
        return self.engine is not Ellipsis

    def close(self):
        self.is_running = False
        if self.engined():
            self.engine.close_btw()
            self.engine.close()
            if self.ui.btw_name and os.path.exists(self.ui.btw_file):
                btw.update_btw(self.ui.btw_name, btwblod=self.ui.btw_file)
        cfg.close()
        ini.close()
        btw.close()
        log.shutdown()


# noinspection PyTypeChecker,PyArgumentList
class Load:
    def __init__(self, func, *args, _thread=True, **kwargs, ):
        parent = ui.QDialog()
        parent.setAttribute(Qt.WA_TranslucentBackground)
        parent.setWindowFlags(Qt.FramelessWindowHint)
        parent.setWindowModality(Qt.ApplicationModal)
        load_bar = ui.QProgressBar(parent)
        load_bar.setFixedSize(240, 40)
        load_bar.setMaximum(0)
        load_bar.setValue(-1)
        load_bar.setTextDirection(ui.QProgressBar.TopToBottom)
        load_bar.show()
        load_bar.setFocus()
        load_bar.move((parent.width() - 240) / 2, parent.height() / 2)
        self.res = ...
        self._stop = False

        try:
            if _thread:
                def _func():
                    self.res = func(*args, **kwargs)

                Thread(target=_func, daemon=True).start()
                while self.res is Ellipsis:
                    parent.show()
                    _app.processEvents()
            else:
                pB_stop = ui.QPushButton('停止', parent=parent)
                # noinspection PyUnresolvedReferences
                pB_stop.clicked.connect(self.stop)
                pB_stop.setFixedSize(100, 36)
                pB_stop.setEnabled(True)
                pB_stop.move((parent.width() - 100) / 2, parent.height() / 2 + 60)
                pB_stop.show()
                for _ in func(*args, **kwargs):
                    parent.show()
                    _app.processEvents()
                    if self._stop:
                        break
        except Exception as _loading_err:
            # raise _loading_err
            log.error(f'执行过程发生错误:{_loading_err}')
            mbx.critical('错误', f'执行过程发生错误, 详见 err 日志！', mainWin.ui)
        finally:
            parent.close()
            parent.deleteLater()

    def stop(self):
        self._stop = True


class _AppUi(ui.Main):
    def __init__(self, main):
        super().__init__()

        self.setWindowTitle(__APP__ + __VERSION__)
        self.setWindowIcon(QIcon('images/ico'))

        self._app: MainApp = main
        self.engine = self._app.engine
        self.btw_name = ini.get('bartender', 'file', '')
        self.btw_dict = {}
        self.btw_bar = ''
        self.btw_file = os.path.abspath('./base/base.btw')
        self.btw_jpeg = os.path.abspath('./base/base.png')
        self.btw_open = False
        self.sub_show = None

        self.nor_array = [_.strip() for _ in ini.get('bartender', 'array', '0123456789')]
        self.rev_array = self.nor_array.copy()
        self.rev_array.reverse()

        self.stf = FmtTime()

        self.ptCheck = ini.get('print_status', 'PrintingCheck', '1') == '1'
        self.prmLoad = ini.get('print_status', 'ParamsShow', '0') == '1'

        self.init()

    def init(self):
        self.set_cmd()
        self.init_check()
        self.tB_show.document().setMaximumBlockCount(200)
        self.lE_btw_used.setText(self.btw_name)
        self.change_btw(self.btw_name) if self.btw_name else None

        self.cLK_print_nocheck.hide()
        self.sB_copy_num.setDisabled(True)
        date = time.localtime()
        self.dTE_curr_time.setDate(ui.QDate(date.tm_year, date.tm_mon, date.tm_mday))
        # self.sB_print_num.setMaximum(10000000)  # @DEL

    def init_check(self):
        self.showMsg('init btw engine %s !' % 'successful' if self._app.engined() else 'failed')

    def set_cmd(self):
        self.pB_btw_base.clicked.connect(_BtwBase)
        self.cLK_params_check.clicked.connect(lambda *x: Load(self.check_params, _thread=False))
        self.cLK_print_nocheck.clicked.connect(lambda *x: Load(self.check_print, False, _thread=False))
        self.cLK_print_check.clicked.connect(lambda *x: Load(self.check_print, _thread=False))
        self.tB_btw_change.clicked.connect(lambda *x: self.change_btw())
        self.tW_btw_params.cellChanged.connect(self.upCell)
        self.pB_rep_data.clicked.connect(lambda *x: RepView())
        self.dTE_curr_time.dateChanged.connect(self.up_stf_date)
        signal.showMsg.connect(self.showMsg)

    def up_stf_date(self, date):
        date = date.toString("yyyy-MM-dd")
        self.stf.setTime(date, '%Y-%m-%d')

    def upCell(self, row, cel):
        key = self.tW_btw_params.item(row, 0).text()
        val = self.tW_btw_params.item(row, cel).text()
        if key == UNIQUE and self.btw_bar != val:
            self.btw_bar = val
        else:
            self.btw_dict[key] = val

    def showMsg(self, msg):
        self.tB_show.append(msg)
        log.info(msg)

    def check_params(self):
        """数据检查"""
        self.showMsg('开始数据进行检查')
        rows = self.sB_print_num.value()
        idx = 1

        # def get_bars(btw_dict):
        #     Asc, Desc = [], []
        #     for k in btw_dict.keys():
        #         if k.startswith('SN_') or k.startswith('sn_'):
        #             if k.endswith('_DESC') or k.endswith('_desc'):
        #                 Desc.append(k)
        #             else:
        #                 Asc.append(k)
        #     for _k in range(rows):
        #         now_bar = str4mat(self.btw_bar, btw_dict)
        #         btw_dict.update({k: arr_next(btw_dict[k], self.nor_array) for k in Asc})
        #         btw_dict.update({k: arr_next(btw_dict[k], self.rev_array) for k in Desc})
        #         yield now_bar
        def get_bars(btw_dict):
            for _r in range(rows):
                index, btw_dict = self.get_bar(btw_dict)
                yield index

        try:
            for ck_bar in get_bars(self.btw_dict.copy()):
                if btw.exist_Rep(ck_bar):
                    mbx.warning('提示', f'数据检查结果通知: 条码数据：{ck_bar} 已存在！', self)
                    return
                self.showMsg(f'数据检查进度: {idx}/{rows} \t条码检查通过: {ck_bar}')
                idx += 1
                yield idx
            self.showMsg(f'数据检查完成！')
        except ValueError:
            self.showMsg(f"列区间无法继续升降序, 请检查！")
            mbx.warning('提示', '序列区间无法继续升降序, 请检查', self)
            return
        except Exception as _check_err:
            log.error(f'数据检擦发生异常： {_check_err}')
            mbx.critical('错误', '数据检擦发生异常, 详见日志!', self)
            raise _check_err

    def get_bar(self, btw_dict=None):
        if btw_dict is None:
            btw_dict = self.btw_dict.copy()
        for k in tuple(btw_dict.keys()):
            if k.startswith('SN_') or k.startswith('sn_'):
                if k.endswith('_DESC') or k.endswith('_desc'):
                    btw_dict[k] = arr_next(btw_dict[k], self.rev_array)
                else:
                    btw_dict[k] = arr_next(btw_dict[k], self.nor_array)
            elif k in self.stf:
                btw_dict[k] = self.stf.get(k)
        return str4mat(self.btw_bar, btw_dict), btw_dict

    """
    def up_bar(self, btw_dict):
        if btw_dict is None:
            btw_dict = self.btw_dict.copy()
        for k in tuple(btw_dict.keys()):
            if k.startswith('SN_') or k.startswith('sn_'):
                if k.endswith('_DESC') or k.endswith('_desc'):
                    btw_dict[k] = arr_next(btw_dict[k], self.rev_array)
                else:
                    btw_dict[k] = arr_next(btw_dict[k], self.nor_array)
            elif k in self.stf:
                btw_dict[k] = self.stf.get(k)
        return btw_dict
    """

    def up_tW_btw_params(self, btw_dict):
        for row in range(1, self.tW_btw_params.rowCount()):
            self.tW_btw_params.item(row, 1).setText(
                btw_dict.get(self.tW_btw_params.item(row, 0).text(), 'Invalid data!')
            )

    def check_print(self, check=True):
        if not self.check_engine():
            return

        pt_num = self.sB_print_num.value()
        ped_num = 1

        self.engine.btFormat.PrintSetup.NumberOfSerializedLabels = 1  # 打印数量
        self.engine.btFormat.PrintSetup.IdenticalCopiesOfLabel = self.sB_copy_num.value()  # 复制数量
        self.showMsg(f"新增打印任务：共计{pt_num}个标签， 每个标签打印{self.sB_copy_num.value()}次数")
        for _ in range(pt_num):
            try:
                now_bar, btw_dict = self.get_bar()
                if check and self.btw_bar:
                    if btw.exist_Rep(now_bar):
                        mbx.warning('警告', f'序列数据：{now_bar} 已存在， 不可重复列印此序列标签', self)
                        return
                    else:
                        btw.add_Rep(now_bar)
                self.up_tW_btw_params(btw_dict)
            except ValueError:
                self.showMsg(f"打印任务异常结束：序列区间无法继续升降序, 请检查！")
                mbx.warning('提示', '序列区间无法继续升降序, 请检查', self)
                return

            self.showMsg(f"打印任务：{ped_num}/{pt_num}， 标签序列: {now_bar}")

            while True:
                state = self.start_print(**btw_dict)
                print('打印状态', f'{state}')
                if self.ptCheck:
                    break
                elif state in (0, 'Success'):
                    break
                elif state == 1:
                    inf = '打印超时， 是否重新打印？'
                elif state == 2:
                    inf = '打印失败， 是否重新打印？'
                else:
                    inf = '未知的打印状态， 是否重新打印？'
                QMessageBox = ui.QMessageBox
                dlg = QMessageBox(QMessageBox.Question, '询问?', inf, parent=self)
                # noinspection PyTypeChecker
                dlg.addButton(dlg.tr("重新打印"), QMessageBox.ResetRole)
                # noinspection PyTypeChecker
                dlg.addButton(dlg.tr("继续打印"), QMessageBox.YesRole)
                # noinspection PyTypeChecker
                dlg.addButton(dlg.tr("取消打印"), QMessageBox.NoRole)
                dlg.exec_()
                if dlg.result() == 0:
                    self.showMsg(f"打印任务失败：重新启动当前异常标签！")
                    continue
                if dlg.result() == 1:
                    self.showMsg(f"打印任务失败：选择跳过当前异常标签！")
                    break
                elif dlg.result() == 2:
                    self.showMsg(f"打印任务失败：选择停止当前打印任务！")
                    return
                else:
                    self.showMsg(f"打印任务失败：未知的异常选项， 强制停止当前打印任务！")
                    return
            yield 0
            ped_num += 1
        self.showMsg(f"打印任务：打印{pt_num}个标签结束！")
        self.load_btw()

    def start_print(self, **params):
        """开始列印"""
        self.engine.set_data_dict(params)
        return self.engine.btFormat.Print()

    def check_engine(self):
        """判断btw引擎是否启动"""
        if self._app.engined():
            return True
        else:
            mbx.warning('警告', 'bartender 引擎初始化加载失败！ \n请确保安PC已经装bartender .NET SDK 组件'
                              '且在系统设置中已设置正确的bartender安装路径', self)
            return False

    def change_btw(self, name=...):
        if name is Ellipsis:
            chose = ChoseBtwBase()
            name = chose.btwname
            if name is None:
                return
            if self.btw_name:
                btw.update_btw(self.btw_name, btwblod=self.btw_file)

        fd = btw.get_btw(name)
        if fd and self.check_engine():
            self.engine.close_btw()
            self.btw_bar = fd.get('UNIQUE')
            with open(self.btw_file, mode='wb')as _wb:
                _wb.write(fd.get('btw'))
        else:
            mbx.critical('错误', f'模板仓库中未检索到标签: {name}, 加载标签失败', self)
            name = ''
        self.btw_name = name
        self.lE_btw_used.setText(name)
        self.load_btw() if name else None
        ini.set('bartender', 'file', name)

    def clean_btw(self):
        self.btw_dict.clear()
        self.mdiArea.removeSubWindow(self.sub_show) if self.sub_show else None
        self.sub_show.deleteLater() if self.sub_show else None
        self.tW_btw_params.setRowCount(0)

    # noinspection PyArgumentList
    def load_params(self, data: dict):
        print(data)
        data.pop(UNIQUE) if UNIQUE in data else None
        # data = self.up_bar(data)
        for k, v in data.items():
            self.tW_btw_params.insertRow(0)
            key = ui.QTableWidgetItem(f'{k}')
            val = ui.QTableWidgetItem(f'{v}')
            key.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tW_btw_params.setItem(0, 0, key)
            self.tW_btw_params.setItem(0, 1, val)
            if k in self.stf:
                if self.prmLoad:
                    val.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                else:
                    self.tW_btw_params.setRowHidden(0, True)

        self.tW_btw_params.insertRow(0)
        key = ui.QTableWidgetItem(UNIQUE)
        val = ui.QTableWidgetItem(f'{self.btw_bar}')
        key.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        val.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        self.tW_btw_params.setItem(0, 0, key)
        self.tW_btw_params.setItem(0, 1, val)

    def load_btw(self):
        if self.check_engine():
            # noinspection PyArgumentList
            try:
                self.clean_btw()

                def _load_btw():
                    self.engine.open_btw(self.btw_file)
                    self.engine.btw_image(self.btw_jpeg)
                    return True

                Load(_load_btw)
                self.load_params(self.engine.get_data_dict())
                self.btw_open = True
                png = QPixmap(self.btw_jpeg)
                lb_btw_show = ui.QLabel()
                lb_btw_show.setPixmap(png)
                self.sub_show = self.mdiArea.addSubWindow(lb_btw_show, Qt.FramelessWindowHint)
                self.sub_show.move(0, 0)
                lb_btw_show.mouseMoveEvent = self.SubMoveEvent
                lb_btw_show.mousePressEvent = self.SubPressEvent
                lb_btw_show.mouseReleaseEvent = self.SubReleaseEvent
                self.sub_show.show()
                self.showMsg(f'加载模板文件 {self.btw_name} 成功！')
            except Exception as _load_btw_err:
                ini.set('bartender', 'file', '')
                self.btw_open = False
                self.showMsg(f'加载模板文件 {self.btw_name} 失败，详见日志！')
                log.error(f"load btw file err: {_load_btw_err}")
                raise _load_btw_err

    def SubMoveEvent(self, mvt):
        # noinspection PyBroadException
        try:
            if Qt.LeftButton and self.sub_show.m_flag:
                self.sub_show.move(mvt.globalPos() - self.sub_show.m_Position)  # 更改窗口位置
                mvt.accept()
        except Exception:
            pass

    def SubPressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.sub_show.m_flag = True
            self.sub_show.m_Position = event.globalPos() - self.sub_show.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.sub_show.setCursor(Qt.SizeAllCursor)

    def SubReleaseEvent(self, mvt):
        self.sub_show.m_flag = False
        self.sub_show.setCursor(Qt.ArrowCursor)
        _ = mvt


class _BtwBase(ui.Base):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowIcon(QIcon('images/ico'))
        self.editing = False
        self.init()
        self.exec_()

    def closeEvent(self, arg__1):
        self.deleteLater()

    def init(self):
        self.cLK_add_btw.clicked.connect(self.add_btw)
        self.tW_btw_base.cellChanged.connect(self.upCell)
        self.tW_btw_base.cellDoubleClicked.connect(self.DoubleClicked)
        self.tW_btw_base.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tW_btw_base.customContextMenuRequested.connect(self.tW_menu)
        self.lE_serch.textChanged.connect(self.search)
        Load(self.load, _thread=False)

    def tW_menu(self, pos):
        row_num = -1
        for i in self.tW_btw_base.selectionModel().selection().indexes():
            row_num = i.row()
        if row_num < 0:
            return
        btwname = self.tW_btw_base.item(row_num, 0).text()
        menu = ui.QMenu()
        item1 = menu.addAction(u"更新模板文件")
        item2 = menu.addAction(u"删除模板文件")
        item3 = menu.addAction(u"导出模板文件")
        action = menu.exec_(self.tW_btw_base.mapToGlobal(pos))
        if action == item1:
            if btwname == mainWin.ui.btw_name:
                mbx.warning('提示', f'待更新模板 {btwname} 当前正在使用，请切换后再尝试改操作！', self)
                return
            if mbx.question('更新？', f'确定更新模板文件: {btwname} ？', self).result() == 0:
                btwblod, type_ = ui.QFileDialog.getOpenFileName(self, "选择模板文件", "C:", "btw Files (*.btw)")
                if not btwblod:
                    return
                if btw.update_btw(btwname, btwblod=btwblod) > 0:
                    log.info(f'更新模板 {btwname} 文件为 {btwblod} 成功！')
                    mbx.information('提示', f'更新模板 {btwname} 文件为 {btwblod} 成功！', self)
                else:
                    log.info(f'更新模板 {btwname} 文件为 {btwblod} 失败！')
                    log.error(f'更新模板 {btwname} 文件为 {btwblod} 失败！')
                    mbx.warning('提示', f'更新模板 {btwname} 文件为 {btwblod} 失败！', self)
        elif action == item2:
            if mbx.question('删除？', f'确定删除模板文件: {btwname} ？', self).result() == 0:
                if btw.del_btw(btwname) >= 0:
                    self.tW_btw_base.removeRow(row_num)
                else:
                    mbx.critical('错误', '未知原因，删除失败', self)
        elif action == item3:
            file_, type_ = ui.QFileDialog.getSaveFileName(self, "导出模板文件", "C:", "btw Files (*.btw)")
            if not file_:
                return
            fd = btw.get_btw(btwname)
            print(fd)
            if fd:
                with open(file_, mode='wb')as _wb:
                    _wb.write(fd.get('btw'))
                mbx.information('提示', f'导出模板文件到 {file_}', self)
            else:
                mbx.critical('错误', f'导出模板文件失败', self)
        else:
            return

    def DoubleClicked(self, *args):
        _ = args
        self.editing = True

    def load(self):
        self.editing = False
        self.tW_btw_base.setRowCount(0)
        data = btw.get_btwS('btwname', 'btwdict')
        for row in data:
            self.tW_btw_base.insertRow(0)
            name = ui.QTableWidgetItem(row[0])
            bard = ui.QTableWidgetItem(row[1])
            name.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tW_btw_base.setItem(0, 0, name)
            self.tW_btw_base.setItem(0, 1, bard)
            yield row

    def upCell(self, row, cel):
        if self.editing:
            btwname = self.tW_btw_base.item(row, 0).text()
            btwdict = self.tW_btw_base.item(row, cel).text()
            print(f'btwname: {btwname}\tbtwdict: {btwdict}')
            if btw.update_btw(btwname, btwdict=btwdict) > 0:
                log.info(f'更新模板 {btwname} 条码组成为 {btwdict} 成功！')
            else:
                log.info(f'更新模板 {btwname} 条码组成为 {btwdict} 失败！')
                log.error(f'更新模板 {btwname} 条码组成为 {btwdict} 失败！')

    def search(self, val):
        for row in range(self.tW_btw_base.rowCount()):
            if val in self.tW_btw_base.item(row, 0).text():
                self.tW_btw_base.showRow(row)
            else:
                self.tW_btw_base.hideRow(row)

    def add_btw(self):
        dlg = ui.AddBtw()
        dlg.setWindowFlags(Qt.WindowCloseButtonHint)
        dlg.setWindowModality(Qt.ApplicationModal)
        dlg.setWindowIcon(QIcon('images/ico'))

        def sure():
            name = dlg.lE_btw_name.text().strip()
            file = dlg.lE_btw_file.text().strip()
            if not name:
                mbx.warning('警告', '模板名称不能为空！', dlg)
                return
            if not os.path.exists(file):
                mbx.warning('警告', '模板文件不存在！', dlg)
                return

            if btw.add_btw(name, '', os.path.abspath(file)):
                dlg.deleteLater()
                self.tW_btw_base.insertRow(0)
                item_name = ui.QTableWidgetItem(name)
                item_name.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                self.tW_btw_base.setItem(0, 0, item_name)
                mbx.information('提示', f'新增模板 {name} 成功', self)
            elif btw.exist_btw(name):
                mbx.information('提示', f'模板名称: {name} 已存在!', dlg)
            else:
                dlg.deleteLater()
                mbx.critical('警告', f'未知原因， 新增失败!', self)

        def _chose():
            file_, type_ = ui.QFileDialog.getOpenFileName(dlg, "选择模板文件", "C:", "btw Files (*.btw)")
            if not file_:
                return
            dlg.lE_btw_file.setText(file_)

        dlg.tB_chose_btw.clicked.connect(lambda *x: _chose())
        dlg.pB_sure.clicked.connect(lambda *x: sure())
        dlg.pB_cancel.clicked.connect(lambda *x: dlg.deleteLater())

        dlg.exec_()


class ChoseBtwBase(_BtwBase):
    def __init__(self):
        self.btwname = None
        super().__init__()

    def init(self):
        self.cLK_add_btw.setText('变更为选中模板')
        self.tW_btw_base.setEditTriggers(ui.QAbstractItemView.NoEditTriggers)
        self.tW_btw_base.setSelectionBehavior(ui.QAbstractItemView.SelectRows)
        self.tW_btw_base.setSelectionMode(ui.QAbstractItemView.SingleSelection)

        self.tW_btw_base.cellDoubleClicked.connect(self.DoubleClicked)
        self.cLK_add_btw.clicked.connect(self.sure)
        self.lE_serch.textChanged.connect(self.search)
        Load(self.load, _thread=False)

    def DoubleClicked(self, row, cel):
        self.change(row)

    def sure(self):
        row = self.tW_btw_base.currentRow()
        if row >= 0:
            self.change(row)

    def change(self, row):
        self.btwname = self.tW_btw_base.item(row, 0).text()
        self.deleteLater()


class RepView(ui.RepView):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowIcon(QIcon('images/ico'))
        self.page = 1
        self.rows = 1000
        self.max_page = 1
        self.search_data = ''

        self.init()

    def init(self):
        self.set_cmd()
        self.exec_()

    def set_cmd(self):
        self.pB_search.clicked.connect(self.search)
        self.pB_page_last.clicked.connect(lambda *x: self.change_page(-1))
        self.pB_page_next.clicked.connect(lambda *x: self.change_page(1))
        self.pB_page_change.clicked.connect(lambda *x: self.change_page(None))

        self.pB_del_sel.clicked.connect(self.del_sel)
        self.pB_del_all.clicked.connect(self.del_all)

    def search(self):
        self.page = 1
        self.search_data = self.lE_search.text()
        self.change_page(0)

    def _search(self):
        rows = btw.getRepLen(self.search_data)
        enable = rows > 0

        self.max_page = ceil(rows / self.rows)

        self.pB_del_sel.setEnabled(enable)
        self.pB_del_all.setEnabled(enable)
        self.pB_page_change.setEnabled(enable)
        self.sB_page.setMaximum(self.max_page)
        self.sB_page.setSuffix(f' / {self.max_page} 页')

    def change_page(self, page=None):
        self.tableWidget.setRowCount(0)
        if page is None:
            self.page = self.sB_page.value()
        else:
            self.page += page

        self._search()
        self.pB_page_last.setEnabled(self.page > 1)
        self.pB_page_next.setEnabled(self.page < self.max_page)
        self.sB_page.setValue(self.page)

        # noinspection PyArgumentList
        for data in btw.searchRep(self.search_data, (self.page - 1) * self.rows, self.rows):
            self.tableWidget.insertRow(0)
            item = ui.QTableWidgetItem(data[0])
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tableWidget.setItem(0, 0, item)

    def del_sel(self):
        if btw.del_Rep(*(item.text() for item in self.tableWidget.selectedItems())):
            print('删除成功')
        else:
            print('删除失败')
        self.change_page(0)
        if self.tableWidget.rowCount() <= 0:
            self.change_page(0)

    def del_all(self):
        if btw.del_Rep(*(self.tableWidget.item(row, 0).text() for row in range(self.tableWidget.rowCount()))):
            self.change_page(-1)
            print('删除成功')
        else:
            print('删除失败')
            self.change_page(0)


try:
    try:
        _app = QApplication()
    except RuntimeError:
        _app = QApplication.instance()
    _app.setStyle('Fusion')
    # noinspection PyArgumentList
    _trans = QTranslator()
    # noinspection PyArgumentList
    _trans.load('config/ZH_CN')
    _app.installTranslator(_trans)
    serverName = 'Eld_Main_App'
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
    mainWin = MainApp()
    mainWin.run()
    loaded_close()
    _app.exec_()
    mainWin.close()
    _app.exit(0)
except Exception as e:
    loaded_close()
    win32api.MessageBox(0, f"程序启动失败：\tError MSG:{e}", "错误！", 48)
    traceback.print_exc(5)
finally:
    sys.exit()
