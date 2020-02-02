# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 15:20:56 2020

@author: magut
"""

from flask import Blueprint

bp = Blueprint('main', __name__)

from app.main import routes, forms
