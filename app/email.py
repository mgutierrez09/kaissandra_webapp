# -*- coding: utf-8 -*-
"""
Created on Sat May 11 19:02:23 2019

@author: mgutierrez
"""

from threading import Thread
from flask import current_app
from flask_mail import Message
from app import mail, Config
import pandas as pd

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email,
           args=(current_app._get_current_object(), msg)).start()

def send_pos_email(dict_pos, event):
    """ Send emal about position has been opened """
    content = pd.DataFrame(dict_pos, index=[0])
    body = content.to_string()
    html = content.to_html()
    subject = dict_pos['dtisoll'] + ' ' + dict_pos['asset'] + ' ' + event
    sender = Config.ADMINS[0]
    # TODO: get users attached to trader as recipients
    recipients = Config.ADMINS
    send_email(subject, sender, recipients, body, html)
    
    