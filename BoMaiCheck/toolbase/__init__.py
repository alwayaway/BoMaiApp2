import os
import sys
import win32api

from ._db import Dbase, Semantide
from ._cfg import Cfgdbase, Cfgfile
from ._ser import *
from ._log import Log
from ._cry import *
from ._img import *


def check_dir(l_dir):
    for _ in l_dir:
        if not os.path.exists(_):
            os.mkdir(_)


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


class Var:
    def __init__(self):
        self._value = None

    def get(self):
        return self._value

    def set(self, _value):
        self._value = _value


class StrVar(Var):
    def __init__(self):
        super(StrVar, self).__init__()
        self._value = ''

    def set(self, _value):
        self._value = str(_value)


class IntVar(Var):
    def __init__(self):
        super(IntVar, self).__init__()
        self._value = 0

    def set(self, _value: int or float):
        self._value = int(_value)


class FloatVar(Var):
    def __init__(self):
        super(FloatVar, self).__init__()
        self._value = float(0.0)

    def set(self, _value: int or float):
        self._value = float(_value)


class NumVar(Var):
    def __init__(self):
        super(NumVar, self).__init__()
        self._value = float(0.0)

    def set(self, _value: int or float):
        tmp = int(_value)
        self._value = tmp if tmp == _value else float(_value)


class BoolVar(Var):
    def __init__(self):
        super(BoolVar, self).__init__()
        self._value = float(0.0)

    def set(self, _value: bool):
        if type(_value) is bool:
            self._value = _value
        else:
            raise ValueError(f"{_value} not bool type")


class CheckError(Exception):
    def __init__(self, msg=''):
        self._msg = msg

    def __str__(self):
        return self._msg


def str2num(_n: str):
    _temp = int(_n)
    return _temp if _temp == float(_n) else float(_n)


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
    except ValueError:
        return ValueError


def get_now(fmt="%Y-%m-%d %H:%M:%S"):
    return time.strftime(fmt, time.localtime())


def get_ZX_code():
    return get_code(6, 'C' + get_now("%y%m%d"))

