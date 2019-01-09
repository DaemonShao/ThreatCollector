# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from ConfigParser import ConfigParser


class ThreatEmail(object):

    config = ConfigParser()
    config.read("scrapy.cfg")

    sender = "scrapy@threat.com"
    receivers = config.get("email_service", "receivers").split(";")

    def send_mail(self, from_user, to_user, subject, email_message):
        message = MIMEText(email_message, "plain", "utf-8")
        message['From'] = from_user
        message['To'] = to_user
        message['Subject'] = Header(subject, 'utf-8')

        try:
            smtpObj = smtplib.SMTP('localhost', port=1025)
            smtpObj.sendmail(self.sender, self.receivers, message.as_string())
            print "邮件发送成功"
        except smtplib.SMTPException:
            print "Error: 无法发送邮件"

