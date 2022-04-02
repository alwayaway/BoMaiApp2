import pyodbc
from BoMaiCheck.toolbase import Dbase


class DataBase:
    def __init__(self, db_file):
        # noinspection SpellCheckingInspection
        init_db = [
            # 发货表单:
            "create table if not exists FHDH("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "SDHNUM_0 VARCHAR(64) not null ,"  # 发货单号
            "STOFCY_0 VARCHAR(64) not null ,"  # 地点
            "DLVDAT_0 timestamp not null ,"     # 发货日期
            "SDDLIN_0 VARCHAR(24) not null ,"  # 发货行
            "ITMREF_0 VARCHAR(64) not null ,"  # 产品编码
            "SOHNUM_0 VARCHAR(64) not null ,"  # 订单号
            "STU_0 VARCHAR(64) not null ,"  # 单位
            "QTYSTU_0 int not null ,"  # 发货数量
            "LOT_0 VARCHAR(48) not null ,"  # 批次
            "WRH_0 VARCHAR(48) not null ,"  # 仓库
            "LOC_0 VARCHAR(48) not null ,"  # 库位
            "BPCNAM_0 VARCHAR(124) not null ,"  # 客户
            "XITMNUM_0 VARCHAR(124) not null ,"  # 图纸编码
            "ITMDES1_0 VARCHAR(255) not null ,"  # 产品名称
            "ITMDES2_0 VARCHAR(124) not null ,"  # 产品规格
            "USRFLD2_0 VARCHAR(24) not null ,"  # 有效期
            "cnum int default 0"
            ")",
            # 装箱单
            "create table if not exists ZXDH("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "FHDH VARCHAR(64) not null ,"  # 发货单号
            "PALNUM_0 VARCHAR(64) not null ,"  # 箱码
            "BOXID_0 VARCHAR(64) not null ,"  # 待开发确认
            "NETWEI_0 VARCHAR(64) not null ,"  # 净重
            "GROWEI_0 VARCHAR(64) not null ,"  # 毛重
            "CARSIZ_0 VARCHAR(64) not null ,"  # 装箱尺寸
            "SOHNUM_0 VARCHAR(64) not null ,"  # 订单号
            "ITMREF_0 VARCHAR(64) not null ,"  # 产品编码
            "STU_0 VARCHAR(64) not null ,"  # 单位
            "QTY_0 int not null ,"  # 数量
            "LOT_0 VARCHAR(64) not null ,"  # 批次
            "WRH_0 VARCHAR(64) not null ,"  # 仓库
            "LOC_0 VARCHAR(64) not null ,"  # 库位
            "VCRLIN_0 VARCHAR(64) not null "  # 装箱行号
            ")",
        ]
        self.db = Dbase(db_file, init_db=init_db)

    def close(self):
        self.db.close()

    def add_codes(self, data):
        keys, values, length = '', [], 0
        for item in data:
            length = len(item)
            keys = item.keys()
            tmp = [str(_) for _ in item.values()]
            values.append(tmp)
        # noinspection SqlInsertValues
        _sql = f"insert into FHDH({','.join(keys)}) values ({','.join('?'*length)})"
        return self.db.executemany(_sql, *values)

    def get_code_tit(self, code):
        _sql = "select SDHNUM_0, STOFCY_0, DLVDAT_0 from FHDH where SDHNUM_0=? limit 0,1"
        return self.db.execute(_sql, code)

    def is_full_checked(self, code):
        _sql = "select SUM(cnum), MAX(QTYSTU_0) from FHDH where SDHNUM_0=?"
        num_, full_ = self.db.execute(_sql, code)[0]
        print(num_, ' :: ', full_)
        if num_ != full_ is not None:
            return int(num_) >= int(full_)
        else:
            return True

    def get_ZXDH_set(self, code):
        _sql = "SELECT PALNUM_0 FROM ZXDH WHERE FHDH=?"
        return self.db.execute(_sql, code)

    def del_ZXDH_item(self, code):
        _sql1 = "DELETE FROM ZXDH WHERE FHDH=?"
        _sql2 = "DELETE FROM FHDH WHERE SDHNUM_0=?"
        return self.db.execute(_sql1, code), self.db.execute(_sql2, code)

    def get_code_data(self, code):
        _sql = "select ITMDES1_0, SOHNUM_0, LOT_0, QTYSTU_0, cnum from FHDH where SDHNUM_0 =?"
        return self.db.execute(_sql, code)

    def get_XS_code(self, code):
        _sql = "select SOHNUM_0 from FHDH where SDHNUM_0 =? LIMIT 1"
        return self.db.execute(_sql, code)

    def up_code_num(self, code, lot, num):
        _sql = "update FHDH set cnum=? where SDHNUM_0=? and LOT_0=?"
        return self.db.execute(_sql, num, code, lot)

    def get_zxd_item(self, fhd, lot):
        _sql = "select SOHNUM_0, LOC_0, WRH_0, LOT_0, ITMREF_0, STU_0 " \
               "from FHDH where SDHNUM_0=? and LOT_0=? LIMIT 0,1"
        return self.db.execute(_sql, fhd, lot)

    def up_zx_num(self, num, box, lot):
        _sql = "update ZXDH set QTY_0= QTY_0+? where PALNUM_0=? and LOT_0=?"
        return self.db.execute(_sql, num, box, lot)

    def ct_zx_num(self, code, data: dict):
        data['FHDH'] = code
        values = [str(_) for _ in data.values()]
        # noinspection SqlInsertValues
        _sql = f"insert into ZXDH({','.join(data.keys())}) values ({','.join('?' * len(data))})"
        return self.db.execute(_sql, *values)

    def get_box_codes(self, code):
        _sql = "select PALNUM_0, SUM(QTY_0) from ZXDH where FHDH=? GROUP BY PALNUM_0"
        return self.db.execute(_sql, code)

    def get_box_items(self, code, box):
        _sql = "select distinct LOT_0, QTY_0 from ZXDH where FHDH=? and PALNUM_0=?"
        return self.db.execute(_sql, code, box)

    def get_print_data_wx(self, fhd, box):
        _sql = "select SUM(QTY_0), MAX(CARSIZ_0) from ZXDH where FHDH=? and PALNUM_0=?"
        qty, size = self.db.execute(_sql, fhd, box)[0]
        return {"FH_CODE": str(fhd), "ZX_CODE": str(box), "BOX_QTY": str(qty), "BOX_SIZE": str(size)}

    def get_print_data_mx(self, data: dict, fhd, box, lot):
        _sql = f"SELECT {','.join(data.values())} " \
               f"FROM FHDH, ZXDH WHERE FHDH.SDHNUM_0 = ZXDH.FHDH AND FHDH.LOT_0=ZXDH.LOT_0 " \
               f"AND SDHNUM_0=? AND PALNUM_0=? AND ZXDH.LOT_0 =?"
        res = self.db.execute(_sql, fhd, box, lot)
        print('执行结果:', f"长度:{len(res)}", res.get())
        return {k: str(v) for k, v in zip(data.keys(), res[0])}


