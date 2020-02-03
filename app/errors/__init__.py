# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 13:40:29 2020

@author: magut
"""

from flask import Blueprint

bp = Blueprint('errors', __name__)

from app.errors import handlers
