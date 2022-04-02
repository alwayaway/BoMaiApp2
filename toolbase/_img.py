import sqlite3


class Img:
    def __init__(self, _file, *args, check_same_thread=False, **kwargs):
        self.conf = sqlite3.connect(_file, *args, check_same_thread=check_same_thread, **kwargs)
        self.init_db(_file)

    def init_db(self, _file):
        self.conf.execute("""
                CREATE TABLE IF NOT EXISTS [image](
                    [id] integer PRIMARY KEY AUTOINCREMENT NOT NULL,
                    [name]	varchar(255) NOT NULL unique,
                    [value]	BLOB
                );
                """)

    def save(self, _name, _b64):
        _sql = f"replace into image([name], [value])  values (?,?)"
        cur = self.conf.cursor()
        try:
            cur.execute(_sql, (_name, _b64))
            self.conf.commit()
            return True
        except Exception as e:
            print(e)
            return e
        finally:
            cur.close()

    def get(self, _name):
        _sql = "select [value] from image where [name] = ?"
        cur = self.conf.cursor()
        try:
            cur.execute(_sql, (_name, ))
            return cur.fetchall()[0][0]
        except Exception as e:
            return e
        finally:
            cur.close()

    def close(self):
        self.conf.close()