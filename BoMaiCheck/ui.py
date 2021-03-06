# -*- coding: utf-8 -*-
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class BtwSet(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(565, 382)
        self.horizontalLayout = QHBoxLayout(self)
        self.frame = QFrame(self)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.horizontalLayout_2 = QHBoxLayout()
        self.label = QLabel(self.frame)
        self.horizontalLayout_2.addWidget(self.label)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(self.horizontalSpacer)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QHBoxLayout()
        self.pB_edit_wx = QPushButton(self.frame)
        self.horizontalLayout_3.addWidget(self.pB_edit_wx)
        self.pB_imp_wx = QPushButton(self.frame)
        self.horizontalLayout_3.addWidget(self.pB_imp_wx)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.lb_show_wx = QLabel(self.frame)
        sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_show_wx.sizePolicy().hasHeightForWidth())
        self.lb_show_wx.setSizePolicy(sizePolicy)
        self.verticalLayout.addWidget(self.lb_show_wx)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer)
        self.horizontalLayout.addWidget(self.frame)
        self.frame_2 = QFrame(self)
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_2)
        self.horizontalLayout_5 = QHBoxLayout()
        self.label_5 = QLabel(self.frame_2)
        self.horizontalLayout_5.addWidget(self.label_5)
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4 = QHBoxLayout()
        self.pB_edit_nx = QPushButton(self.frame_2)
        self.horizontalLayout_4.addWidget(self.pB_edit_nx)
        self.pB_imp_nx = QPushButton(self.frame_2)
        self.horizontalLayout_4.addWidget(self.pB_imp_nx)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.lb_show_nx = QLabel(self.frame_2)
        sizePolicy.setHeightForWidth(self.lb_show_nx.sizePolicy().hasHeightForWidth())
        self.lb_show_nx.setSizePolicy(sizePolicy)
        self.verticalLayout_2.addWidget(self.lb_show_nx)
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(self.verticalSpacer_2)
        self.horizontalLayout.addWidget(self.frame_2)
        self.setWindowTitle("self")
        self.label.setText("<html><head/><body><p><span style=\" font-size:12pt; font-weig \
        ht:600; color:#0055ff;\">\u5916\u7bb1\u6807\u7b7e</span></p></body></html>")
        self.pB_edit_wx.setText("\u7f16\u8f91\u4fee\u6539")
        self.pB_imp_wx.setText("\u5bfc\u5165\u66ff\u6362")
        self.lb_show_wx.setText("<html><head/><body><p><br/></p></body></html>")
        self.label_5.setText("<html><head/><body><p><span style=\" font-size:12pt; font-we \
        ight:600; color:#ff5500;\">\u88c5\u7bb1\u660e\u7ec6\u6807\u7b7e</span></p></body></html>") \
        
        self.pB_edit_nx.setText("\u7f16\u8f91\u4fee\u6539")
        self.pB_imp_nx.setText("\u5bfc\u5165\u66ff\u6362")
        self.lb_show_nx.setText("<html><head/><body><p><br/></p></body></html>")


