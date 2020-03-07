import zipfile
import shutil
from get_all_files_relative_filepath import get_relative_filepath
# 解压功能模块，提取所有文件


def jieya(in_path, out_path):
    zFile = zipfile.ZipFile(in_path, "r")
    for fileM in zFile.namelist():
        zFile.extract(fileM, out_path)
    zFile.close()


def get_all_zip(path):   # main
    print('解压开始')
    out_path = r"发票\PDF"
    abs_path = get_relative_filepath(path)[0]
    for item in abs_path:
        if item.split('.')[-1] == 'zip':
            jieya(item, out_path)
        else:   # 非压缩文件不用解压，直接移动到目标文件夹
            shutil.copy(item, out_path)

