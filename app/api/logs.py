# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 17:12:10 2019

@author: mgutierrez
"""
from flask import request, jsonify
from app import db
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request
import datetime as dt
from app.tables_test import LogMessage

@bp.route('/logs/traders', methods=['POST'])
#@token_auth.login_required
def get_trader_log():
    """  """
    json_data = request.get_json() or {}
    if 'Message' not in json_data:
        return bad_request("Message not included in json.")
    if 'Name' not in json_data:
        return bad_request("Name of trader not included in json.")
    now = dt.datetime.utcnow()
    out = dt.datetime.strftime(now,'%d.%m.%y %H:%M:%S')+' trader '+json_data['Name']+': '+json_data['Message']
    print(out)
    logmessage = LogMessage.query.filter_by(origin="TRADER").first()
    if not logmessage:
        logmessage = LogMessage(origin="TRADER", message=out, datetime=now)
        db.session.add(logmessage)
    else:
        logmessage.message = out
        logmessage.datetime = now
    print(logmessage)
    
    db.session.commit()
    return jsonify({
        'Out': out,
    })
    
@bp.route('/logs/networks', methods=['POST'])
#@token_auth.login_required
def get_network_log():
    """  """
    json_data = request.get_json() or {}
    if 'Message' not in json_data:
        return bad_request("Message not included in json.")
    now = dt.datetime.utcnow()
    out = dt.datetime.strftime(now,'%d.%m.%y %H:%M:%S')+' network: '+json_data['Message']
    print(out)
    # save it in db
    logmessage = LogMessage.query.filter_by(origin="NETWORK").first()
    if not logmessage:
        logmessage = LogMessage(origin="NETWORK", message=out, datetime=now)
        db.session.add(logmessage)
    else:
        logmessage.message = out
        logmessage.datetime = now
    
    db.session.commit()
    print(logmessage)
    return jsonify({
        'Out': out,
    })