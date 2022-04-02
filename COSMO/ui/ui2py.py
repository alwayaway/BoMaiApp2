import os
import re


def file_name(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] in ('.ui',):
                L.append(file)
    return L


ABANDON = ['# ', 'import *', 'setObjectName', '##',
           'QMetaObject', 'objectName',
           # 'setWindowTitle',
           'retranslateUi']
WDG = ['Dialog', 'MainWindow']
FORMAT = {
    "Dialog": 'self',
    "MainWindow": 'self',
}
MAXLENGTH = 120


def ui2py(file, ui_dir):
    with open(file, mode='w', encoding='utf-8')as _w:
        _imp = [
            '# -*- coding: utf-8 -*-',
            'from PySide2.QtCore import *',
            'from PySide2.QtGui import *',
            'from PySide2.QtWidgets import *',
            '\n\n'
        ]
        re_translate = re.compile(r'QCoreApplication.translate\((.*?)\)')
        _w.write('\n'.join(_imp))
        for f in file_name(ui_dir):
            _py = f.split('.')[0]
            _cmd = f"pyside2-uic.exe -o {_py}.py {ui_dir}/{f}"
            os.system(_cmd)

            with open(f"{_py}.py", mode='r', encoding='utf-8')as _r:

                def get_rows():
                    for _ in _r.readlines():
                        yield _

                rows = get_rows()
                _row_temp = ''
                data = []
                _Q = 'object'
                for _row in rows:
                    _remove = False
                    for _aba in ABANDON:
                        if _aba in _row:
                            _remove = True
                            break
                    if _remove:
                        continue
                    elif 'class ' in _row:
                        for _wdg in WDG:
                            if _wdg in _row:
                                _Q = f'Q{_wdg}'
                                break
                        data.append(f'class {_py}({_Q}):\n')
                        continue
                    elif 'setupUi' in _row:
                        data.append('    def __init__(self):\n')
                        data.append('        super().__init__()\n')
                        continue
                    # elif 'def retranslateUi' in _row:
                    #     data.append('\n')
                    #     data.append('    def retranslateUi(self):\n')
                    elif 'QCoreApplication' in _row:
                        _row_temp = _row
                        while True:
                            try:
                                _temp = re_translate.findall(_row_temp)[0]
                                break
                            except:
                                _row_temp = _row_temp.strip('\n') + rows.__next__()

                        _row = _row_temp.replace(f'QCoreApplication.translate({_temp})',
                                                 _temp.split('", ')[1].strip(' u') + '"')
                    elif _row.strip() == '':
                        continue

                    if '___' in _row:
                        _row = _row.replace(';', '')

                    for _k, _v in FORMAT.items():
                        if _k in _row:
                            _row = _row.replace(_k, _v)

                    if len(_row) > MAXLENGTH:
                        _row = [_row[i:i + 90] for i in range(0, len(_row), 90)]
                        fst = _row[0]
                        fst = len(fst) - len(fst.lstrip())
                        _row = (' \\\n' + ' ' * fst).join(_row)
                    data.append(_row)

                _w.write(''.join(data))
                _w.write('\n\n')
            os.remove(f'{_py}.py')


ui2py(file='../ui.py', ui_dir="./")
