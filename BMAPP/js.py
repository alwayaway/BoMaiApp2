
class JsMethods:
    def __init__(self):
        _JSMethods = [self._message, self.goIndex]
        jsSet = [_js.__doc__ for _js in _JSMethods]
        self.jsName = 'AppScript'
        self.VueJs = "var %s = new Vue({ methods: { %s }});" % (self.jsName, ','.join(jsSet))

    def _js(self, js):
        return f'{self.jsName}.{js}'

    def goIndex(self):
        """
        goIndex: function (url) {
            this.$message({
              message: '首页',
              type: 'information',
            });
            }
        """
        return self._js("goIndex('')")

    def _message(self, msg, tp):
        """
        message(msg, tp) {
            this.$message({
              message: msg,
              type: tp
            });
          }
        """
        return self._js(f"message('{msg}', '{tp}')")

    def success(self, msg):
        return self._message(msg, 'success')

    def error(self, msg):
        return self._message(msg, 'error')

    def warning(self, msg):
        return self._message(msg, 'warning')

    def information(self, msg):
        return self._message(msg, 'information')