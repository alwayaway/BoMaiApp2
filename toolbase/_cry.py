# coding:utf-8

"""
Time:     ${DATE} ${TIME}
Author:   alwayaway
e-mail: alwayaway@foxmail.com
Version:  V 1.1
File:     ${NAME}.py
Describe: Config by sqlite3 or  file[.ini/.conf]
"""

import string
from random import choice
from hashlib import md5
from base64 import decodebytes, encodebytes
from itertools import cycle

_SYMBOLS__ = '-'  # 符号  可通过string.punctuation获取所有符号
_NUMBER__ = string.digits  # 数字
_LETTER__ = string.ascii_letters  # 英文字符'
_PWDSTR__ = _SYMBOLS__ + _NUMBER__ + _LETTER__  # 定义生成密码是组成密码元素的范围   字符+数字+大小写字母
_CODE__ = _NUMBER__ + _LETTER__

def generate_wd(wd_length: int or iter = (8, 9, 10, 11, 12)):
    """
    生成随机密码 8-12位
    :return: passwd
    """
    passwd_lst = []
    passwd_length = wd_length if type(wd_length) is int else choice(wd_length)
    for i in range(passwd_length):
        passwd_lst.append(choice(_PWDSTR__))  # 把循环出来的字符插入到passwd_lst列表中
    return ''.join(passwd_lst)  # 通过''.join(passwd_lst)合并列表中的所有元素组成新的字符串


def get_code(length: int, pre='', suf=''):
    code = []
    for i in range(length):
        code.append(choice(_CODE__))
    return pre + ''.join(code) + suf


def to_md5(text):
    """
    获取 text的 md5信息摘要，此md5值不可逆
    :param text: 待加密字符
    :return: md5信息摘要
    """
    md = md5()
    md.update(text.encode("utf-8"))
    return md.hexdigest()


def encrypt(data, key):
    """
    私有方法加密
    :param data:
    :param key:
    :return:
    """
    n = len(data)
    if len(key) < n:
        key += key * (n // len(key))
    key = [ord(i) for i in key]
    data = [ord(i) for i in data]
    endata = ""
    for k, v in zip(key, data):
        endata += chr(k + v)
    endata = encodebytes(endata.encode()).decode().strip()
    return endata


def decrypt(data, key):
    """
    私有方法解密
    :param data:
    :param key:
    :return:
    """
    data = decodebytes(data.encode()).decode()
    n = len(data)
    if len(key) < n:
        key += key * (n // len(key))
    key = [ord(i) for i in key]
    data = [ord(i) for i in data]
    endata = ""
    for k, v in zip(key, data):
        endata += chr(v - k)
    return endata


def datcrypt(source, key):
    """
    文标加密算法，加密后显示乱码，使用密钥重新加密后还原
    :param source: 文本
    :param key: 密钥
    :return:
    """
    temp = cycle(key)
    return ''.join([chr(ord(ch) ^ ord(next(temp))) for ch in source])


if __name__ == '__main__':
    data0 = generate_wd(100)
    print(data0)
    data1 = datcrypt(data0, 'alwayaway')
    print(data1)
    data2 = datcrypt(data1, 'alwayaway')
    print(data2)
    data3 = encrypt(data0, 'alwayaway')
    print(data3)
    data4 = decrypt(data3, 'alwayaway')
    print(data4)
