# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 16:22:13 2019

@author: mgutierrez
"""

from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.tables_test import User
from app.api.errors import error_response, unauthorized_request

#def is_admin(id):
#    def decorator(function):
#        """ Auth function to check if user is admin """
#        print(function)
#        trader =Trader.query.filter_by(id=id).first()
#        user = trader.
#        if not g.current_user.isadmin:
#            return unauthorized_request("User is not admin. Access denied")

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return False
    g.current_user = user
    return user.check_password(password)

@basic_auth.error_handler
def basic_auth_error():
    return error_response(401)

@token_auth.verify_token
def verify_token(token):
    g.current_user = User.check_token(token) if token else None
    return g.current_user is not None

@token_auth.error_handler
def token_auth_error():
    return error_response(401)