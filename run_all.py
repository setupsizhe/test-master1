# coding=utf-8
import unittest
import time
from XTestRunner import HTMLTestRunner
import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from case import test_api


curpath = os.path.dirname(os.path.realpath(__file__))
report_path = os.path.join(curpath, "report")
if not os.path.exists(report_path): os.mkdir(report_path)
case_path = os.path.join(curpath, "case")

def add_case(casepath=case_path, rule="test*.py"):
    '''加载所有的测试用例'''
    # 定义discover方法的参数
    discover = unittest.defaultTestLoader.discover(casepath,
                                                  pattern=rule,)

    return discover

def run_case(all_case, reportpath=report_path):
    '''执行所有的用例, 并把结果写入测试报告'''
    htmlreport = reportpath+r"\result.html"
    print("测试报告生成地址：%s"% htmlreport)

    with open(htmlreport, "wb") as fp:
        runner = HTMLTestRunner(stream=fp,verbosity=2,title="接口测试报告",description="用例执行情况")
        runner.run(all_case)
        f1=open(htmlreport,'r', encoding='utf-8')
        res=f1.read()
        f1.close()
        return res


def send_emails():
    mail_host = "smtp.163.com"  # 设置服务器
    mail_user = "15751592835@163.com"  # 用户名
    mail_pass = "qw1234"  # 口令

    sender = '15751592835@163.com'
    receivers = ['liusizhe@tsingyun.net','15751592835@163.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message=MIMEMultipart()
    subject='请查阅测试报告'
    message['Subject'] = Header(subject, 'utf-8')
    message['From'] = Header("{}".format(sender), 'utf-8')
    message['To'] = Header("{}".format(';'.join(receivers)), 'utf-8')
    cases=add_case()
    send_content=run_case(cases)
    html=MIMEText(_text=send_content, _subtype='html', _charset='utf-8')

    att = MIMEText(_text=send_content, _subtype='base64', _charset='utf-8')
    att["Content-Type"] = 'application/octet-stream'
    file_name = 'result.html'
    att["Content-Disposition"] = 'attachment; filename="{}"'.format(file_name)
    message.attach(html)
    message.attach(att)

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print ("邮件发送成功")
    except smtplib.SMTPException as e:
        print ("Error: 无法发送邮件:%s"%e)

if __name__ == "__main__":
    send_emails()

