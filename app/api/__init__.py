# -*- coding: utf-8 -*-
"""
Created on Mon May 13 15:42:10 2019

@author: mgutierrez
"""

from flask import Blueprint
from app import Config

bp = Blueprint('api', __name__)

tradeLogMsg = {}
netLogMsg ={}
for val in Config.ASSETS:
    ass = Config.ASSETS[val]
    tradeLogMsg[ass] = ass+" tradeLog waiting for info"
    netLogMsg[ass] = ass+" netWork waiting for info"

from app.api import users, traders, errors, tokens, logs