class Data_View(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(722, 612)
        self.horizontalLayout_3 = QHBoxLayout(self)
        self.groupBox = QGroupBox(self)
        self.groupBox.setMaximumSize(QSize(160, 16777215))
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.lE_code_serch = QLineEdit(self.groupBox)
        self.verticalLayout.addWidget(self.lE_code_serch)
        self.lW_codes = QListWidget(self.groupBox)
        self.verticalLayout.addWidget(self.lW_codes)
        self.horizontalLayout = QHBoxLayout()
        self.tB_page_last_code = QToolButton(self.groupBox)
        self.horizontalLayout.addWidget(self.tB_page_last_code)
        self.code_page = QLabel(self.groupBox)
        self.horizontalLayout.addWidget(self.code_page)
        self.tB_page_next_code = QToolButton(self.groupBox)
        self.horizontalLayout.addWidget(self.tB_page_next_code)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3.addWidget(self.groupBox)
        self.groupBox_2 = QGroupBox(self)
        self.groupBox_2.setMaximumSize(QSize(160, 16777215))
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.lE_box_serch = QLineEdit(self.groupBox_2)
        self.verticalLayout_2.addWidget(self.lE_box_serch)
        self.lW_boxs = QListWidget(self.groupBox_2)
        self.verticalLayout_2.addWidget(self.lW_boxs)
        self.horizontalLayout_3.addWidget(self.groupBox_2)
        self.groupBox_3 = QGroupBox(self)
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_3)
        self.tW_box_item = QListWidget(self.groupBox_3)
        self.verticalLayout_3.addWidget(self.tW_box_item)
        self.horizontalLayout_3.addWidget(self.groupBox_3)
        self.setWindowTitle("self")
        self.groupBox.setTitle("\u53d1\u8d27\u5355\u53f7")
        self.tB_page_last_code.setText("\u4e0a\u4e00\u9875")
        self.code_page.setText("0/0\u9875")
        self.tB_page_next_code.setText("\u4e0b\u4e00\u9875")
        self.groupBox_2.setTitle("\u88c5\u7bb1\u53f7")
        self.groupBox_3.setTitle("\u88c5\u7bb1\u660e\u7ec6")


class MainUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(900, 600)
        self.centralwidget = QWidget(self)
        self.gridLayout = QGridLayout(self.centralwidget)
        self.horizontalLayout = QHBoxLayout()
        self.label = QLabel(self.centralwidget)
        self.horizontalLayout.addWidget(self.label)
        self.lE_code_chose = QLineEdit(self.centralwidget)
        self.horizontalLayout.addWidget(self.lE_code_chose)
        self.label_2 = QLabel(self.centralwidget)
        self.horizontalLayout.addWidget(self.label_2)
        self.lE_show_adr = QLineEdit(self.centralwidget)
        self.lE_show_adr.setEnabled(False)
        self.horizontalLayout.addWidget(self.lE_show_adr)
        self.label_3 = QLabel(self.centralwidget)
        self.horizontalLayout.addWidget(self.label_3)
        self.lE_show_date = QLineEdit(self.centralwidget)
        self.lE_show_date.setEnabled(False)
        self.horizontalLayout.addWidget(self.lE_show_date)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 2)
        self.groupBox_3 = QGroupBox(self.centralwidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setMaximumSize(QSize(300, 300))
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_3)
        self.horizontalLayout_5 = QHBoxLayout()
        self.label_5 = QLabel(self.groupBox_3)
        self.horizontalLayout_5.addWidget(self.label_5)
        self.sB_box_num = QSpinBox(self.groupBox_3)
        self.sB_box_num.setMinimumSize(QSize(64, 0))
        self.sB_box_num.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.sB_box_num.setMaximum(1000)
        self.sB_box_num.setSingleStep(10)
        self.horizontalLayout_5.addWidget(self.sB_box_num)
        self.tB_box_num = QToolButton(self.groupBox_3)
        self.horizontalLayout_5.addWidget(self.tB_box_num)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QHBoxLayout()
        self.label_6 = QLabel(self.groupBox_3)
        self.horizontalLayout_6.addWidget(self.label_6)
        self.lE_box_size = QLineEdit(self.groupBox_3)
        self.horizontalLayout_6.addWidget(self.lE_box_size)
        self.tB_box_size = QToolButton(self.groupBox_3)
        self.horizontalLayout_6.addWidget(self.tB_box_size)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QHBoxLayout()
        self.label_4 = QLabel(self.groupBox_3)
        self.horizontalLayout_7.addWidget(self.label_4)
        self.lb_show_box_code = QLabel(self.groupBox_3)
        self.horizontalLayout_7.addWidget(self.lb_show_box_code)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(self.horizontalSpacer_3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_2 = QHBoxLayout()
        self.ldN_num = QLCDNumber(self.groupBox_3)
        self.ldN_num.setStyleSheet(u"border-color: rgb(0, 170, 255);\n"
"color: rgb(0, 0, 255);")
        self.horizontalLayout_2.addWidget(self.ldN_num)
        self.cLB_box = QCommandLinkButton(self.groupBox_3)
        self.horizontalLayout_2.addWidget(self.cLB_box)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.lW_show_sacn = QTableWidget(self.groupBox_3)
        if (self.lW_show_sacn.columnCount() < 2):
            self.lW_show_sacn.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.lW_show_sacn.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.lW_show_sacn.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.lW_show_sacn.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.lW_show_sacn.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.lW_show_sacn.horizontalHeader().setDefaultSectionSize(40)
        self.lW_show_sacn.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_2.addWidget(self.lW_show_sacn)
        self.gridLayout.addWidget(self.groupBox_3, 2, 1, 2, 1)
        self.lE_scan_lot = QLineEdit(self.centralwidget)
        self.gridLayout.addWidget(self.lE_scan_lot, 2, 0, 1, 1)
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setMaximumSize(QSize(300, 16777215))
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox_2)
        self.lW_show_boxs = QTableWidget(self.groupBox_2)
        if (self.lW_show_boxs.columnCount() < 2):
            self.lW_show_boxs.setColumnCount(2)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.lW_show_boxs.setHorizontalHeaderItem(0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.lW_show_boxs.setHorizontalHeaderItem(1, __qtablewidgetitem3)
        self.lW_show_boxs.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.lW_show_boxs.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.lW_show_boxs.horizontalHeader().setDefaultSectionSize(40)
        self.lW_show_boxs.horizontalHeader().setStretchLastSection(True)
        self.horizontalLayout_3.addWidget(self.lW_show_boxs)
        self.gridLayout.addWidget(self.groupBox_2, 4, 1, 1, 1)
        self.groupBox = QGroupBox(self.centralwidget)
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.tW_show_code = QTableWidget(self.groupBox)
        self.verticalLayout.addWidget(self.tW_show_code)
        self.gridLayout.addWidget(self.groupBox, 3, 0, 2, 1)
        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_2)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(self.horizontalSpacer)
        self.pB_data_serch = QPushButton(self.frame_2)
        self.horizontalLayout_4.addWidget(self.pB_data_serch)
        self.pB_port_set = QPushButton(self.frame_2)
        self.horizontalLayout_4.addWidget(self.pB_port_set)
        self.pB_rule_set = QPushButton(self.frame_2)
        self.horizontalLayout_4.addWidget(self.pB_rule_set)
        self.pB_btw_set = QPushButton(self.frame_2)
        self.horizontalLayout_4.addWidget(self.pB_btw_set)
        self.gridLayout.addWidget(self.frame_2, 0, 0, 1, 2)
        self.setCentralWidget(self.centralwidget)
        self.setWindowTitle("self")
        self.label.setText("\u53d1\u8d27\u5355\u53f7")
        self.label_2.setText("\u5730\u70b9\uff1a")
        self.label_3.setText("\u53d1\u8d27\u65e5\u671f")
        self.label_5.setText("\u88c5\u7bb1\u6570\u91cf\uff1a")
        self.tB_box_num.setText("\u786e\u5b9a")
        self.label_6.setText("\u88c5\u7bb1\u5c3a\u5bf8\uff1a")
        self.tB_box_size.setText("\u786e\u5b9a")
        self.label_4.setText("\u88c5\u7bb1\u660e\u7ec6\uff1a\u7bb1\u53f7\uff1a")
        self.lb_show_box_code.setText("<p><span style=\" font-size:11pt; font-weight:600;  \
        color:#0055ff;\">...</span></p>")
        self.cLB_box.setText("\u624b\u52a8\u88c5\u7bb1/\u5c3e\u7bb1")
        ___qtablewidgetitem = self.lW_show_sacn.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText("\u6279\u6b21")
        ___qtablewidgetitem1 = self.lW_show_sacn.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText("\u6570\u91cf")
        self.groupBox_2.setTitle("\u88c5\u7bb1\u5217\u8868")
        ___qtablewidgetitem2 = self.lW_show_boxs.horizontalHeaderItem(0)
        ___qtablewidgetitem2.setText("\u7bb1\u53f7")
        ___qtablewidgetitem3 = self.lW_show_boxs.horizontalHeaderItem(1)
        ___qtablewidgetitem3.setText("\u88c5\u7bb1\u6570")
        self.groupBox.setTitle("\u53d1\u8d27\u660e\u7ec6")
        self.pB_data_serch.setText("\u6570\u636e\u67e5\u8be2")
        self.pB_port_set.setText("\u7aef\u53e3\u8bbe\u7f6e")
        self.pB_rule_set.setText("\u6821\u9a8c\u89c4\u5219")
        self.pB_btw_set.setText("\u6a21\u677f\u7ba1\u7406")


