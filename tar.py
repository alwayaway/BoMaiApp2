import os
import shutil
try:
    from PyInstaller import __main__
except:
    pass


def py_tar_bomai():
    py_file = 'BMAPP/main.py'
    __main__.run([
        '-w', '-D', '-y', '--clean',
        '-i=bomai.ico',
        '-n=BoMaiApp',
        py_file,
        '--hidden-import=PySide6.QtWebEngineCore'
        '--add-data=BMAPP\\base;base',
        '--add-data=BMAPP\\config;config',
        '--add-data=BMAPP\\html;html',
        '--add-data=BMAPP\\images;images',
        '-p=C:\\Windows\\System32\\downlevel\\',
        '-p=C:\\Windows\\System32\\',
        '-p=C:\\Windows\\SysWOW64\\',
        '-p=C:\\Windows\\SysWOW64\\downlevel\\',
        # '--log-level=WARN',
    ])


def clean_run():
    l_dir = ('log', 'images', 'base')
    for _ in l_dir:
        if os.path.exists(_):
            os.rmdir(_)


def nuitka_tar_BOMAI():
    main_path = 'BMAPP/main.py'
    main_ico = "--windows-icon-from-ico=bomai.ico"
    WINDOWS_COMPANY_NAME = '邦越科技'
    WINDOWS_PRODUCT_NAME = '博迈APP'
    WINDOWS_FILE_VERSION = "1.0.0.0"
    WINDOWS_PRODUCT_VERSION = "1.0.0.0"
    WINDOWS_FILE_DESCRIPTION = 'by alwayaway'
    WINDOWS_FORCE_STDERR_SPEC = '%PROGRAM%.err.txt'

    ex_cmd = [
        f"--windows-company-name={WINDOWS_COMPANY_NAME}",
        f"--windows-product-name={WINDOWS_PRODUCT_NAME}",
        f"--windows-file-version={WINDOWS_FILE_VERSION}",
        f"--windows-product-version={WINDOWS_PRODUCT_VERSION}",
        f"--windows-file-description={WINDOWS_FILE_DESCRIPTION}",
        f"--windows-force-stderr-spec={WINDOWS_FORCE_STDERR_SPEC}",
        '--run'
    ]

    cmd = [
        "nuitka3 --standalone",
        main_path, main_ico,
        "--output-dir=./dist",
        "--remove-output",
        "--plugin-enable=pyside2",
        "--windows-disable-console",
        '--include-data-dir=BMAPP/config=config',
        '--include-data-dir=BMAPP/html=html',
        '--include-data-dir=BMAPP/images=images',
    ]
    cmd.extend(ex_cmd)
    cmd = ' '.join(cmd)
    run = os.system(cmd)
    print(run)
    if run < 2:
        clean_run()


def nuitka_tar_ELD():
    main_path = 'EldLabelMG/main_eld_app.py'
    main_ico = "--windows-icon-from-ico=eld.ico"
    WINDOWS_COMPANY_NAME = '邦越科技'
    WINDOWS_PRODUCT_NAME = 'ELD LABEL PRINT MANAGER'
    WINDOWS_FILE_VERSION = "1.0.0.0"
    WINDOWS_PRODUCT_VERSION = "1.0.0.0"
    WINDOWS_FILE_DESCRIPTION = 'by alwayaway'
    WINDOWS_FORCE_STDERR_SPEC = '%PROGRAM%.err.txt'

    ex_cmd = [
        f"--windows-company-name={WINDOWS_COMPANY_NAME}",
        f"--windows-product-name={WINDOWS_PRODUCT_NAME}",
        f"--windows-file-version={WINDOWS_FILE_VERSION}",
        f"--windows-product-version={WINDOWS_PRODUCT_VERSION}",
        f"--windows-file-description={WINDOWS_FILE_DESCRIPTION}",
        f"--windows-force-stderr-spec={WINDOWS_FORCE_STDERR_SPEC}",
        '--run'
    ]

    cmd = [
        "nuitka --standalone",
        main_path, main_ico,
        # '--lto=yes',
        "--output-dir=./dist",
        "--remove-output",
        "--enable-plugin=pyside2",
        '--include-qt-plugins=sensible,qml,shiboken2',
        "--windows-disable-console",
        # "--msvc=14.2",
        '--include-data-dir=EldLabelMG/config=config',
        '--include-data-dir=EldLabelMG/images=images',
        '--include-data-file=Python.Runtime.dll=Python.Runtime.dll',
        '--include-data-file=python.exe.config=main_eld_app.exe.config',
    ]
    cmd.extend(ex_cmd)
    cmd = ' '.join(cmd)
    run = os.system(cmd)
    print(run)
    if run < 2:
        l_dir = ('log', 'config', 'base', 'images')
        for _ in l_dir:
            if os.path.exists(_):
                shutil.rmtree(_)


def py_tar_BOMAICheck():
    __main__.run([
        '-w', '-D', '-y', '--clean',
        '-i=pt.ico',
        r'BoMaiCheck\BMCheckApp.py',
        '--add-data=BoMaiCheck\\config;config',
        '--add-data=BoMaiCheck\\log;log',
        '--add-data=BoMaiCheck\\btw;btw',
        r'--add-binary=D:\python\BoMaiApp2\venv\Lib\site-packages\clr_loader\ffi\dlls\x86\ClrLoader.dll;'
        r'.\clr_loader\ffi\dlls\x86',
        '-p=C:\\Windows\\SysWOW64\\downlevel\\',
        '-p=C:\\Windows\\SysWOW64\\',
        # '--log-level=WARN',
    ])


