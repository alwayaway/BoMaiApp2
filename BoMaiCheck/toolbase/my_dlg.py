from PySide2.QtWidgets import *
from PySide2.QtCore import Qt, Signal, QTimer


class Dlg_MSG:
    def __init__(self):
        self.dlg = None

    def information(self, tit, msg, parent):
        self.dlg = QMessageBox(QMessageBox.Information, tit, msg, parent=parent)
        self.dlg.addButton(self.dlg.tr("我知道了"), QMessageBox.YesRole)
        self.dlg.exec_()
        return self.dlg

    def question(self, tit, msg, parent):
        self.dlg = QMessageBox(QMessageBox.Question, tit, msg, parent=parent)
        self.dlg.addButton(self.dlg.tr("确定"), QMessageBox.YesRole)
        self.dlg.addButton(self.dlg.tr("取消"), QMessageBox.NoRole)
        self.dlg.exec_()
        return self.dlg

    def warning(self, tit, msg, parent):
        self.dlg = QMessageBox(QMessageBox.Warning, tit, msg, parent=parent)
        self.dlg.addButton(self.dlg.tr("我知道了"), QMessageBox.YesRole)
        self.dlg.exec_()
        return self.dlg

    def critical(self, tit, msg, parent):
        self.dlg = QMessageBox(QMessageBox.Critical, tit, msg, parent=parent)
        self.dlg.addButton(self.dlg.tr("我知道了"), QMessageBox.YesRole)
        self.dlg.exec_()
        return self.dlg

