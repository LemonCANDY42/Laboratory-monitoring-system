import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
from email.mime.message import MIMEMessage
from copy import deepcopy
from tkinter import E

class EmailManager:
    def __init__(self,email='545410124@qq.com'):
        self.email = email
        self.is_sending = False
        self.count = 0
        self.set_recv()
    
    def connect(self):
        # 1. 连接邮箱服务器
        self.con = smtplib.SMTP_SSL('smtp.qq.com', 465)
        # 2. 登录邮箱
        self.con.login(self.email, 'brhbkqrtlllcbeec')
    
    def set_recv(self,recv_email = '245550353@qq.com'):
        # recv_email can be a list 
        self.recv_email = recv_email

    def send_msg(self,message='Python邮件发送测试...',header = "test",file_list=[]):
        self.is_sending = True
        try:
            # 创建邮件对象
            msg = MIMEMultipart()
            # 设置邮件主题
            subject = Header(header, 'utf-8').encode()
            msg['Subject'] = subject
            # 设置邮件发送者
            msg['From'] = 'QInvestment<{0}>'.format(self.email)
            
            # 设置邮件接受者
            _to = ''
            if self.recv_email is list:
                for i in self.recv_email:
                    _to = _to+'<{0}>'.format(i)
            else:
                _to = _to+'<{0}>'.format(self.recv_email)
            msg['To'] = _to
            if file_list:
                for _file,file_name in file_list:
                    # 添加文件附件
                    file = MIMEText(open(_file, 'rb').read(), 'base64', 'utf-8')
                    file["Content-Disposition"] = f'attachment; filename="{file_name}"'
                    msg.attach(file)

            _message = MIMEText(message, 'plain', 'utf-8')
            msg.attach(_message)
            print(msg)
            # 3.发送邮件
            self.con.sendmail(self.email, self.recv_email, msg.as_string())
        except Exception as e:
            raise e
        else:
            self.count+=1
        finally:
            self.is_sending = False

    def quit(self):
        self.con.quit()


if __name__ == "__main__":
    e = EmailManager()
    e.set_recv(recv_email = ["245550353@qq.com","l.w.r.f.42@outlook.com"])
    e.connect()
    e.send_msg()
    print(e.con)
    e.quit()

        