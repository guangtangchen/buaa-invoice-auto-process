import xlrd
from get_all_files_relative_filepath import get_relative_filepath
from send_email import send_email


def get_file_info(path):
    """
    获取文件路径相关信息
    :param path: str, 路径
    :return: tuple, 文件名，类型，前导路径
    """
    frame = []
    temp1 = path.split('\\')
    for item in temp1:
        temp2 = item.split('/')   # 对/和\都处理一下，防止输入不和自己心意
        for i in temp2:
            frame.append(i)
    file_name = frame[-1]
    file_type = frame[-1].split('.')[-1]
    formal_path = '/'.join(frame[:-1])
    return file_name, file_type, formal_path


def send(excel_path=r'发票\企业信息表.xlsx',
         pdf_path=r'发票\PDF'):
    workbook = xlrd.open_workbook(excel_path)
    worksheet = workbook.sheet_by_name(workbook.sheet_names()[0])
    print(worksheet.name)
    rows = worksheet.nrows
    info = {}
    for row in range(rows):
        name = worksheet.cell_value(row, 15)
        addr = worksheet.cell_value(row, 19)
        info[name] = addr
    print(info)
    names = info.keys()
    pdf_abs_path = get_relative_filepath(pdf_path)[0]
    file_info = {}
    for file in pdf_abs_path:
        file_only_name = get_file_info(file)[0].split('.')[0]
        file_info[file_only_name] = file
    print(file_info)
    text = '这是贵公司的收款发票，请查收。------北航招就处'
    subject = '10月24号北航双选会发票'
    for name in names:
        try:
            email_addr = [info[name]]
            attach_file = file_info[name]
            send_email(email_addr, subject, text, attach_file)
            with open(r'发票\sended.txt', 'a') as f:
                f.write(name + '\n')   # 把成功发送的企业记录下来
        except:
            print('failed:' + name)
            with open(r'发票\failed.txt', 'a') as f:
                f.write(name+'\n')   # 把发送失败的企业记录下来，后续人工处理


if __name__ == '__main__':
    send()


