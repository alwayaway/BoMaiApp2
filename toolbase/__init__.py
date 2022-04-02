import os
import sys
import time

from ._cfg import Cfgdbase, Cfgfile
from ._cry import *
from ._db import Dbase, Semantide
from ._img import *
from ._log import Log

try:
    import pyi_splash
except:
    class _Splash:
        def update_text(self, text):
            print('pyi_splash: ', str(text))

        def close(self):
            print('close pyi_splash')


    pyi_splash = _Splash()


def loaded_splash(text):
    pyi_splash.update_text(text)


def loaded_close():
    pyi_splash.close()


def check_dir(l_dir):
    for _ in l_dir:
        if not os.path.exists(_):
            os.mkdir(_)


def base_path(filename):  # 生成资源文件目录访问路径
    relative_path = os.path.join(filename)
    if getattr(sys, 'frozen', False):  # 判断sys中是否存在frozen变量,
        _path = getattr(sys, '_MEIPASS')
    else:
        _path = os.path.abspath(".")
    return os.path.join(_path, relative_path)


class Pro_file:
    def __init__(self):
        self._queue = []
        self._params = {}
        self._state = True

    def __bool__(self):
        return self._state

    def get(self, *args):
        return (self._params.get(_) for _ in args)

    def set(self, **kwargs):
        for k, v in kwargs.items():
            self._params[k] = v

    def add(self, que):
        return self._queue.insert(0, que)

    def remove(self, que):
        return self._queue.remove(que)

    def pop(self):
        return self._queue.pop()

    def length(self):
        return len(self._queue)

    def clear(self):
        self._queue.clear()

    def close(self):
        self.clear()
        self._state = False
        return self._state


def str2num(_n: str):
    _tmp_n, _tmp_f = int(_n), float(_n)
    return _tmp_n if _tmp_n == _tmp_f else _tmp_f


def str4mat(_str, _dict):
    try:
        return _str.format(**_dict)
    except KeyError as _e:
        _e = f'{_e}'.strip("'")
        _str = _str.replace('{%s}' % _e, '{{%s}}' % _e)
        return _str.format(**_dict)


def arr_next(init: str, array: list):
    try:
        if init:
            temp = array[array.index(init[-1]) + 1]
            return init[0:-1] + temp
        else:
            return init
    except IndexError:
        return arr_next(init[0:-1], array) + array[0]


def get_now(fmt="%Y-%m-%d %H:%M:%S"):
    return time.strftime(fmt, time.localtime())


class VarValue:
    def __init__(self, v=None):
        self._v = v

    def set(self, v):
        self._v = v

    def get(self):
        return self._v

    def __bool__(self):
        if self._v:
            return True
        else:
            return False


def Na2Str(Na):
    if Na is None:
        return ''
    else:
        return str(Na)

