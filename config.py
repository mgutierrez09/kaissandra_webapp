# -*- coding: utf-8 -*-
"""
Created on Sat May 11 18:11:47 2019

@author: mgutierrez
"""

import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
#    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'\
#        .format(user=os.environ.get('POSTGRES_USER'),pw=os.environ.get('POSTGRES_PW'),\
#                url=os.environ.get('POSTGRES_URL'),db=os.environ.get('POSTGRES_DB'))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'postgresql+psycopg2://{user}:{pw}@{url}/{db}'\
        .format(user=os.environ.get('POSTGRES_USER'),pw=os.environ.get('POSTGRES_PW'),\
                url=os.environ.get('POSTGRES_URL'),db=os.environ.get('POSTGRES_DB'))
#    print(os.environ.get('MAIL_SERVER'))
#    print(os.environ.get('MAIL_PORT'))
#    print(os.environ.get('MAIL_USE_TLS'))
#    print(os.environ.get('MAIL_USERNAME'))
#    print(os.environ.get('MAIL_PASSWORD'))
#    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
#        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['kaissandra.ai@gmail.com']

    ASSETS = {"1":'AUDCAD',
             "2":'EURAUD',
             "3":'EURCAD',
             "4":'EURCHF',
             "7":'EURGBP',
             "8":'EURNZD',
             "10":'EURUSD',
             "11":'GBPAUD',
             "12":'GBPCAD',
             "13":'GBPCHF',
             "14":'GBPUSD',
             "16":'USDCAD',
             "17":'USDCHF',
             "19":'USDJPY',
             "27":"CADJPY",
             "28":"EURJPY",
             "29":"AUDJPY",
             "30":"CHFJPY",
             "31":"GBPJPY",
             "32":"NZDUSD",
             "33":"AUDUSD"}
    indx_assets=[i for i in ASSETS.keys()]
    LOT = 100000.0