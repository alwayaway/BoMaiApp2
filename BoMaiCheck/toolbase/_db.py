import sqlite3


class Dbase:
    def __init__(self, db_file, *args, init_db: list or tuple or str, check_same_thread=False, **kwargs):
        """
        初始化配置
        :param db_file: dbase的存储位置
        :param args: 其他打开sqlite3的参数
        :param check_same_thread: 设置check_same_thread=False 防止多线程使用时无法不同线程无法使用
        :param init_db: 初始化
        :param kwargs: 其他打开sqlite3的参数
        """
        self.conn = sqlite3.connect(db_file, *args, check_same_thread=check_same_thread, **kwargs)
        self._init_db(init_db)

    def reload(self, db_file, *args, init_db: list or tuple or str, check_same_thread=False, **kwargs):
        self.conn = sqlite3.connect(db_file, *args, check_same_thread=check_same_thread, **kwargs)
        self._init_db(init_db)

    def _init_db(self, init_db: list or tuple or str):
        if type(init_db) is str:
            self.conn.executescript(init_db)
        else:
            for init_sql in init_db:
                self.conn.execute(init_sql)

    def execute(self, sql, *args):
        cur = self.conn.cursor()
        try:
            cur.execute(sql, args)
            self.commit()
            return Semantide(queryset=cur.fetchall(), msg=f'SQL:{sql}\nParams:{args}')
        except Exception as _e:
            self.rollback()
            return Semantide(False, error=_e, msg=f'SQL:{sql}\nParams:{args}')
        finally:
            cur.close()

    def exec_sql(self, sql):
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
            self.commit()
            return Semantide(queryset=cur.fetchall(), msg=f'SQL:{sql}')
        except Exception as _e:
            self.rollback()
            return Semantide(False, error=_e, msg=f'SQL:{sql}')
        finally:
            cur.close()

    def executemany(self, sql, *args):
        cur = self.conn.cursor()
        try:
            cur.executemany(sql, args)
            self.commit()
            return Semantide(queryset=cur.fetchall(), msg=f'SQL:{sql}\nParams:{args}')
        except Exception as _e:
            self.rollback()
            return Semantide(False, error=_e, msg=f'SQL:{sql}\nParams:{args}')
        finally:
            cur.close()

    def get_cursor(self):
        return self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def rollback(self, *args, **kwargs):
        self.conn.rollback(*args, **kwargs)

    def close(self):
        self.conn.close()


class Semantide:
    """信息载体类"""

    def __init__(self, _bool=True, queryset=None, error=None, msg='null'):
        """
        :param _bool: 执行是否成功
        :param queryset: 返回的结果集
        :param error: 执行失败参数的异常
        :param msg: 执行信息
        """
        self._queryset = queryset if queryset else ()
        self._bool = _bool
        self._msg = msg
        self._error = error

    def __bool__(self):
        return self._bool

    def __str__(self):
        return self._msg

    def _item_queryset(self):
        for value in self._queryset:
            yield value

    def __iter__(self):
        return self._item_queryset()

    def __getitem__(self, item=None):
        return self._queryset[item]

    def error(self):
        return self._error

    def get(self):
        return self._queryset

    def __len__(self):
        return len(self._queryset)
