import os
# 输入一个文件夹路径，返回文件夹下所有文件的绝对路径以及除去输入部分的相对路径
# relative_path_2为包含的path最后一级目录的相对目录


def get_relative_filepath(path):
    abs_path = []
    relative_path = []
    relative_path_2 = []
    head = path.split('/')[-1].split('\\')[-1]
    if os.path.isfile(path):
        abs_path.append(path)
        relative_path.append(head)
        relative_path_2.append(head)
        return abs_path, relative_path, relative_path_2
    lenth = len(path) + 1
    for root, dirs, files in os.walk(path):
        for name in files:
            temp = root + '\\' + name
            abs_path.append(temp)
            relative_path.append(temp[lenth:])
            relative_path_2.append(head + '\\' + temp[lenth:])
    return abs_path, relative_path, relative_path_2




