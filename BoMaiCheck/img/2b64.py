from base64 import b64decode, b64encode
import os
from Printer_Check_V2.toolbase import Img


def file_name(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] in ['.jpg', '.png']:
                L.append(file)
    return L


img = Img("../config/ImgBase")
for f in file_name("./"):
    with open(f, mode='rb')as png:
        data = b64encode(png.read())
        img.save(f.split('.')[0], data)