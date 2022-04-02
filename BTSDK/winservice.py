# -*- coding:utf-8 -*-
"""
Build:
    pyinstaller -F --hidden-import=win32timezone [service].py

Install:
    [service].exe install

Service Manage:
    sc start [Service]
    sc stop [Service]
  or
    [service].exe start
    [service].exe stop

Uninstall:
    sc delete [Service]
  or
    [service].exe remove
"""

import os
import sys
import servicemanager
import win32serviceutil
import win32service
import win32event
import winerror

from BTSDK.BtService import start


class WindowsService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'ByBtSdkServiceX86'
    _svc_display_name_ = 'BtSDK打印服务X86'
    _svc_description_ = '为应用程序提供BartenderX86打印队列服务服务【需要安装Bartender X86 SDK】,' \
                        '终止或停用该服务将导致使用该服务的应用无法打印标签'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.httpd: start = ...
        self.run = True

    def SvcDoRun(self):
        # 服务工作代码
        self.httpd = start()
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        self.httpd.serve_forever()

    def SvcStop(self):
        if self.httpd is not ...:
            self.httpd.server_close()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)
        self.run = False


if __name__ == '__main__':
    if len(sys.argv) == 1:
        # noinspection PyUnresolvedReferences
        try:
            event_src_dll = os.path.abspath(servicemanager.__file__)
            servicemanager.PrepareToHostSingle(WindowsService)
            servicemanager.Initialize('WindowsService', event_src_dll)
            servicemanager.StartServiceCtrlDispatcher()
        except win32service.error as details:
            if details.args[0] == winerror.ERROR_FAILED_SERVICE_CONTROLLER_CONNECT:
                win32serviceutil.usage()
    else:
        win32serviceutil.HandleCommandLine(WindowsService)
