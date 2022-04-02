import time


class FmtTime:
    def __init__(self, date=None, mat=None):
        self._dict = {
            "@y": lambda: self._str4time("%y"),
            "@Y": lambda: self._str4time("%Y"),
            "@m": lambda: self._str4time("%m"),
            "@d": lambda: self._str4time("%d"),
            "@H": lambda: self._str4time_now("%H"),
            "@I": lambda: self._str4time_now("%I"),
            "@M": lambda: self._str4time_now("%M"),
            "@S": lambda: self._str4time_now("%S"),
            "@j": lambda: self._str4time("%j"),
            "@p": lambda: self._str4time_now("%p"),
            "@U0": lambda: self._str4time("%U"),
            "@U": lambda: self._year_week("%U"),
            "@w": lambda: self._str4time("%w"),
            "@w7": lambda: self._weekday7(),
            "@W0": lambda: self._str4time("%W"),
            "@W": lambda: self._year_week("%W"),
        }

        self.noUp = list(self._dict.keys())
        self.noUp.append("@唯一约束")
        self.date: time.struct_time = ...
        if date:
            self.setTime(date, mat)
        else:
            self.date = time.localtime()

    def _str4time(self, mat):
        return time.strftime(mat, self.date)

    def _str4time_now(self, mat):
        return time.strftime(mat, time.localtime())

    def _weekday7(self):
        day = time.strftime('%w', self.date)
        return day if day != '0' else '7'

    def _year_week(self, mat):
        yw = time.strftime(mat, self.date)
        xq = time.strftime("%w", time.strptime(f'{self.date.tm_year}-01-01', "%Y-%m-%d"))
        if mat == "%U" and xq != '0':
            return str(int(yw) + 1).zfill(2)
        elif mat == "%W" and xq != '1':
            return str(int(yw) + 1).zfill(2)
        else:
            return yw

    def setTime(self, date, mat=None):
        if mat is None:
            mat = "%Y-%m-%d %H:%M:%S"
        self.date = time.strptime(date, mat)

    def __getitem__(self, item):
        val = self._dict.get(item, lambda: f'无效参数: {item}')
        return val() if callable(val) else val

    def get(self, key):
        return self.__getitem__(key)

    def test(self):
        formats = {
            "@y": '两位数的年份表示（00-99)',
            "@Y": '四位数的年份表示（000-9999)',
            "@m": '月份（01-12）',
            "@d": '月内天数（0-31）',
            "@H": '24小时制小时数（00-23） 仅限当前时刻',
            "@I": '12小时制小时数（01-12） 仅限当前时刻',
            "@M": '分钟数（00-59） 仅限当前时刻',
            "@S": '秒（00-59） 仅限当前时刻',
            "@j": '年内天数（001-366）',
            "@p": 'AM（上午） 或 PM（下午） 仅限当前时刻',
            "@U0": '一年中的星期数（00-53）星期天为星期的开始 (1月1日后，第一个星期天前为00周， 第一个星期天为01周)',
            "@U": '一年中的星期数（01-53）星期天为星期的开始 (包含1月1日的周为01周，1月1号后的第一个星期天为02周)',
            "@w": '星期（0-6），星期天为星期的开始（星期天为0）',
            "@w7": '星期（1-7），星期一为星期的开始（星期天为7）',
            "@W0": '一年中的星期数（00-53）星期一为星期的开始(1月1日后，第一个星期一前为00周， 第一个星期一为01周)',
            "@W": '一年中的星期数（01-53）星期一为星期的开始(包含1月1日的周为01周，1月1号后的第一个星期一为02周)',
        }
        for k, v in formats.items():
            print(k, ' %-50s  \t\t: ' % v, self.get(k))

    def __contains__(self, key):
        return key in self._dict


if __name__ == '__main__':
    f = FmtTime('2024/1/7 9:0:0', mat="%Y/%m/%d %H:%M:%S")
    f.test()
