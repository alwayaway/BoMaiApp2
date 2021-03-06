# -*- coding: utf-8 -*-
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


# noinspection PyArgumentList
class AddBtw(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(400, 142)
        self.verticalLayout = QVBoxLayout(self)
        self.formLayout = QFormLayout()
        self.formLayout.setContentsMargins(-1, 20, -1, -1)
        self.label = QLabel(self)
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)
        self.lE_btw_name = QLineEdit(self)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lE_btw_name)
        self.label_2 = QLabel(self)
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)
        self.horizontalLayout_2 = QHBoxLayout()
        self.lE_btw_file = QLineEdit(self)
        self.horizontalLayout_2.addWidget(self.lE_btw_file)
        self.tB_chose_btw = QToolButton(self)
        self.horizontalLayout_2.addWidget(self.tB_chose_btw)
        self.formLayout.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_2)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 16)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(self.horizontalSpacer)
        self.pB_sure = QPushButton(self)
        self.horizontalLayout.addWidget(self.pB_sure)
        self.pB_cancel = QPushButton(self)
        self.horizontalLayout.addWidget(self.pB_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.setWindowTitle("\u65b0\u589e")
        self.label.setText("\u6a21\u677f\u540d\u79f0\uff1a")
        self.label_2.setText("\u6a21\u677f\u6587\u4ef6\uff1a")
        self.tB_chose_btw.setText("...")
        self.pB_sure.setText("\u786e\u5b9a")
        self.pB_cancel.setText("\u53d6\u6d88")


# noinspection PyArgumentList
class Base(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(462, 405)
        self.verticalLayout = QVBoxLayout(self)
        self.lE_serch = QLineEdit(self)
        self.verticalLayout.addWidget(self.lE_serch)
        self.tW_btw_base = QTableWidget(self)
        if (self.tW_btw_base.columnCount() < 2):
            self.tW_btw_base.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tW_btw_base.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tW_btw_base.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tW_btw_base.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.tW_btw_base)
        self.cLK_add_btw = QCommandLinkButton(self)
        self.verticalLayout.addWidget(self.cLK_add_btw)
        self.setWindowTitle("\u6a21\u677f\u4ed3\u5e93")
        self.lE_serch.setPlaceholderText("\u68c0\u7d22\u6a21\u677f")
        ___qtablewidgetitem = self.tW_btw_base.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText("\u6807\u7b7e\u540d\u79f0")
        ___qtablewidgetitem1 = self.tW_btw_base.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText("\u6761\u7801\u7ec4\u6210")
        self.cLK_add_btw.setText("\u65b0\u589e")


# noinspection PyArgumentList
class ChoseBtw(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(400, 300)
        self.verticalLayout = QVBoxLayout(self)
        self.tW_base = QTableWidget(self)
        if (self.tW_base.columnCount() < 1):
            self.tW_base.setColumnCount(1)
        __qtablewidgetitem = QTableWidgetItem()
        self.tW_base.setHorizontalHeaderItem(0, __qtablewidgetitem)
        self.tW_base.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.tW_base)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 6, -1, 10)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(self.horizontalSpacer)
        self.pB_sure = QPushButton(self)
        self.horizontalLayout.addWidget(self.pB_sure)
        self.pB_cancel = QPushButton(self)
        self.horizontalLayout.addWidget(self.pB_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.setWindowTitle("\u6a21\u677f\u53d8\u66f4")
        ___qtablewidgetitem = self.tW_base.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText("\u6a21\u677f\u540d\u79f0")
        self.pB_sure.setText("\u786e\u5b9a")
        self.pB_cancel.setText("\u53d6\u6d88")


# noinspection PyArgumentList
class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.centralwidget = QWidget(self)
        self.Ly_main = QVBoxLayout(self.centralwidget)
        self.Ly_hor_title = QHBoxLayout()
        self.lb_title = QLabel(self.centralwidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_title.sizePolicy().hasHeightForWidth())
        self.lb_title.setSizePolicy(sizePolicy)
        self.lb_title.setMinimumSize(QSize(0, 60))
        self.Ly_hor_title.addWidget(self.lb_title)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.Ly_hor_title.addItem(self.horizontalSpacer)
        self.pB_btw_base = QPushButton(self.centralwidget)
        self.Ly_hor_title.addWidget(self.pB_btw_base)
        self.pB_rep_data = QPushButton(self.centralwidget)
        self.Ly_hor_title.addWidget(self.pB_rep_data)
        self.pB_cfg_data = QPushButton(self.centralwidget)
        self.Ly_hor_title.addWidget(self.pB_cfg_data)
        self.pB_about = QPushButton(self.centralwidget)
        self.Ly_hor_title.addWidget(self.pB_about)
        self.Ly_main.addLayout(self.Ly_hor_title)
        self.Ly_ver_btw = QVBoxLayout()
        self.horizontalLayout_3 = QHBoxLayout()
        self.label_7 = QLabel(self.centralwidget)
        self.horizontalLayout_3.addWidget(self.label_7)
        self.dTE_curr_time = QDateTimeEdit(self.centralwidget)
        self.dTE_curr_time.setCalendarPopup(True)
        self.horizontalLayout_3.addWidget(self.dTE_curr_time)
        self.label_6 = QLabel(self.centralwidget)
        self.horizontalLayout_3.addWidget(self.label_6)
        self.lE_btw_used = QLineEdit(self.centralwidget)
        self.lE_btw_used.setEnabled(False)
        self.horizontalLayout_3.addWidget(self.lE_btw_used)
        self.tB_btw_change = QToolButton(self.centralwidget)
        self.horizontalLayout_3.addWidget(self.tB_btw_change)
        self.Ly_ver_btw.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QHBoxLayout()
        self.verticalLayout = QVBoxLayout()
        self.tW_btw_params = QTableWidget(self.centralwidget)
        if (self.tW_btw_params.columnCount() < 2):
            self.tW_btw_params.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tW_btw_params.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tW_btw_params.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tW_btw_params.sizePolicy().hasHeightForWidth())
        self.tW_btw_params.setSizePolicy(sizePolicy1)
        self.tW_btw_params.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.tW_btw_params)
        self.formLayout = QFormLayout()
        self.label_2 = QLabel(self.centralwidget)
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_2)
        self.sB_copy_num = QSpinBox(self.centralwidget)
        self.sB_copy_num.setMinimum(1)
        self.sB_copy_num.setMaximum(10)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.sB_copy_num)
        self.label_3 = QLabel(self.centralwidget)
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_3)
        self.sB_print_num = QSpinBox(self.centralwidget)
        self.sB_print_num.setMinimum(1)
        self.sB_print_num.setMaximum(6000)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.sB_print_num)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.mdiArea = QMdiArea(self.centralwidget)
        sizePolicy2 = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.mdiArea.sizePolicy().hasHeightForWidth())
        self.mdiArea.setSizePolicy(sizePolicy2)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.horizontalLayout_2.addWidget(self.mdiArea)
        self.Ly_ver_btw.addLayout(self.horizontalLayout_2)
        self.Ly_main.addLayout(self.Ly_ver_btw)
        self.Ly_hor_print = QHBoxLayout()
        self.cLK_params_check = QCommandLinkButton(self.centralwidget)
        self.Ly_hor_print.addWidget(self.cLK_params_check)
        self.cLK_print_nocheck = QCommandLinkButton(self.centralwidget)
        self.Ly_hor_print.addWidget(self.cLK_print_nocheck)
        self.cLK_print_check = QCommandLinkButton(self.centralwidget)
        self.Ly_hor_print.addWidget(self.cLK_print_check)
        self.Ly_main.addLayout(self.Ly_hor_print)
        self.tB_show = QTextBrowser(self.centralwidget)
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.tB_show.sizePolicy().hasHeightForWidth())
        self.tB_show.setSizePolicy(sizePolicy3)
        self.tB_show.setMaximumSize(QSize(16777215, 100))
        self.Ly_main.addWidget(self.tB_show)
        self.setCentralWidget(self.centralwidget)
        self.setWindowTitle("self")
        self.lb_title.setText("<html><head/><body><p><span style=\" font-size:12pt; font-weight:600; color:#00aa00;\">By ELD LABEL PRINT MANGER V1.1.0</span></p></body></html>")
        self.pB_btw_base.setText("\u6a21\u677f\u4ed3\u5e93")
        self.pB_rep_data.setText("\u9632\u91cd\u8d44\u6599")
        self.pB_cfg_data.setText("\u7cfb\u7edf\u8bbe\u7f6e")
        self.pB_about.setText("\u5173\u4e8e\u7a0b\u5e8f")
        self.label_7.setText("<html><head/><body><p><span style=\" font-size:16pt; font-weight:600; color:#0055ff;\">\u65e5\u671f\u53d8\u66f4:</span></p></body></html>")
        self.dTE_curr_time.setDisplayFormat("yyyy-MM-dd")
        self.label_6.setText("<html><head/><body><p><span style=\" font-size:16pt; font-weight:600; color:#aa00ff;\">\u5f53\u524d\u4f7f\u7528\u6807\u7b7e\uff1a</span></p></body></html>")
        self.tB_btw_change.setText("\u53d8\u66f4")
        ___qtablewidgetitem = self.tW_btw_params.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText("\u53c2\u6570\u540d\u79f0")
        ___qtablewidgetitem1 = self.tW_btw_params.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText("\u53c2\u6570\u6570\u636e")
        self.label_2.setText("\u590d\u5236\u6570\u91cf")
        self.label_3.setText("\u6253\u5370\u6570\u91cf")
        self.cLK_params_check.setText("\u6570\u636e\u68c0\u67e5")
        self.cLK_print_nocheck.setText("\u65e0\u6821\u9a8c\u8865\u7801\u5217\u5370")
        self.cLK_print_check.setText("\u5f00\u59cb\u5217\u5370")


