# -*- coding: utf-8 -*-
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Mail:

    @staticmethod
    def send(host, port, sender_email, password, receiver_email, subject, message):
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        try:
            server = smtplib.SMTP(host, port)
            server.set_debuglevel(1)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(sender_email, password)
            message = msg.as_string()
            server.sendmail(sender_email, receiver_email, message)
            server.quit()
            return True
        except Exception as e:
            print(e)
            return False
