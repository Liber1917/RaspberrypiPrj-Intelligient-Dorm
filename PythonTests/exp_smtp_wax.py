import smtplib#导入smtp模块
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
import os
#自己的qq邮箱，如果你是136的话可以改成xxxxxx@136.com
QQMAIL_USER = '2741184145@qq.com'
#smtp服务的授权码，根据上面的操作就可以获得
QQMAIL_PASS = 'okyhahqvupbtddhc'
#smtp的服务类型，我的是QQ，其他比如136邮箱可改成smtp.136.com,或者谷歌邮箱smtp.gmail.com
SMTP_SERVER = 'smtp.qq.com'
#这个端口一般没什么问题所有邮箱都是25，谷歌的587也可以
SMTP_PORT = 465
recipient1='2741184145@qq.com'
#邮件主题
sub1 = 'sub'
#邮件内容
text1='this is text'
#发送函数，参数recipient是接受者了，subject是邮件主题，text是邮件内容
#send_email(recipient1,sub1,text1)
def send_email(recipient,subject,text):
    smtpserver = smtplib.SMTP_SSL(SMTP_SERVER,465)
#    smtpserver.ehlo()
#    smtpserver.starttls()
#    smtpserver.ehlo
    smtpserver.login(QQMAIL_USER,QQMAIL_PASS)
    header = 'To:'+recipient+'\n'+'From:'+QQMAIL_USER
    header = header + '\n' +'Subject:' + subject +'\n'
    msg = header +'\n'+text+'\n\n'
    smtpserver.sendmail(QQMAIL_USER,recipient,msg)
    smtpserver.quit()
send_email(recipient1,sub1,text1)

