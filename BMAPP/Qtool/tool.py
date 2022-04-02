import json
import os
from http import cookiejar
from urllib import request
import contextlib
from threading import Thread
import pylightxl as xl
import xlsxwriter


class HttpTool:
    def __init__(self):
        self.header = {"Content-Type": "application/json",}
        self.cookie = cookiejar.CookieJar()
        self.get_opener()
        self.request = request

    def get_opener(self):
        handler = request.HTTPCookieProcessor(self.cookie)
        opener = request.build_opener(handler)
        request.install_opener(opener)
        return opener

    def setCookie(self, domain, name, value, path):
        Cookie = cookiejar.Cookie
        secure = False
        domain_specified = False

        initial_dot = domain.startswith(".")
        assert domain_specified == initial_dot

        discard = False
        expires = None

        c = Cookie(0, name, value,
                   None, False,
                   domain, domain_specified, initial_dot,
                   path, False,
                   secure,
                   expires,
                   discard,
                   None,
                   None,
                   {})
        self.cookie.set_cookie(c)
        # print(self.cookie)

    def post(self, url, data):
        try:
            data = json.dumps(data).encode('utf-8')
            data = request.Request(url, headers=self.header, data=data)
            return request.urlopen(data)
        except Exception as post_err:
            return self._Err(post_err)

    def get(self, url):
        try:
            data = request.Request(url, headers=self.header)
            return request.urlopen(data)
        except Exception as get_err:
            return self._Err(get_err)

    class _Err:
        def __init__(self, err):
            self._err = err
            self.__doc__ = "无法连接到指定服务器，请检查网络是否正常！"

        def __str__(self):
            return str(self._err)

        def read(self):
            return f'{{"code": -1001, "message": "{self.__doc__}"}}'.encode()


class DownLoader:
    def __init__(self, url, file, http=None):
        self.http = HttpTool() if http is None else http
        self.url = url
        self.file = file
        self._err = None
        self._thread = Thread(target=self._start, daemon=True)

    def start(self):
        self._thread.start()

    def wait(self, timeout):
        self._thread.join(timeout)

    def error(self):
        return self._err

    def _start(self):
        try:
            with contextlib.closing(self.http.request.urlopen(self.url)) as fp:
                headers = fp.info()
                tfp = open(self.file, 'wb')
                with tfp:
                    result = self.file, headers
                    if 'octet-stream' not in headers['Content-Type']:
                        raise result
                    bs = 1024 * 8
                    read = 0
                    block_num = 0
                    if "content-length" in headers:
                        max_size = int(headers["Content-Length"])
                    else:
                        max_size = -1

                    while True:
                        block = fp.read(bs)
                        if not block:
                            break
                        read += len(block)
                        tfp.write(block)
                        block_num += 1
                        self.loading(read, max_size)

            if max_size >= 0 and read < max_size:
                raise("retrieval incomplete: got only %i out of %i bytes"
                      % (read, max_size), result)

            self.finished()
        except Exception as _down_err:
            self._err = _down_err

    def loading(self, recvSize, totalSize):
        pass

    def finished(self):
        pass


class XlsxWriterLight:
    def __init__(self, file_, data:dict):
        db = xl.Database()
        for k1, v1 in data.items():
            db.add_ws(ws=k1)
            wt = db.ws(ws=k1)
            for col, tit in enumerate(v1.keys(), start=1):
                wt.update_index(row=1, col=col, val=tit)
            for col, val in enumerate(v1.values(), start=1):
                wt.update_index(row=2, col=col, val=val)
        if os.path.exists(file_):
            os.remove(file_)
        xl.writexl(db=db, fn=file_)


class TxtWriter:
    def __init__(self, path, data:dict):
        for k1, v1 in data.items():
            with open(f'{path}/{k1}.txt', mode='w') as _wf:
                _wf.write('::'.join(v1.keys()))
                _wf.write('::'.join(v1.values()))


class XlsxWriter:
    def __init__(self, file_, data:dict, rows: int):
        if os.path.exists(file_):
            os.remove(file_)
        workbook = xlsxwriter.Workbook(file_)
        for k1, v1 in data.items():
            sheet = workbook.add_worksheet(k1)
            for col, tit in enumerate(v1.keys()):
                sheet.write(0, col, tit)
            row = 1
            for _ in range(rows):
                for col, val in enumerate(v1.values()):
                    sheet.write(row, col, val)
                row += 1
            rows = 1
        workbook.close()


if __name__ == '__main__':
    pass