def nuitka_tar_BOMAICheck():
    main_path = r'BoMaiCheck\BMCheckApp.py'
    main_ico = "--windows-icon-from-ico=pt.ico"
    WINDOWS_COMPANY_NAME = '邦越科技'
    WINDOWS_PRODUCT_NAME = '出库检查系统'
    WINDOWS_FILE_VERSION = "2.0.0.0"
    WINDOWS_PRODUCT_VERSION = "2.0.0.0"
    WINDOWS_FILE_DESCRIPTION = 'by alwayaway'
    WINDOWS_FORCE_STDERR_SPEC = '%PROGRAM%.err.txt'

    ex_cmd = [
        f"--windows-company-name={WINDOWS_COMPANY_NAME}",
        f"--windows-product-name={WINDOWS_PRODUCT_NAME}",
        f"--windows-file-version={WINDOWS_FILE_VERSION}",
        f"--windows-product-version={WINDOWS_PRODUCT_VERSION}",
        f"--windows-file-description={WINDOWS_FILE_DESCRIPTION}",
        f"--windows-force-stderr-spec={WINDOWS_FORCE_STDERR_SPEC}",
        '--run'
    ]

    cmd = [
        "python -m nuitka --standalone",
        main_path, main_ico,
        "--output-dir=./dist",
        "--remove-output",
        "--plugin-enable=pyside2",
        "--windows-disable-console",
        "--plugin-enable=pylint-warnings",
        "--include-data-dir=BoMaiCheck/config=config",
        "--include-data-dir=BoMaiCheck/log=log",
        "--include-data-dir=BoMaiCheck/btw=btw",
        '--include-data-file=Python.Runtime.dll=Python.Runtime.dll',
    ]
    cmd.extend(ex_cmd)
    cmd = ' '.join(cmd)
    os.system(cmd)


def nuitka_tar_COSMO():
    main_path = 'COSMO/ScanServiceApp.py'
    main_ico = "--windows-icon-from-ico=pt.ico"
    WINDOWS_COMPANY_NAME = '邦越科技'
    WINDOWS_PRODUCT_NAME = 'COSMO ScanServiceApp'
    WINDOWS_FILE_VERSION = "1.0.0.0"
    WINDOWS_PRODUCT_VERSION = "1.0.0.0"
    WINDOWS_FILE_DESCRIPTION = 'by alwayaway'
    WINDOWS_FORCE_STDERR_SPEC = '%PROGRAM%.err.txt'

    ex_cmd = [
        f"--windows-company-name={WINDOWS_COMPANY_NAME}",
        f"--windows-product-name={WINDOWS_PRODUCT_NAME}",
        f"--windows-file-version={WINDOWS_FILE_VERSION}",
        f"--windows-product-version={WINDOWS_PRODUCT_VERSION}",
        f"--windows-file-description={WINDOWS_FILE_DESCRIPTION}",
        f"--windows-force-stderr-spec={WINDOWS_FORCE_STDERR_SPEC}",
        '--run'
    ]

    cmd = [
        "nuitka --standalone",
        main_path, main_ico,
        "--output-dir=./dist",
        "--remove-output",
        "--plugin-enable=pyside2",
        "--windows-disable-console",
        '--include-data-dir=COSMO/config=config',
        '--include-data-dir=COSMO/log=log',
        '--include-data-dir=COSMO/qml=qml',
        '--include-data-dir=COSMO/uic=uic',
    ]
    cmd.extend(ex_cmd)
    cmd = ' '.join(cmd)
    run = os.system(cmd)
    print(run)


def py_tar_COSMO():
    __main__.run([
        '-w', '-D', '-y', '--clean',
        '-i=pt.ico',
        r'COSMO/ScanServiceApp.py',
        '--add-data=COSMO\\config;config',
        '--add-data=COSMO\\log;log',
        '--add-data=COSMO\\qml;qml',
        '--add-data=COSMO\\uic;uic',
        '-p=C:\\Windows\\System32\\downlevel\\',
        '-p=C:\\Windows\\System32\\',
        # '--log-level=WARN',
    ])


def py_tar_eld():
    kp_png_file = 'EPSWlogo.png'
    exe_name = 'eld'
    main_path = 'EldLabelMG/main_eld_app.py'
    __main__.run([
        '-w', '-D', '-y', '--clean',
        '-i=eld.ico', f'-n={exe_name}',
        f'{main_path}',
        '--win-private-assemblies',
        '--add-data=EldLabelMG/config;config',
        '--add-data=EldLabelMG/images;images',
        r'--add-binary=D:\python\BoMaiApp2\venv\Lib\site-packages\clr_loader\ffi\dlls\x86\ClrLoader.dll;'
        r'.\clr_loader\ffi\dlls\x86',
        f'--add-data=python.exe.config;./',
        '--add-binary=Python.Runtime.dll;./',
        '--add-binary=python.exe.config;./',
        '-p=C:\\Windows\\SysWOW64\\downlevel\\',
        '-p=C:\\Windows\\SysWOW64\\',
        f'--splash={kp_png_file}',
        '--key=AlwayAway',
        # '--log-level=WARN',
    ])
    os.replace(rf'D:\python\BoMaiApp2\dist\{exe_name}\python.exe.config',
               rf'D:\python\BoMaiApp2\dist\{exe_name}\{exe_name}.exe.config')


if __name__ == '__main__':
    py_tar_bomai()
    # nuitka_tar_BOMAI()
    # nuitka_tar_ELD()
    # py_tar_eld()
    # nuitka_tar_BOMAICheck()
    # py_tar_BOMAICheck()
    # nuitka_tar_COSMO()
    # py_tar_COSMO()

