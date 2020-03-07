#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# @Version : 1.2
# @Time    : 2019/11/19
# @Author  : GT
# 主程序

from HWOcrClientToken import HWOcrClientToken
import json
import os
import shutil
from extract_file import get_all_zip
from pdf_to_png import main_pdf_to_png
from send import send
from get_all_files_relative_filepath import get_relative_filepath


def get_file_info(path):
    frame = []
    temp1 = path.split('\\')
    for item in temp1:
        temp2 = item.split('/')
        for i in temp2:
            frame.append(i)
    file_name = frame[-1]
    file_type = frame[-1].split('.')[-1]
    formal_path = '/'.join(frame[:-1])
    return file_name, file_type, formal_path


if __name__ == '__main__':
    # 解压
    get_all_zip(r'发票\发票原始')
    # 转图片
    main_pdf_to_png(target_path=r'发票\PDF')
    # 华为云OCR
    PNG_path = r'发票\图片版'
    PNG_list = get_relative_filepath(PNG_path)[0]
    number_total = len(PNG_list)
    number = 0
    ex = 0
    print('共有'+str(len(PNG_list))+'张图片')
    username = "you_account_in_HWCloud_site"
    password = "you_password_in_HWCloud_site"
    domain_name = "you_name_in_HWCloud_site"  # if the user isn't IAM user, domain_name is the same with username
    region = "cn-north-4"  # cn-north-1,cn-east-2 etc.
    endpoint = "ocr.cn-north-4.myhuaweicloud.com"
    for item in PNG_list:
        try:
            url1 = '/v1.0/ocr/vat-invoice'  # 增值税发票识别代号
            ocrClient = HWOcrClientToken(domain_name, username, password, region, endpoint)
            response = ocrClient.request_ocr_service_base64(url1, item)
            name = json.loads(response.text)['result']['buyer_name']   # 公司名称
            print(name)
            count = get_file_info(item)[0].split('.')[-2]
            print(count)
            formal = r'发票\PDF' + "\\" + count + '.pdf'
            latter = r'发票\PDF' + '\\' + name + '.pdf'
            try:
                if os.path.exists(latter):
                    print(item, '已存在！', latter)    # 统计重复的发票
                    ex += 1
                shutil.move(formal, latter)    # 重命名至规范的文档
                number += 1
                print('已处理' + str(number) + '个文件')
            except:
                pass
        except ValueError as e:
            print("处理失败:"+item)
            print(e)
    print('开始发送')
    # 邮件发送
    send(excel_path=r'发票\企业信息表.xlsx', pdf_path=r'发票\PDF')
    print('程序执行结束，请查看结果文档，failed.txt与sended.txt')




