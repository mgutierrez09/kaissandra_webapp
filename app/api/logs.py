# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 17:12:10 2019

@author: mgutierrez
"""
from flask import request, jsonify
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request
import datetime as dt

@bp.route('/logs/traders', methods=['POST'])
@token_auth.login_required
def get_trader_log():
    """  """
    json_data = request.get_json() or {}
    if 'Message' not in json_data:
        return bad_request("Message not included in json.")
    if 'Name' not in json_data:
        return bad_request("Name of trader not included in json.")
    out = dt.datetime.strftime(dt.datetime.utcnow(),'%d.%m.%y %H:%M:%S')+' trader '+json_data['Name']+': '+json_data['Message']
    print(out)
    return jsonify({
        'Out': out,
    })
    
@bp.route('/logs/networks', methods=['POST'])
@token_auth.login_required
def get_network_log():
    """  """
    json_data = request.get_json() or {}
    if 'Message' not in json_data:
        return bad_request("Message not included in json.")
    out = dt.datetime.strftime(dt.datetime.utcnow(),'%d.%m.%y %H:%M:%S')+' network: '+json_data['Message']
    print(out)
    return jsonify({
        'Out': out,
    })