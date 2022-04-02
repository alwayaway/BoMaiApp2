# coding:utf-8

"""
Time:     ${DATE} ${TIME}
Author:   alwayaway
e-mail: alwayaway@foxmail.com
Version:  V 1.1
File:     ${NAME}.py
Describe: Config by sqlite3 or  file[.ini/.conf]
"""

import sqlite3
import configparser as _conf


class Cfgdbase:
    """Config by sqlite3  """

    def __init__(self, dbfile, *args, check_same_thread=False, **kwargs):
        """
        初始化配置 设置check_same_thread=False 防止多线程使用时无法不同线程无法使用
        """
        self.conf = sqlite3.connect(dbfile, *args, check_same_thread=check_same_thread, **kwargs)
        self.initdb()

    def initdb(self):
        """
        初始化配置DB结构
        :return:
        """
        self.conf.execute("""
                CREATE TABLE IF NOT EXISTS [Conf](
                    [id] integer PRIMARY KEY AUTOINCREMENT NOT NULL,
                    [section]	varchar(255) NOT NULL COLLATE NOCASE,
                    [option]	varchar(255) NOT NULL COLLATE NOCASE,
                    [value]	varchar(255),
                    unique(section, option)
                );
                """)

    def load(self, dbfile, *args, check_same_thread=False, **kwargs):
        """
        加载配置文件
        :return:
        """
        self.close()
        self.__init__(dbfile, *args, check_same_thread=check_same_thread, **kwargs)

    def save(self):
        """
        保存修改的配置
        :return:
        """
        self.conf.commit()

    def getOpts(self, section):
        """
        获取配置参数
        :param section: 节点
        :return: value
        """
        cur = self.conf.cursor()
        try:
            _sql = 'select option, value from Conf where section=?'
            cur.execute(_sql, (section,))
            res = cur.fetchall()
            return {kv[0]: kv[1] for kv in res}
        except Exception as e:
            return e
        finally:
            cur.close()

    def get(self, section, option, value=None, save=True):
        """
        获取配置参数
        :param section: 节点
        :param option:  选项
        :param value:   参数
        :return: value
        """
        value = '' if value is None else value
        cur = self.conf.cursor()
        try:
            _sql = 'select value from Conf where section=? and option=?'
            cur.execute(_sql, (section, option))
            res = cur.fetchall()
            if res:
                return res[0][0]
            elif value is None:
                return None
            elif save:
                return self.set(section, option, value)
            else:
                return value
        except Exception as e:
            return e
        finally:
            cur.close()

    def set(self, section, option, value, auto=True):
        """
        设置配置参数
        :param section: 节点
        :param option:  选项
        :param value:   参数
        :param auto:    自动保存
        :return: 如果不存在该节点和选项 则返回value 否则无返回值
        """
        cur = self.conf.cursor()
        try:
            _sql = 'update Conf set value=? where section=? and option=?'
            cur.execute(_sql, (value, section, option))
            if cur.rowcount == 0:
                _sql = 'insert into Conf (section, option, value) values(?, ?, ?)'
                cur.execute(_sql, (section, option, value))
            return value
        except Exception as e:
            self.conf.rollback()
            print(e)
            return e
        finally:
            cur.close()
            if auto:
                self.save()

    def remove(self, section, option):
        """
        获取配置参数
        :param section: 节点
        :param option:  选项
        :param value:   参数
        :return: value
        """
        cur = self.conf.cursor()
        try:
            _sql = 'delete from Conf where section=? and option=?'
            cur.execute(_sql, (section, option))
            self.save()
        except Exception as e:
            self.conf.rollback()
            return e
        finally:
            cur.close()

    def close(self):
        """退出时务必先关闭连接"""
        self.conf.close()


class Cfgfile:
    """Config by file[.ini/.conf] """

    def __init__(self, file: str = None, encoding: str = 'utf-8'):
        """
        初始化配置
        :param encoding: 字符编码
        :param file: 预加载的配置文件路径
        """
        self.file = file
        self.encoding = encoding
        self.conf = _conf.ConfigParser()
        if file:
            self.conf.read(file, encoding=encoding)

    def load(self, file: str, encoding: str = 'utf-8'):
        """
        预加载配置文件
        :param encoding: 字符编码
        :param file: 预加载的配置文件路径
        """
        self.__init__(file, encoding)

    def save(self):
        """
        保存修改的配置文件
        :return: None
        """
        with open(self.file, mode='w', encoding=self.encoding)as f:
            self.conf.write(f)

    def get(self, section: str, option: str, init: str = ""):
        """
        获取配置参数
        :param init: 不存在该配置目标时的默认值
        :param section: 章节
        :param option: 选项
        :return: init or values
        """
        try:
            return self.conf.get(section, option)
        except _conf.NoSectionError:
            self.conf[section] = {}
            self.conf[section][option] = init
        except _conf.NoOptionError:
            self.conf[section][option] = init
        self.save()
        return init

    def set(self, section: str, option: str, value: str, save: bool = True):
        """
        更新配置参数
        :param value: 更新参数
        :param section: 更新节点
        :param option: 更新选项
        :param save: 是否保存到配置文件
        :return: None
        """
        try:
            self.conf.set(section, option, value)
        except _conf.NoSectionError:
            self.conf[section] = {}
            self.conf[section][option] = value
        except _conf.NoOptionError:
            self.conf[section][option] = value
        if save:
            self.save()

    def close(self):
        pass


if __name__ == '__main__':
    pass
    # conf = Cfgdbase('config.db')
    # print(conf.get("A", "B", 10000))
    # print(conf.get("A", "c", '中文测试'))
    # print(conf.get("A", "D", 'English'))
    # conf.set("A", "B", "-9999")
    # print(conf.get("A", "B"))
    # conf.close()
    #
    # conf2 = Cfgfile('config.ini')
    # print(conf2.get("A", "B", '10000'))
    # print(conf2.get("A", "c", '中文测试'))
    # print(conf2.get("A", "D", 'English'))
    # conf2.set("A", "B", "-9999")
    # print(conf2.get("A", "B"))