class MSSQL:
    class Result:
        def __init__(self, result, is_success=True, msg='', err=None):
            self.value = result
            self._bool = is_success
            self._msg = msg
            self._err = err

        def isEmpty(self):
            return False if self.value else True

        def __bool__(self):
            return self._bool

        def __str__(self):
            return self._msg

        def __repr__(self):
            return self._msg

        def __len__(self):
            return len(self.value)

        def __iter__(self):
            return self._item()

        def __getitem__(self, item=None):
            return self.value[item]

        def error(self):
            return self._err

        def _item(self):
            for _v in self.value:
                yield _v

    def __init__(self, host, user, pwd, db='master', charset='utf8'):
        self._host = host
        self._user = user
        self._pwd = pwd
        self._db = db
        self._charset = charset
        if not self._db:
            raise (NameError, "没有设置数据库信息")
        conn_info = 'DRIVER={SQL Server};DATABASE=%s;SERVER=%s;UID=%s;PWD=%s' % (
            self._db, self._host, self._user, self._pwd)
        self.conn = pyodbc.connect(conn_info, charset=self._charset)

    def _get_connect(self):
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "连接数据库失败")
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
                result.append(dict([(desc[0], row[index]) for index, desc in enumerate(row.cursor_description)]))
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
    conn = MSSQL('brosmed2019.f3322.net,8087', 'sage', 'Brosmed2021', 'sagex3v12', )
    print(conn.conn.getinfo(pyodbc.SQL_ACCESSIBLE_TABLES))
    conn.close()
