import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
import time


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


def send_email(receivers,
               subject,
               text='空天报国，敢为人先',
               attach_file='',
               sleep_time=2,   # 发送时间间隔
               sender='your_email_addr',
               password='your_password'):
    text = "<html><h1 style='color:black'>" + text + "</h1></html>"  # 内容
    attach_mark = 0
    if attach_file == '':
        pass
    else:
        attach_mark = 1
        file_name, file_type, temp = get_file_info(attach_file)
        file_part = MIMEApplication(open(attach_file, 'rb').read())
        file_part.add_header('Content-Disposition', 'attachment', filename=file_name)
    smtpserver = 'smtp.163.com'

    smtp = smtplib.SMTP_SSL(smtpserver, 465)   # SSL协议端口号需要使用465
    smtp.login(sender, password)
    if len(receivers) == 1:
        pass
    else:
        print('sending begin...' + f'共需发送{len(receivers)}封')
    count = 0
    text_part = MIMEText(text, 'html', 'utf-8')
    all = MIMEMultipart()
    all.attach(text_part)
    if attach_mark == 1:
        all.attach(file_part)
    all['Subject'] = Header(subject, 'utf-8')
    all['From'] = sender
    for rec in receivers:
        if count == 0:
            count = 1
        else:
            time.sleep(sleep_time)  # 除了第一次发送外都间隔一定时间，避免访问服务器过快
        all['To'] = rec
        smtp.sendmail(sender, rec, all.as_string())
        print('sended: ' + rec)
    smtp.quit()
    if len(receivers) == 1:
        pass
    else:
        print(f'done，已发送{len(receivers)}封邮件')