# noinspection PyArgumentList
class RepView(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(510, 560)
        self.verticalLayout = QVBoxLayout(self)
        self.horizontalLayout_2 = QHBoxLayout()
        self.lE_search = QLineEdit(self)
        self.horizontalLayout_2.addWidget(self.lE_search)
        self.pB_search = QPushButton(self)
        self.horizontalLayout_2.addWidget(self.pB_search)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.tableWidget = QTableWidget(self)
        if (self.tableWidget.columnCount() < 1):
            self.tableWidget.setColumnCount(1)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.tableWidget)
        self.horizontalLayout = QHBoxLayout()
        self.pB_del_sel = QPushButton(self)
        self.pB_del_sel.setEnabled(False)
        self.horizontalLayout.addWidget(self.pB_del_sel)
        self.pB_del_all = QPushButton(self)
        self.pB_del_all.setEnabled(False)
        self.horizontalLayout.addWidget(self.pB_del_all)
        self.pB_page_last = QPushButton(self)
        self.pB_page_last.setEnabled(False)
        self.horizontalLayout.addWidget(self.pB_page_last)
        self.pB_page_next = QPushButton(self)
        self.pB_page_next.setEnabled(False)
        self.horizontalLayout.addWidget(self.pB_page_next)
        self.sB_page = QSpinBox(self)
        self.sB_page.setEnabled(True)
        self.sB_page.setMinimum(1)
        self.sB_page.setMaximum(1)
        self.horizontalLayout.addWidget(self.sB_page)
        self.pB_page_change = QPushButton(self)
        self.pB_page_change.setEnabled(False)
        self.horizontalLayout.addWidget(self.pB_page_change)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.setWindowTitle("\u9632\u91cd\u4ed3\u5e93")
        self.lE_search.setPlaceholderText("\u8f93\u5165\u68c0\u7d22\u6761\u4ef6")
        self.pB_search.setText("\u641c\u7d22")
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText("\u5386\u53f2\u8bb0\u5f55")
        self.pB_del_sel.setText("\u5220\u9664\u9009\u4e2d")
        self.pB_del_all.setText("\u5220\u9664\u5f53\u524d\u9875")
        self.pB_page_last.setText("\u4e0a\u4e00\u9875")
        self.pB_page_next.setText("\u4e0b\u4e00\u9875")
        self.sB_page.setSuffix(" / 1 \u9875")
        self.sB_page.setPrefix("\u7b2c")
        self.pB_page_change.setText("\u8df3\u8f6c")


