import traceback
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import json

__HOST__ = 'localhost'
__PORT__ = 8000
host = (__HOST__, __PORT__)
SERVICE = 'BtService'
VERSION = '1.0.0.0'


class HttpHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.api = {}
        self.printers = ['test']
        for _f in self.__dir__():
            if _f.startswith('api_'):
                self.api[_f[4:]] = eval(f"self.{_f}")

        super(HttpHandler, self).__init__(*args, **kwargs)

    def version_string(self):
        return f"{SERVICE} V{VERSION}"

    def resp(self, _code, message='', data=None, _resp=200):
        rtv = json.dumps({'code': _code, 'message': message, 'data': data}, ensure_ascii=False)
        self.send_response(_resp)
        self.send_header('Content-type', 'text/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(rtv.encode())

    def _response(self, path, args):
        path = path.strip('/')
        if path in self.api:
            return self.api.get(path)(args)
        else:
            return self.resp(404, 'not found')

    @staticmethod
    def splitquery(url):
        path, _, query = url.rpartition('?')
        if _:
            return path, query
        return url, None

    def do_GET(self):
        path, args = self.splitquery(self.path)
        if args:
            args = parse_qs(args).items()
            args = dict([(k, v[0]) for k, v in args])
        else:
            args = {}
        self._response(path, args)

    def do_POST(self):
        args = self.rfile.read(int(self.headers['content-length'])).decode("utf-8")
        args = json.loads(args) if args else {}
        self._response(self.path, args)

    def getPrinter(self):
        pass
        # L_printer = win32print.EnumPrinters(6, None, 2)
        # self.printers = [i['pPrinterName'] for i in L_printer]

    def api_GetPrinter(self, _args):
        self.getPrinter()
        return self.resp(200, '', self.printers)


def start():
    print(f'init {SERVICE} ...')
    # noinspection PyBroadException
    try:
        _httpd = HTTPServer(host, HttpHandler)
    except Exception as _err:
        print(f'init {SERVICE} ERR')
        traceback.print_exc(1)
        raise _err
    else:
        print(f'init {SERVICE} OK')
        print(f'Starting {SERVICE} {VERSION} at {__HOST__}:{__PORT__}')
    return _httpd


if __name__ == '__main__':
    httpd = start()
    httpd.serve_forever()
