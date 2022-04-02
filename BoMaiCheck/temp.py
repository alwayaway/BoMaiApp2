#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pyodbc


class MSSQL:
    class Result:
        def __init__(self, result, is_success=True, msg='', err=None):
            self.value = result
            self._bool = is_success
            self._msg = msg
            self._err = err

        def __bool__(self):
            return self._bool

        def __str__(self):
            return self._msg

        def __repr__(self):
            return self._msg

        def error(self):
            return self._err

    def __init__(self,host,user,pwd,db='master', charset='utf8'):
        self._host = host
        self._user = user
        self._pwd = pwd
        self._db = db
        self._charset = charset
        if not self._db:
            raise(NameError,"没有设置数据库信息")
        conn_info = 'DRIVER={SQL Server};DATABASE=%s;SERVER=%s;UID=%s;PWD=%s' % (self._db, self._host, self._user, self._pwd)
        self.conn = pyodbc.connect(conn_info, charset=self._charset)

    def _get_connect(self):
        cur = self.conn.cursor()
        if not cur:
            raise(NameError,"连接数据库失败")
        else:
            return cur

    def _exec_query(self, sql, *args):
        cur = self._get_connect()
        try:
            cur.execute(sql, *args)
            resList = cur.fetchall()
            return self.Result(resList, msg=f'{cur.messages}')
        except Exception as _err:
            return self.Result(None, False, msg=f'{cur.messages}', err=_err)
        finally:
            cur.close()

    def exec_query_tuple(self, sql, *args):
        """结果集以元组返回"""
        return self._exec_query(sql, *args)

    def exec_query_dict(self, sql, *args):
        result = []
        exec_res = self._exec_query(sql, *args)
        if exec_res:
            for row in exec_res.value:
                result.append( dict([(desc[0], row[index]) for index, desc in enumerate(row.cursor_description)]) )
            exec_res.value = result

        return exec_res

    def exec_sql(self, sql, *args):
        cur = self._get_connect()
        try:
            cur.execute(sql, *args)
            cur.commit()
            return self.Result(None, msg=f'非查询语句执行: {cur.messages}')
        except Exception as _err:
            cur.rollback()
            return self.Result(None, False, msg=f'非查询语句执行: {cur.messages}', err=_err)
        finally:
            cur.close()

    def close(self):
        self.conn.close()

    def exec_with_transaction(self):
        return self._ExecWithTransaction(self._get_connect())

    class _ExecWithTransaction:
        def __init__(self, cur: pyodbc.Cursor):
            self.cur = cur

        def exec_sql(self, sql, *args):
            return self.cur.execute(sql, *args)

        def commit(self):
            self.cur.commit()

        def rollback(self):
            self.cur.rollback()

        def close(self):
            self.cur.close()


if __name__ == '__main__':
    conn = MSSQL('brosmed2019.f3322.net,8087', 'sage', 'Brosmed2021', 'sagex3v12',)
    print(conn.conn.getinfo(pyodbc.SQL_ACCESSIBLE_TABLES))
    conn.close()
