from PyInstaller import __main__


def py_tar_WinService():
    __main__.run([
        '-c', '-F', '-y', '--clean',
        '-i=../pt.ico',
        'winservice.py',
        '--hidden-import=win32timezone',
        '-p=C:\\Windows\\System32\\downlevel\\',
        '-p=C:\\Windows\\System32\\',
        # '--log-level=WARN',
    ])


py_tar_WinService()
