# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 17:12:10 2019

@author: mgutierrez
"""
import time
from flask import request, jsonify, Response
from app import db, Config
from app.api import bp, tradeLogMsg, netLogMsg
from app.api.auth import token_auth
from app.api.errors import bad_request
import datetime as dt
from app.tables_test import LogMessage, Trader

@bp.route('/logs/traders', methods=['POST'])
@token_auth.login_required
def get_trader_log():
    """  """
    json_data = request.get_json() or {}
    if 'Message' not in json_data:
        return bad_request("Message not included in json.")
    if 'Name' not in json_data:
        return bad_request("Name of trader not included in json.")
    if 'Asset' not in json_data:
        asset = "UNKNWN"
    else:
        asset = json_data['Asset']
    now = dt.datetime.utcnow()
    out = dt.datetime.strftime(now,'%d.%m.%y %H:%M:%S')+' trader '+json_data['Name']+' '+asset+' '+json_data['Message']
    print(out)
    global tradeLogMsg
    tradeLogMsg[asset] = out
    logmessage = LogMessage.query.filter_by(origin="TRADER", asset=asset).first()
    if not logmessage:
        logmessage = LogMessage(origin="TRADER", message=out, datetime=now, asset=asset)
        db.session.add(logmessage)
    else:
        logmessage.message = out
        logmessage.datetime = now
    #print(logmessage)
    
    db.session.commit()
    return jsonify({
        'Out': out,
    })

@bp.route('/logs/monitor', methods=['POST'])
@token_auth.login_required
def get_monitor_log():
    """  """
    json_data = request.get_json() or {}
    if 'Message' not in json_data:
        return bad_request("Message not included in json.")
    if 'Name' not in json_data:
        return bad_request("Name of trader not included in json.")
    if 'Asset' not in json_data:
        asset = "UNKNWN"
    else:
        asset = json_data['Asset']
    now = dt.datetime.utcnow()
    out = dt.datetime.strftime(now,'%d.%m.%y %H:%M:%S')+'Monitoring '+asset+': '+json_data['Message']
    print(out)
    global netLogMsg
    netLogMsg[asset] = out
    logmessage = LogMessage.query.filter_by(origin="TRADER", asset=asset).first()
    if not logmessage:
        logmessage = LogMessage(origin="TRADER", message=out, datetime=now, asset=asset)
        db.session.add(logmessage)
    else:
        logmessage.message = out
        logmessage.datetime = now
    #print(logmessage)
    
    db.session.commit()
    return jsonify({
        'Out': out,
    })

@bp.route('/logs/global', methods=['POST'])
@token_auth.login_required
def get_global_log():
    """  """
    print(netLogMsg)
    print(tradeLogMsg)
    return jsonify({
        'netLogMsg': netLogMsg,
        'tradeLogMsg': tradeLogMsg,
    })
    
@bp.route('/logs/networks', methods=['POST'])
@token_auth.login_required
def get_network_log():
    """  """
    json_data = request.get_json() or {}
    if 'Message' not in json_data:
        return bad_request("Message not included in json.")
    if 'Asset' not in json_data:
        asset = "UNKNWN"
    else:
        asset = json_data['Asset']
    now = dt.datetime.utcnow()
    out = dt.datetime.strftime(now,'%d.%m.%y %H:%M:%S')+' network '+asset+" "+json_data['Message']
    print(out)
    global netLogMsg
    netLogMsg[asset] = out
    # save it in db
    logmessage = LogMessage.query.filter_by(origin="NETWORK", asset=asset).first()
    if not logmessage:
        logmessage = LogMessage(origin="NETWORK", message=json_data['Message'], asset=asset, datetime=now)
        db.session.add(logmessage)
    else:
        logmessage.message = out
        logmessage.datetime = now
    
    db.session.commit()
    #print(logmessage)
    return jsonify({
        'Out': out,
    })

##### Streamline SSE #####

@bp.route('/account/status')
def streamAccountStatus():
    def eventStream():
        # WARNING! Only compatible with farnamstreet trader for now
        
        while True:
            
            yield 'data: {}\n\n'.format(get_account_status())
    return Response(eventStream(), mimetype="text/event-stream")

def get_account_status():
    """  """
    time.sleep(5)
    trader = Trader.query.filter_by(tradername='farnamstreet').first()
    status = '{0:.2f}/{1:.1f}/{2:.2f}/{3:.2f}'.format(trader.balance, 
                    trader.leverage, trader.equity, trader.profits)
    return status

@bp.route('/logs/streamNetwork')
def streamNetwork():
    def eventStream():
        ass_idx = -1
        assets = Config.ASSETS
        indx_assets = Config.indx_assets
        while True:
            ass_idx = (ass_idx+1) % len(assets)
            asset = assets[indx_assets[ass_idx]]
            yield 'data: {}/{}\n\n'.format(get_log_network(asset), asset)
    return Response(eventStream(), mimetype="text/event-stream")

@bp.route('/logs/streamTrader')
def streamTrader():
    def eventStream():
        ass_idx = -1
        assets = Config.ASSETS
        indx_assets = Config.indx_assets
        while True:
            # update asset index
            ass_idx = (ass_idx+1) % len(assets)
            asset = assets[indx_assets[ass_idx]]
            # wait for source data to be available, then push it
            yield "data: {}/{}\n\n".format(get_log_trader(asset), asset)
    return Response(eventStream(), mimetype="text/event-stream")

def get_log_trader(asset):
    '''Get trader logs'''
    
    time.sleep(0.1)
    # user = User.query.filter_by(username="kaissandra").first()
    global tradeLogMsg
    logmessage = LogMessage.query.filter_by(origin="TRADER", asset=asset).first()
    if not logmessage:
        return "WAITING FOR CONNECTION"
    else:
        return tradeLogMsg[asset]

def get_log_network(asset):
    '''Get network logs'''
    time.sleep(0.1)
    # user = User.query.filter_by(username="kaissandra").first()
    global netLogMsg
    logmessage = LogMessage.query.filter_by(origin="NETWORK", asset=asset).first()
    if not logmessage:
        return "WAITING FOR CONNECTION"
    else:
        return netLogMsg[asset]
        # s = time.ctime(time.time())