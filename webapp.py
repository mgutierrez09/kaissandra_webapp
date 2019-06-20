# -*- coding: utf-8 -*-
"""
Created on Sat May 11 17:56:10 2019

@author: mgutierrez
"""

from app import create_app, db
from app.tables_test import User, Position, Trader, Strategy, Network, \
                       Session, Asset

app = create_app()


@app.shell_context_processor
def make_shell_context():
    {'db':db, 'User':User, 'Position':Position, 'Trader':Trader,
     'Strartegy':Strategy, 'Network':Network,
     'Session':Session, 'Asset':Asset}