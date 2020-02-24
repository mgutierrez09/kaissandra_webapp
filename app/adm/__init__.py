# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24
@author: mgutierrez

init file of flask admin blueprint
"""

from flask import Blueprint

bp = Blueprint('adm', __name__)

from app.adm import views