# -*- coding:utf-8  -*-
import os
import sys
import clr


class Bartender:
    # noinspection PyUnresolvedReferences
    def __init__(self, sdk_path=None):
        self.loaded = False

        sys.path.append(sdk_path if sdk_path else 'SDK/Assemblies')  # 加载 BT SDK路径

        try:
            clr.AddReference("System")
            clr.AddReference("Seagull.BarTender.Print")
        except Exception as _clr_load_err:
            raise FileNotFoundError('Can not load SDK: Seagull.BarTender.Print!')

        import Seagull.BarTender.Print as BtSDK
        from System import EventHandler

        self.BtSDK = BtSDK

        self.btEngine = BtSDK.Engine(True)
        self.btFormats = []
        self.EventHandlerMsg = {}

        self.JobCancelled = EventHandler(self.btEngine_JobCancelledSlot)  # 打印任务关闭时触发
        self.btEngine.JobCancelled += self.JobCancelled

        self.JobErrorOccurred = EventHandler(self.btEngine_JobErrorOccurredSlot)  # 打印出错时触发
        self.btEngine.JobErrorOccurred += self.JobErrorOccurred

        self.JobMonitorErrorOccurred = EventHandler(self.btEngine_JobMonitorErrorOccurredSlot)  # 监控出错时触发
        self.btEngine.JobMonitorErrorOccurred += self.JobMonitorErrorOccurred

        self.JobPaused = EventHandler(self.btEngine_JobPausedSlot)  # 任务暂停时触发
        self.btEngine.JobPaused += self.JobPaused

        self.JobQueued = EventHandler(self.btEngine_JobQueuedSlot)  # 打印任务入列时触发
        self.btEngine.JobQueued += self.JobQueued

        self.JobRestarted = EventHandler(self.btEngine_JobRestartedSlot)  # 任务重启时触发
        self.btEngine.JobRestarted += self.JobRestarted

        self.JobResumed = EventHandler(self.btEngine_JobResumedSlot)  # 任务回溯时触发
        self.btEngine.JobResumed += self.JobResumed

        self.JobSent = EventHandler(self.btEngine_JobSentSlot)  # 任务发送时触发
        self.btEngine.JobSent += self.JobSent
        self.loaded = True

    def close(self):
        if self.loaded and self.btEngine.IsAlive:
            for btFormat in self.btFormats:
                btFormat.close_btw()
            self.btEngine.Stop()  # 停止引擎
            self.btEngine.Dispose()  # 释放资源

    def __del__(self):
        self.close()

    def get_printer_list(self):
        """获取打印机列表"""
        printers = self.BtSDK.Printers()
        printer_list = []
        for printer in printers:
            printer_list.append(printer.PrinterName)
        return printer_list, printers.Default.PrinterName

    def open_btw(self, btwFile, name=None):
        """打开btw文件"""
        btFormat = self.BtFile(self.BtSDK, self.btEngine, btwFile, self, name)
        self.btFormats.append(btFormat)
        return btFormat

    class BtFile:
        def __init__(self, BtSDK, btEngine, btwFile, parent, name=None):
            self.name = name if name is not None else btwFile.split('\\')[-1]
            self.BtSDK = BtSDK
            self.btEngine = btEngine
            self.parent: Bartender = parent
            self.btFormat = self.btEngine.Documents.Open(btwFile)

        def close_btw(self):
            """关闭文档并保存"""
            self.btFormat.Close(self.BtSDK.SaveOptions.SaveChanges)
            self.parent.btFormats.remove(self)

        def btw_image(self, file):
            """btw2jpeg"""
            self.btFormat.ExportImageToFile(
                file, self.BtSDK.ImageType.JPEG, self.BtSDK.ColorDepth.ColorDepth256,
                self.BtSDK.Resolution(96), self.BtSDK.OverwriteOptions.Overwrite
            )

        def get_data_dict(self, key=None):
            """获取btw文件参数"""
            data_dict = {}
            if self.btFormat:
                if key:
                    return self.btFormat.SubStrings[key].Value
                for substring in self.btFormat.SubStrings:
                    data_dict[substring.Name] = substring.Value
            return data_dict

        def set_data_dict(self, data_dict):
            """设置btw文件参数"""
            if len(data_dict) and self.btFormat:
                for key, value in data_dict.items():
                    for substring in self.btFormat.SubStrings:
                        if substring.Name == key:
                            self.btFormat.SubStrings.SetSubString(key, value)

        def get_substring_config(self, substring):
            data_dict = {}
            if self.btFormat:
                # Substring类
                data_dict['SerializeBy'] = self.btFormat.SubStrings[substring].SerializeBy  # 返回str
                data_dict['SerializeEvery'] = self.btFormat.SubStrings[substring].SerializeEvery  # 返回str
                # PrintSetup类
                data_dict['NumberOfSerializedLabels'] = self.btFormat.PrintSetup.NumberOfSerializedLabels
                data_dict['IdenticalCopiesOfLabel'] = self.btFormat.PrintSetup.IdenticalCopiesOfLabel
            return data_dict

        def set_substring_config(self, substring, data_dict):
            if self.btFormat:
                # Substring类
                self.btFormat.SubStrings[substring].SerializeBy = data_dict['SerializeBy']
                self.btFormat.SubStrings[substring].SerializeEvery = data_dict['SerializeEvery']
                # PrintSetup类
                self.btFormat.PrintSetup.NumberOfSerializedLabels = data_dict['NumberOfSerializedLabels']
                self.btFormat.PrintSetup.IdenticalCopiesOfLabel = data_dict['IdenticalCopiesOfLabel']
                return True
            return False

        def setPrinter(self, printer):
            self.btFormat.PrintSetup.PrinterName = printer

        def Print(self, s=1, c=1, timeout=None):  # 返回nResult，0=成功，1=失败
            """

            :param s: 打印数量
            :param c: 复制数量
            :param timeout: 超时
            :return:
            """
            # 判断bartender是否启动
            if not self.btEngine.IsAlive:
                self.btEngine.Start()
            try:  # 开始打印
                self.btFormat.PrintSetup.NumberOfSerializedLabels = s
                self.btFormat.PrintSetup.IdenticalCopiesOfLabel = c
                return self.btFormat.Print(self.name, timeout)  # 0=成功，1=超时，2=失败
            except Exception as ex:
                print(ex)
                return 2

    def _set_Event(self, _k, _v):
        self.EventHandlerMsg[_k] = _v

    def get_Event(self, _k):
        """
        get event
        :param _k:
        :return: event: e.g.: event.ID event.Name event.Status event.Message event.ErrorType
        """
        return self.EventHandlerMsg.get(_k)

    def btEngine_JobSentSlot(self, sender, event):
        """任务发送时触发"""
        self._set_Event('JobSent', event)
        return sender, event

    def btEngine_JobResumedSlot(self, sender, event):
        """任务回溯时触发"""
        self._set_Event('JobResumed', event)
        return sender, event

    def btEngine_JobRestartedSlot(self, sender, event):
        """任务重启时触发"""
        self._set_Event('JobRestarted', event)
        return sender, event

    def btEngine_JobPausedSlot(self, sender, event):
        """任务暂停时触发"""
        self._set_Event('JobPaused', event)
        return sender, event

    def btEngine_JobMonitorErrorOccurredSlot(self, sender, event):
        """监控出错时触发"""
        self.btEngine.JobCancelled -= self.JobCancelled
        self.btEngine.JobErrorOccurred -= self.JobErrorOccurred
        self.btEngine.JobMonitorErrorOccurred -= self.JobMonitorErrorOccurred
        self.btEngine.JobPaused -= self.JobPaused
        self.btEngine.JobQueued -= self.JobQueued
        self.btEngine.JobRestarted -= self.JobRestarted
        self.btEngine.JobResumed -= self.JobResumed
        self.btEngine.JobSent -= self.JobSent
        self._set_Event('JobMonitorErrorOccurred', event)
        return sender, event

    def btEngine_JobErrorOccurredSlot(self, sender, event):
        """打印出错时触发"""
        self._set_Event('JobErrorOccurred', event)
        return sender, event

    def btEngine_JobCancelledSlot(self, sender, event):
        """打印任务关闭时触发"""
        self._set_Event('JobCancelled', event)
        return sender, event

    def btEngine_JobQueuedSlot(self, sender, event):
        """打印任务入列时触发"""
        self._set_Event('JobQueued', event)
        return sender, event


def sdk_test():
    _engine = Bartender()
    file = os.path.abspath('./base/test.btw')
    print(f'Use btw file: {file}')
    btf = _engine.open_btw(file)
    print(btf.get_data_dict())
    tup_q = ('quit', 'exit', 'QUIT', 'EXIT')
    print(f'输入 {", ".join(tup_q)} 之一可结束程序'.encode('gbk').decode('gbk'))
    while True:
        data = input(">>:")
        if data in tup_q:
            break
        btf.btFormat.PrintSetup.NumberOfSerializedLabels = 2  # 打印数量
        btf.btFormat.PrintSetup.IdenticalCopiesOfLabel = 1  # 复制数量
        btf.set_data_dict({'测试数据': f'BTW SDK TEST: {data}'})
        print(btf.get_data_dict())
        print(btf.btFormat.Print())

    _engine.btEngine.Stop()
    _engine.close()


if __name__ == '__main__':
    sdk_test()
