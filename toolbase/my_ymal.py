import yaml


class Yml:
    def __init__(self, file):
        self._f = file
        self._y = {}
        self.read()

    def read(self):
        with open(self._f, encoding='utf-8')as _r:
            tmp = yaml.load(_r, yaml.CLoader)
        if tmp:
            self._y = tmp

    def dump(self):
        with open(self._f, encoding='utf-8', mode='w')as _w:
            yaml.dump(self._y, _w, allow_unicode=True)

    def __getitem__(self, item):
        return self._y.get(item)

    def __setitem__(self, key, value):
        self._y[key] = value

    def get(self, item, init=None):
        tmp = self.__getitem__(item)
        if tmp:
            return tmp
        elif init:
            self.__setitem__(item, init)
            self.dump()
        return init

    def set(self, key, value):
        self._y[key] = value
        self.dump()

    def items(self):
        return self._y.items()

    def keys(self):
        return self._y.keys()

    def values(self):
        return self._y.values()

    def __repr__(self):
        return self._y

    def __str__(self):
        return str(self._y)
