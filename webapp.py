# -*- coding: utf-8 -*-
"""
Created on Sat May 11 17:56:10 2019

@author: mgutierrez
"""

from app import create_app, db
from config import Config
from app.tables_test import User, Position, Trader, Strategy, Network, \
                       Session, Asset, LogMessage

app = create_app()

# inject Config parameters in all templates
@app.context_processor
def inject_config():
    return dict(ASSETS=Config.ASSETS, indx_assets=Config.indx_assets)#[str(i) for i in range(len(Config.ASSETS))]

@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'User':User, 'Position':Position, 'Trader':Trader,
     'Strartegy':Strategy, 'Network':Network,
     'Session':Session, 'Asset':Asset, 'LogMessage':LogMessage}