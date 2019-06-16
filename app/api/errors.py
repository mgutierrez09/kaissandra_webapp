# -*- coding: utf-8 -*-
"""
Created on Mon May 13 15:43:24 2019

@author: mgutierrez
"""

from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response

def bad_request(message):
    return error_response(400, message)

def unauthorized_request(message):
    return error_response(401, message)