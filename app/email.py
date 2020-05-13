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
        try:
            mail.send(msg)
        except:
            print("WARNING! Email not sent")


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email,
           args=(current_app._get_current_object(), msg)).start()

def send_pos_email(dict_pos, dt, event):
    """ Send emal about position has been opened """
    content = pd.DataFrame(dict_pos, index=[0])[pd.DataFrame(columns=dict_pos.keys()).columns.tolist()]
    body = content.to_string(index=False)
    html = content.to_html(index=False)
    subject = dt + ' ' + dict_pos['asset'] + ' ' + event
    sender = Config.ADMINS[0]
    # TODO: get users investing in trader as recipients
    if event=='open':
        recipients = Config.ADMINS+Config.MAILS_POSITION_EXTENSION
    elif event=='close':
        recipients = Config.ADMINS+Config.MAILS_POSITION_EXTENSION
    elif event=='extend':
        recipients = Config.MAILS_POSITION_EXTENSION
    elif event=='noextend':
        recipients = Config.MAILS_POSITION_NOEXTENSION
    if Config.MAIL_SERVER:
        send_email(subject, sender, recipients, body, html)
#    else:
    print("Email sent from "+sender)
    print("Receipients:")
    print(recipients) 
    print("Subject: "+subject)
    print("Body:")
    print(body)

def send_config_email(config, asset):
    """ Send emal about position has been opened """
    content = pd.DataFrame({'margins':[c['mar'] for c in config['list_spread_ranges']],
                            'spreads':[c['sp'] for c in config['list_spread_ranges']],
                            'thresholds':[c['th'] for c in config['list_spread_ranges']],
                            'max_opened_positions':config['max_opened_positions'],
                            'list_thr_sl':config['list_thr_sl'],
                            'list_max_lots_per_pos':config['list_max_lots_per_pos']}, 
                            index=[i for i in range(len(config['list_spread_ranges']))])
    body = content.to_string(index=False)
    html = content.to_html(index=False)
    subject = asset + ' ' + config['config_name']
    sender = Config.ADMINS[0]
    recipients = Config.MAILS_CONFIG
    if Config.MAIL_SERVER:
        send_email(subject, sender, recipients, body, html)
    print("Email sent from "+sender)
    print("Receipients:")
    print(recipients) 
    print("Subject: "+subject)
    print("Body:")
    print(body)
    