class PortSet(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(390, 173)
        self.verticalLayout = QVBoxLayout(self)
        self.groupBox = QGroupBox(self)
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.gridLayout = QGridLayout()
        self.label = QLabel(self.groupBox)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_3 = QLabel(self.groupBox)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.cB_paritys = QComboBox(self.groupBox)
        self.gridLayout.addWidget(self.cB_paritys, 1, 1, 1, 1)
        self.label_5 = QLabel(self.groupBox)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.label_5, 2, 2, 1, 1)
        self.cB_stopbitses = QComboBox(self.groupBox)
        self.gridLayout.addWidget(self.cB_stopbitses, 2, 3, 1, 1)
        self.label_4 = QLabel(self.groupBox)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.cB_bytesizes = QComboBox(self.groupBox)
        self.gridLayout.addWidget(self.cB_bytesizes, 2, 1, 1, 1)
        self.label_2 = QLabel(self.groupBox)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.label_2, 1, 2, 1, 1)
        self.cB_baudrates = QComboBox(self.groupBox)
        self.gridLayout.addWidget(self.cB_baudrates, 1, 3, 1, 1)
        self.cB_port = QComboBox(self.groupBox)
        self.gridLayout.addWidget(self.cB_port, 0, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.horizontalLayout_2 = QHBoxLayout()
        self.cLB_connect = QCommandLinkButton(self.groupBox)
        self.horizontalLayout_2.addWidget(self.cLB_connect)
        self.cLB_save = QCommandLinkButton(self.groupBox)
        self.horizontalLayout_2.addWidget(self.cLB_save)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addWidget(self.groupBox)
        self.setWindowTitle("self")
        self.groupBox.setTitle("\u7aef\u53e3\u8bbe\u7f6e")
        self.label.setText("\u7aef\u53e3\u53f7\uff1a")
        self.label_3.setText("\u6821\u9a8c\u4f4d\uff1a")
        self.label_5.setText("\u505c\u6b62\u4f4d\uff1a")
        self.label_4.setText("\u6570\u636e\u4f4d\uff1a")
        self.label_2.setText("\u6ce2\u7279\u7387\uff1a")
        self.cLB_connect.setText("\u6253\u5f00")
        self.cLB_save.setText("\u4fdd\u5b58")


class RuleEdit(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(391, 203)
        self.verticalLayout_2 = QVBoxLayout(self)
        self.groupBox = QGroupBox(self)
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.formLayout = QFormLayout()
        self.label = QLabel(self.groupBox)
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)
        self.lE_norm = QLineEdit(self.groupBox)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lE_norm)
        self.label_2 = QLabel(self.groupBox)
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)
        self.sB_len = QSpinBox(self.groupBox)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sB_len.sizePolicy().hasHeightForWidth())
        self.sB_len.setSizePolicy(sizePolicy)
        self.sB_len.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.sB_len.setStepType(QAbstractSpinBox.DefaultStepType)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.sB_len)
        self.label_3 = QLabel(self.groupBox)
        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)
        self.horizontalLayout = QHBoxLayout()
        self.sB_lot_pre = QSpinBox(self.groupBox)
        self.sB_lot_pre.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.horizontalLayout.addWidget(self.sB_lot_pre)
        self.label_5 = QLabel(self.groupBox)
        self.horizontalLayout.addWidget(self.label_5)
        self.sB_lot_suf = QSpinBox(self.groupBox)
        self.sB_lot_suf.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.horizontalLayout.addWidget(self.sB_lot_suf)
        self.lE_show_lot = QLineEdit(self.groupBox)
        self.lE_show_lot.setEnabled(False)
        self.horizontalLayout.addWidget(self.lE_show_lot)
        self.formLayout.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout)
        self.label_4 = QLabel(self.groupBox)
        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_4)
        self.horizontalLayout_2 = QHBoxLayout()
        self.sB_num_pre = QSpinBox(self.groupBox)
        self.sB_num_pre.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.horizontalLayout_2.addWidget(self.sB_num_pre)
        self.label_6 = QLabel(self.groupBox)
        self.horizontalLayout_2.addWidget(self.label_6)
        self.sB_num_suf = QSpinBox(self.groupBox)
        self.sB_num_suf.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.horizontalLayout_2.addWidget(self.sB_num_suf)
        self.lE_show_num = QLineEdit(self.groupBox)
        self.lE_show_num.setEnabled(False)
        self.horizontalLayout_2.addWidget(self.lE_show_num)
        self.formLayout.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout_2)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout_3 = QHBoxLayout()
        self.cLB_save = QCommandLinkButton(self.groupBox)
        self.cLB_save.setAutoDefault(False)
        self.horizontalLayout_3.addWidget(self.cLB_save)
        self.cLB_cancle = QCommandLinkButton(self.groupBox)
        self.cLB_cancle.setAutoDefault(False)
        self.horizontalLayout_3.addWidget(self.cLB_cancle)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addWidget(self.groupBox)
        QWidget.setTabOrder(self.lE_norm, self.sB_len)
        QWidget.setTabOrder(self.sB_len, self.sB_lot_pre)
        QWidget.setTabOrder(self.sB_lot_pre, self.sB_lot_suf)
        QWidget.setTabOrder(self.sB_lot_suf, self.lE_show_lot)
        QWidget.setTabOrder(self.lE_show_lot, self.sB_num_pre)
        QWidget.setTabOrder(self.sB_num_pre, self.sB_num_suf)
        QWidget.setTabOrder(self.sB_num_suf, self.lE_show_num)
        QWidget.setTabOrder(self.lE_show_num, self.cLB_save)
        QWidget.setTabOrder(self.cLB_save, self.cLB_cancle)
        self.setWindowTitle("self")
        self.groupBox.setTitle("\u7f16\u8f91")
        self.label.setText("\u6807\u51c6\u6570\u636e\uff1a")
        self.label_2.setText("\u6570\u636e\u957f\u5ea6\uff1a")
        self.label_3.setText("\u6279\u6b21\u533a\u95f4\uff1a")
        self.label_5.setText("\u81f3")
        self.sB_lot_suf.setSuffix("")
        self.sB_lot_suf.setPrefix("")
        self.label_4.setText("\u6570\u91cf\u533a\u95f4\uff1a")
        self.label_6.setText("\u81f3")
        self.cLB_save.setText("\u786e\u5b9a")
        self.cLB_cancle.setText("\u53d6\u6d88")


class RuleSet(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(618, 465)
        self.verticalLayout = QVBoxLayout(self)
        self.tW_rule = QTableWidget(self)
        self.verticalLayout.addWidget(self.tW_rule)
        self.cLB_add_rule = QCommandLinkButton(self)
        self.verticalLayout.addWidget(self.cLB_add_rule)
        self.setWindowTitle("self")
        self.cLB_add_rule.setText("\u65b0\u589e")


