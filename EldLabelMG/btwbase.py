import sqlite3


def get_item(*args):
    max_row = len(args)
    idx = 0
    while idx < max_row:
        yield args[idx: idx + 100]
        idx += 100


class BtwBase:
    def __init__(self, db_file, *args, check_same_thread=False, **kwargs):
        """初始化配置 设置check_same_thread=False 防止多线程使用时无法不同线程无法使用"""
        self.db = sqlite3.connect(db_file, *args, check_same_thread=check_same_thread, **kwargs)
        self.init_db()

    def init_db(self):
        """初始化配置DB结构"""
        init = ["""
                CREATE TABLE IF NOT EXISTS [BtwBase](
                    [id] integer PRIMARY KEY AUTOINCREMENT NOT NULL,
                    [btwname]	varchar(125) NOT NULL COLLATE NOCASE UNIQUE ,
                    [btwdict]	varchar(255) NOT NULL COLLATE NOCASE,
                    [btwblod]	BLOB
                );""",
                """
                CREATE TABLE IF NOT EXISTS [RepBase](
                    [id] integer PRIMARY KEY AUTOINCREMENT NOT NULL,
                    [bar]	varchar(255) NOT NULL COLLATE NOCASE UNIQUE
                );
                """]

        for it in init:
            self.db.execute(it)

    def get_btw(self, name):
        cur = self.db.cursor()
        try:
            _sql = 'select btwdict, btwblod from BtwBase where btwname=?'
            cur.execute(_sql, (name,))
            res = cur.fetchall()
            if res:
                return {
                    "UNIQUE": res[0][0],
                    'btw': res[0][1]
                }
            else:
                return {}
        except Exception as e:
            raise e
        finally:
            cur.close()

    def get_btwS(self, *args):
        """
        :param args: btwname, btwdict, btwblod
        :return:
        """
        cur = self.db.cursor()
        try:
            _sql = 'select %s from BtwBase' % ','.join(args)
            cur.execute(_sql)
            return cur.fetchall()
        except Exception as e:
            raise e
        finally:
            cur.close()

    # def update_btw(self, name, bard, file):
    #     cur = self.db.cursor()
    #     # noinspection PyBroadException
    #     try:
    #         with open(file, mode='rb')as _rb:
    #             _sql = 'update BtwBase set btwdict=?, btwblod=? where btwname=?'
    #             cur.execute(_sql, (bard, _rb.read(), name))
    #         self.db.commit()
    #         return cur.rowcount
    #     except Exception:
    #         return -1
    #     finally:
    #         cur.close()

    def update_btw(self, name, **kwargs):
        """
        :param name:
        :param kwargs: btwdict, btwblod
        :return:
        """
        cur = self.db.cursor()
        if 'btwblod' in kwargs:
            with open(kwargs['btwblod'], mode='rb')as _rb:
                kwargs['btwblod'] = _rb.read()
        # noinspection PyBroadException
        try:
            _sql = 'update BtwBase set %s where btwname=?' % ','.join([f'{k}=?' for k in kwargs.keys()])
            cur.execute(_sql, (*kwargs.values(), name))
            self.db.commit()
            return cur.rowcount
        except Exception:
            return -1
        finally:
            cur.close()

    def exist_btw(self, name):
        cur = self.db.cursor()
        # noinspection PyBroadException
        try:
            _sql = 'select * from BtwBase where btwname=?'
            cur.execute(_sql, (name,))
            return len(cur.fetchall())
        except Exception:
            return -1
        finally:
            cur.close()

    def add_btw(self, name, bard, file):
        cur = self.db.cursor()
        # noinspection PyBroadException
        try:
            with open(file, mode='rb')as _rb:
                # if self.exist_btw(name):
                #     _sql = 'update BtwBase set btwdict=?, btwblod=? where btwname=?'
                # else:
                #     _sql = 'insert into BtwBase (btwdict, btwblod, btwname) values (?,?,?)'
                _sql = 'insert into BtwBase (btwdict, btwblod, btwname) values (?,?,?)'
                cur.execute(_sql, (bard, _rb.read(), name))
                self.db.commit()
            return True
        except Exception:
            return False
        finally:
            cur.close()

    def del_btw(self, name):
        cur = self.db.cursor()
        # noinspection PyBroadException
        try:
            _sql = 'delete from BtwBase where btwname=?'
            cur.execute(_sql, (name,))
            self.db.commit()
            return len(cur.fetchall())
        except Exception:
            return -1
        finally:
            cur.close()

    def add_Rep(self, bar):
        cur = self.db.cursor()
        # noinspection PyBroadException
        try:
            _sql = 'insert into RepBase (bar) values (?)'
            cur.execute(_sql, (bar, ))
            self.db.commit()
            return True
        except Exception:
            return False
        finally:
            cur.close()

    def del_Rep(self, *bars):
        cur = self.db.cursor()
        # noinspection PyBroadException
        try:
            for barSet in get_item(*bars):
                _sql = 'delete from RepBase where bar in (%s)' % ','.join(('?' for _ in range(len(barSet))))
                cur.execute(_sql, barSet)
            self.db.commit()
            return True
        except Exception as _del_err:
            self.db.rollback()
            raise _del_err
            return False
        finally:
            cur.close()

    def exist_Rep(self, *bars):
        cur = self.db.cursor()
        # noinspection PyBroadException
        try:
            for barSet in get_item(*bars):
                _sql = 'select bar from RepBase where bar in (%s)' % ','.join(('?' for _ in range(len(barSet))))
                cur.execute(_sql, barSet)
                res = cur.fetchall()
                if len(res) > 0:
                    return res
            return ()
        except Exception as _err:
            return _err
        finally:
            cur.close()

    def searchRep(self, search, lit1, lit2):
        cur = self.db.cursor()
        # noinspection PyBroadException
        try:
            _sql = f"select bar from RepBase where bar like '{search}%' limit ?, ?"
            cur.execute(_sql, (lit1, lit2))
            return cur.fetchall()
        except Exception:
            raise
        finally:
            cur.close()

    def getRepLen(self, search):
        cur = self.db.cursor()
        # noinspection PyBroadException
        try:
            _sql = f"select count(*) from RepBase where bar like '{search}%'"
            cur.execute(_sql)
            return cur.fetchall()[0][0]
        except Exception:
            raise
        finally:
            cur.close()

    def close(self):
        # cur = self.db.cursor()
        # # noinspection PyBroadException
        # try:
        #     _sql = 'VACUUM'
        #     cur.execute(_sql)
        # except Exception:
        #     pass
        # finally:
        #     cur.close()
        self.db.close()
