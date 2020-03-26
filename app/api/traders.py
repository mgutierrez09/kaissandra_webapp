# -*- coding: utf-8 -*-
"""
Created on Tue May 14 11:00:24 2019

@author: mgutierrez
"""

#import json
import time
import pandas as pd
import datetime as dt
from flask import jsonify, request, url_for, g
from app import db, ma, Config
from app.api import bp
from app.email import send_pos_email
from app.tables_test import (Trader, Strategy, Asset, Network, Session, Position, PositionSplit,
                        User, Extension, SessionStratetgy, TraderSchema, StrategySchema, NetworkSchema, SessionSchema, 
                        PositionSchema, PositionSplitSchema, ExtensionSchema)
from app.api.errors import bad_request, error_response, unauthorized_request
from app.api.auth import token_auth

str_sch = StrategySchema()
network_sch = NetworkSchema()
### WARNING! Temporary. Params should be read from DB
config_params = {}
command = ''
opened_positions = {}

# @bp.route('/traders/<int:id>', methods=['GET'])
# @token_auth.login_required
# #@is_admin
# def get_trader_entry(id):
#     """  """
#     if not g.current_user.isadmin:
#         return unauthorized_request("User is not admin. Access denied")
#     #jsonify(Trader.query.get_or_404(id).to_dict())
#     return get_trader(id)

#@bp.route('/traders', methods=['GET'])
##@token_auth.login_required
#def traders():
#    return get_traders()

@bp.route('/traders/sessions/<int:id>', methods=['GET'])
@token_auth.login_required
def get_session(id):
    """  """
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
    session = Session.query.filter_by(id=id).first()
    session_sch = SessionSchema()
    result = session_sch.dump(session)
    return jsonify({
        'Session': result,
    })
    
@bp.route('/traders/sessions/name', methods=['GET'])
@token_auth.login_required
def get_session_from_name():
    """  """
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
    json_data = request.get_json() or {}
    if 'sessionname' not in json_data:
        return bad_request('sessionname must be included.')
    session = Session.query.filter_by(sessionname=json_data['sessionname']).first()
    if session == None:
        return bad_request('session does not exist.')
    result = SessionSchema().dump(session)
    return jsonify({
        'Session': result,
    })
    
#@bp.route('/traders/sessions/all', methods=['GET'])
##@token_auth.login_required
#def get_sessions():
#    """  """
#    if not g.current_user.isadmin:
#        return unauthorized_request("User is not admin. Access denied")
#    #json_data = request.get_json() or {}
##    if 'sessionname' not in json_data:
##        return bad_request('sessionname must be included.')
#    sessions = Session.query.all()
#    result = SessionSchema(many=True).dump(sessions)
#    return jsonify({
#        'Sessions': result,
#    })
    
#@bp.route('/traders/strategies/all', methods=['GET'])
##@token_auth.login_required
#def get_strategies():
#    """  """
#    if not g.current_user.isadmin:
#        return unauthorized_request("User is not admin. Access denied")
#    str_sch = StrategySchema(many=True)
#    strategies = Strategy.query.all()
#    # Serialize the queryset
#    result = str_sch.dump(strategies)
#    return jsonify({'strategies': result})

@bp.route('/traders/strategies/<int:id>', methods=['GET'])
@token_auth.login_required
def get_strategy(id):
    """  """
    if not g.current_user.isadmin:
        return unauthorized_request("Unauthorized. Access denied")
    strategy = Strategy.query.filter_by(id=id).first()
    # Serialize the queryset
    result = StrategySchema().dump(strategy)
    return jsonify({'strategy': result})

@bp.route('/traders/<int:id>/strategies', methods=['GET'])
@token_auth.login_required
def get_strategies_trader(id):
    """  """
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
    str_sch = StrategySchema(many=True)
    trader = Trader.query.filter_by(id=id).first()
    strategies = trader.strategies
    # Serialize the queryset
    result = str_sch.dump(strategies)
    return jsonify({'strategies': result})

#@bp.route('/traders/networks/all', methods=['GET'])
##@token_auth.login_required
#def get_networks():
#    """  """
#    networks = Network.query.all()
#    return jsonify({'networks':NetworkSchema(many=True).dump(networks)})

@bp.route('/traders/strategies/<int:id>/networks', methods=['GET'])
@token_auth.login_required
def get_networks_from_strategy(id):
    """  """
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
    strategy = Strategy.query.filter_by(id=id).first()
    return jsonify({'networks':NetworkSchema(many=True).dump(strategy.networks)})

@bp.route('/traders/strategies/networks/<int:id>', methods=['GET'])
@token_auth.login_required
def get_network(id):
    """  """
    network = Network.query.filter_by(id=id).first()
    return jsonify({'network':NetworkSchema().dump(network)})

@bp.route('/traders/strategies/networks', methods=['GET'])
@token_auth.login_required
def get_network_from_name():
    """  """
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
    json_data = request.get_json() or {}
    if 'networkname' not in json_data:
        return bad_request('networkname must be included.')
    network = Network.query.filter_by(networkname=json_data['networkname']).first()
    return jsonify({'network':NetworkSchema().dump(network)})

@bp.route('/traders/<int:id>/assets', methods=['GET'])
@token_auth.login_required
def get_assets(id):
    """  """
    pass

@bp.route('/traders/positionsplits/<int:id>', methods=['GET'])
@token_auth.login_required
def get_positionsplit(id):
    """  """
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
    positionsplit = PositionSplit.query.filter_by(id=id).first()
    if positionsplit == None:
        bad_request('PositionSplit does not exist.')
    splits_result = PositionSplitSchema().dump(positionsplit)
    return jsonify({
        'Split':splits_result
    })
    
@bp.route('/traders/positions/<int:id>', methods=['GET'])
@token_auth.login_required
def get_position(id):
    """  """
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
    position = Position.query.filter_by(id=id).first()
    result = PositionSchema().dump(position)
    #print(result)
    return jsonify({
        'Position':result
    })

#@bp.route('/traders/positions/all', methods=['GET'])
##@token_auth.login_required
#def get_positions():
#    """  """
#    positions = Position.query.all()
#    
#    result = PositionSchema(many=True).dump(positions)
#    return jsonify({
#        'Positions':result
#    })
    
@bp.route('/traders/sessions/<int:id>/positions', methods=['GET'])
@token_auth.login_required
def get_positions_from_session(id):
    """  """
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
    session = Session.query.filter_by(id=id).first()
    if session == None:
        return bad_request('Session does not exist')
    result = PositionSchema(many=True).dump(session.positions)
    return jsonify({
        'Positions':result
    })
    

    
#@bp.route('/traders/positions/filter', methods=['GET'])
##@token_auth.login_required
#def get_positions_filter():
#    """  """
#    data = request.get_json() or {}
#    if 'asset' in data:
#        positions = Position.query.filter_by(asset=data['asset']).all()
#    
#    result = PositionSchema(many=True).dump(positions)
#    return jsonify({
#        'Positions':result
#    })
    
@bp.route('/traders', methods=['POST','PUT'])
@token_auth.login_required
def set_trader():
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
    data = request.get_json() or {}
#    if request.method == 'GET':
#        pass
    code, trader = Trader.validate_fields(data)
    if code==-1:
        return bad_request('must include tradername field')
    if code == 1:
        # init budget to zero if no budget added when creating
        
        trader_sch = TraderSchema()
    if code==2:
        # already exists. PUT        
        code_mod = trader.modify_attributes(data)
        if code_mod<0:
            return bad_request('One or more fields are wrong.')
        trader_sch = TraderSchema()
        trader = Trader.query.filter_by(tradername=data['tradername']).first()
        # Serialize the queryset
        result = trader_sch.dump(trader)
        response = jsonify({'trader': result})
        # TODO: choose the right status for succesful PUT
        response.status_code = 200
        #response.headers['Location'] = url_for('api.get_trader_entry', id=trader.id)
        return response
    # POST
    trader = Trader()
    if 'budget' not in data:
        data['budget'] = 0
    data['performance'] = 0
    if trader.add2db(data)==-1:
        return bad_request('please use valid trader fields')
    
    result = trader_sch.dump(trader)
    mess = "Trader added with code "+str(code)
    #response = jsonify(trader.to_dict())
    response = jsonify({
        'message': mess,
        'trader': result,
    })
    response.status_code = 200
    #response.headers['Location'] = url_for('api.get_trader_entry', id=trader.id)
    return response

@bp.route('/traders/<int:id>/strategies', methods=['POST', 'PUT'])
@token_auth.login_required
def set_strategy(id):
    """  """
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
    trader = Trader.query.get(id)
    if not trader:
        return bad_request('Trader does not exist.')
    
    json_data = request.get_json() or {}
    if 'strategyname' not in json_data:
        return bad_request('Strategy must be included.')
    try:
        data = str_sch.load(json_data)
    except ma.ValidationError as err:
        return jsonify(err.messages), 422
    if 'sessionname' in json_data:
        sessionname = json_data['sessionname']
        del json_data['sessionname']
    else:
        sessionname = None
#    print("strategy.strategyname")
#    print(strategy.strategyname)
    list_strategies = Strategy.query.all()
#    print("list_strategies")
#    print(list_strategies)
    new_strategy = data[0]
#    print("data")
#    print(data)
    # print("new_strategy")
    # print(new_strategy)
    if new_strategy.strategyname not in [stra.strategyname for stra in list_strategies]:
        # create new strategy
        code = trader.add_strategy(new_strategy)
        strategy = new_strategy
    else:
        code = 0
        strategy = Strategy.query.filter_by(strategyname=new_strategy.strategyname).first()
        code_attrs = strategy.set_attributes(json_data)
        if code_attrs<0:
            return bad_request('Error when setting attributes. Check them and resend request')
    # add session to strategy
    if sessionname != None:
        Session.query.filter_by(sessionname=sessionname).first().add_strategy(strategy)
    # print("Strategy slthr:")
    # print(strategy.slthr)
    db.session.commit()
    
    if code == 1:
        mess = 'New stratedy added'
        status_code = 200
    elif code == 0:
        mess = 'Strategy already existed. Parameters updated'
        status_code = 200
    else:
        return bad_request('Wrong code when strategy added to trader. Check fields and try again')
    
    result = str_sch.dump(strategy)
    response = jsonify({
        'message': mess,
        'Strategy': result,
    })
    response.status_code = status_code
    #response.headers['Location'] = url_for('api.get_strategy', id=trader.id)
    return response
    
@bp.route('/traders/networks', methods=['POST', 'PUT'])
@token_auth.login_required
def set_network():
    """  """
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
    json_data = request.get_json() or {}
    if 'strategy' not in json_data:
        return bad_request('strategy must be included.')
    if 'networkname' not in json_data:
        return bad_request('networkname must be included.')
    # load strategy and delete entry from json
    strategy = Strategy.query.filter_by(strategyname=json_data['strategy']).first()
    if strategy == None:
        return bad_request('Strategy must does not exist.')
    del json_data['strategy']
    try:
        data = network_sch.load(json_data)
    except ma.ValidationError as err:
        return jsonify(err.messages), 422
    list_networks = Network.query.all()
    if data[0].networkname not in [net.networkname for net in list_networks]:
        # create new strategy
        code = strategy.add_network(data[0])
#        if code_ora==-1:
#            return bad_request('Oracle has already an oracle.')
        network = data[0]
    else:
        code = 0
        network = Network.query.filter_by(networkname=data[0].networkname).first()
        if strategy.strategyname not in [stra.strategyname for stra in network.strategies]:
            strategy.add_network(network)
            code = 2
        code_attrs = network.set_attributes(json_data)
        if code_attrs<0:
            return bad_request('Error when setting attributes. Check them and resend request')
    db.session.commit()
    
    if code == 1:
        mess = 'New network added'
        status_code = 200
    elif code == 0:
        mess = 'Network already exists. Parameters updated'
        status_code = 200
    elif code == 2:
        mess = 'Network already exists. Added to new strategy'
        status_code = 200
    else:
        return bad_request('Wrong code when network added to strategy. Check fields and try again')
    
    result = network_sch.dump(network)
    response = jsonify({
        'Message': mess,
        'Network': result,
    })
    response.status_code = status_code
    return response

@bp.route('/traders/<int:id>/assets', methods=['POST'])
@token_auth.login_required
def set_assets(id):
    """  """
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
    trader = Trader.query.get(id)
    if not trader:
        return bad_request('Trader does not exist.')
    data = request.get_json() or {}
    if data == {}:
        return bad_request("assets are not included")
#    try:
#        
#    except ma.ValidationError as err:
#        return jsonify(err.messages), 422
#    print(data)
    assetnames = data['assets'].split(',')
    list_assets = []
    list_assetnames = []
    for assetname in assetnames:
        code = Asset.is_asset(assetname)
        if code < 0:
            return bad_request('Asset '+assetname+' does not exist.')
        asset = Asset.query.filter_by(assetname=assetname).first()
        # add to DB
        if asset == None:
            asset = Asset(assetname=assetname)
            asset.add2db(data)
        # add to trader
        if asset not in trader.assets:
            list_assets.append(asset)
            list_assetnames.append(assetname)
#    print(list_assetnames)
    code = trader.add_assets(list_assets)
    # loop over assets in trader to unlink those which are not in trader anymore
    for asset in trader.assets:
        if asset.assetname not in assetnames:
            trader.assets.remove(asset)
    db.session.commit()
    mess = "Assets added with code "+str(code)
    return jsonify({
        'message': mess,
        'Assets': [ass.assetname for ass in trader.assets],
    })

@bp.route('/traders/<int:id>/sessions', methods=['POST'])
@token_auth.login_required
def open_session(id):
    """  """
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
    trader = Trader.query.get(id)
    if trader == None:
        return bad_request("Trader does not exist")
    json_data = request.get_json() or {}
    if 'sessionname' not in json_data:
        return bad_request('sessionname must be included.')
    session_sch = SessionSchema()
    
    session = Session.query.filter_by(sessionname=json_data['sessionname']).first()
    if session == None:
        try:
            data_sch = session_sch.load(json_data)
            session = data_sch[0]
            code = trader.add_session(session)
            mess = "Session created with code "+str(code)
        except ma.ValidationError as err:
            return jsonify(err.messages), 422
    else:
        return bad_request("Session already exits. Choose another sessionname")
    db.session.commit()
    result = session_sch.dump(session)
    # update params structure
    # params[session.id] = {}
    # print(params)
    return jsonify({
        'message': mess,
        'Session': result,
    })

@bp.route('/traders/sessions/open', methods=['GET'])
@token_auth.login_required
def get_open_sessions():
    """ Get id of all open sessions """
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
    sessions = Session.query.filter_by(running=True)
    sessions_id = []
    for session in sessions:
        sessions_id.append(session.id)
    
    result = sessions_id
    return jsonify({
        'message': "Open Sessions id",
        'Sessions': result,
        'Number':len(sessions_id)
    })

@bp.route('/traders/sessions/<int:id>/close', methods=['PUT'])
@token_auth.login_required
def close_session(id):
    """  """
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
    session = Session.query.filter_by(id=id).first()
    if session == None:
        return bad_request("Session does not exist")
    if not session.running:
        return bad_request("Session not running")
    session.running = False
    session.dto = dt.datetime.utcnow()
    db.session.commit()
    result = SessionSchema().dump(session)
    return jsonify({
        'message': "Session closed",
        'Session': result,
    })

@bp.route('/traders/sessions/close', methods=['PUT'])
@token_auth.login_required
def close_sessions():
    """ Close all sessions but those included in json """
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
    json_data = request.get_json() or {}
    if 'all_but_ids' not in json_data:
        ids = []
    else:
        try:
            ids = [int(entry) for entry in json_data['all_but_ids'].split(',')]
        except:
            return bad_request("Error when parsing ids. Make sure they are ints and separated by ,")
    sessions = Session.query.filter_by(running=True)
    sessions_closed = []
    for session in sessions:
        if session.id not in ids:
            session.running = False
            session.dto = dt.datetime.utcnow()
            sessions_closed.append(session.id)
    if len(sessions_closed)==0:
        return jsonify({
        'message': "No Session open",
        })
    db.session.commit()
    result = sessions_closed
    return jsonify({
        'message': "Sessions closed",
        'Sessions': result,
    })
    
@bp.route('/traders/sessions/get_params', methods=['GET'])
@token_auth.login_required
def get_params():
    """  """
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
    open_sessions = Session.query.filter_by(running=True).all()
    if len(open_sessions)==0:
        return jsonify({
            'message': "No session running. Get parameters from strategy directly."
        })
    # WARNING: All open sessions are considered to have same strategies
    strategy = open_sessions[-1].sessionstrategies[-1]
    newparams = {'lots':strategy.poslots,'stoploss':strategy.slthr}
    return jsonify({
         'params': newparams,
    })

@bp.route('/traders/sessions/get_session_config', methods=['GET'])
@token_auth.login_required
def get_session_config():
    """  """
    global config_params
    global command
    return jsonify({
            'config': config_params,
            'command':command
    })

@bp.route('/traders/sessions/set_session_config', methods=['PUT'])
@token_auth.login_required
def set_session_config():
    """  """
    json_data = request.get_json() or {}
    global config_params
    global command
    msg = ''
    if 'config' in json_data:
        config_params = json_data['config']
        #print(config_params)
        msg += 'Config set. '

    if 'command' in json_data:
        command = json_data['command']
        msg += 'Command '+command+' set.'
        #print(command)
    return jsonify({
            'message': msg
    })

@bp.route('/traders/sessions/change_params', methods=['PUT'])
@token_auth.login_required
def change_params():
    """ Change parameters of opened sessions """
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
    json_data = request.get_json() or {}
    
    open_sessions = Session.query.filter_by(running=True).all()
    
    if len(open_sessions)==0:
        return jsonify({
            'message': "No session running. No parameters changed."
        })
    message = ""
    newparams = {}
    for session in open_sessions:
        id = session.id
        newparams[id] = {}
        for json_key in json_data.keys():
            
            if json_key == 'lots' or json_key == 'stoploss':
                try:
                    value = float(json_data[json_key])
                except:
                    return bad_request(json_key+" value is not a number")
                
                # WARNING! Assume all strategies in session share parameters
                for strategy in session.sessionstrategies:
                    if json_key == 'lots':
                        strategy.poslots = value
                    else:
                        strategy.slthr = value
                
                newparams[id][json_key] = value
                if session.newparams:
                    message = message+"WARNING! Parameter "+str(json_key)+" already changed "+\
                          "but not updated. Value overwritten.\n"
                else:
                    message = message+"Parameters updated\n"
            else:
                message = message+"WARNING! Parameter "+str(json_key)+" not allowed or value is wrong. Skipped\n"
        session.newparams = True
    db.session.commit()
    return jsonify({
        'message': message,
        'params': newparams,
    })
    
@bp.route('/traders/sessions/<int:id>/get_params', methods=['GET'])
@token_auth.login_required
def params_enquired(id):
    """ Route for parameters enquiry from trader """
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
    session = Session.query.filter_by(id=id).first()
    if session == None:
        return bad_request("Session does not exist")
    if not session.running:
        return bad_request("Session not running")
    newparams = {}
    if session.newparams:
        # build new params
        # WARNING! For now, assumed all strategies in session share parameters
        strategy = session.sessionstrategies[-1]
        newparams['lots'] = strategy.poslots
        newparams['stoploss'] = strategy.slthr
        msg = "New params"
        session.newparams = False
        db.session.commit()
    else:
        msg = "Params not updated"
    json_return = jsonify({
        'message': msg,
        'params': newparams,
    })
    return json_return

@bp.route('/traders/sessions/reset', methods=['PUT'])
@token_auth.login_required
def reset_sessions():
    """ Change parameters of opened sessions """
    return bad_request("Depricated. Not in use anymore.")
    # for key in list(params):
    #     del params[key]
    # message = "Sessions parameters reset"
    # return jsonify({
    #     'message': message,
    # })
    
@bp.route('/traders/sessions/<int:id>/positions/open', methods=['POST'])
@token_auth.login_required
def open_position(id):
    """  """
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
    session = Session.query.get(id)
    if session == None:
        return bad_request("Session does not exist.")
#    if not session.running:
#        return bad_request("Session not running.")
    json_data = request.get_json() or {}
    if 'asset' not in json_data:
        return bad_request('asset must be included.')
    code = Asset.is_asset(json_data['asset'])
    if code < 0:
        return bad_request('Asset does not exist.')
    if 'dtisoll' not in json_data:
        return bad_request('dtisoll must be included.')
    if 'bi' not in json_data:
        return bad_request('bi must be included.')
    if 'ai' not in json_data:
        return bad_request('ai must be included.')
    if 'espread' not in json_data:
        return bad_request('espread must be included.')
    if 'lots' not in json_data:
        return bad_request('lots must be included.')
    if 'direction' not in json_data:
        return bad_request('direction must be included.')
    #json_data['dtosoll'] = dt.datetime.utcnow()
    position_sch = PositionSchema()
    try:
        data_sch = position_sch.load(json_data)
        position = data_sch[0]
        #position.dtosoll = dt.datetime.utcnow()
        #print(data_sch)
        code = session.add_position(position)
        mess = "Position opened with code "+str(code)
    except ma.ValidationError as err:
        return jsonify(err.messages), 422
    
    db.session.commit()
    
    # jsonify
    result = position_sch.dump(position)
    # send email
    #if session.sessiontype == 'live':
    
    pos_dict = result[0]
    del pos_dict['positionsplits']
    del pos_dict['filecontent']
    del pos_dict['filename']
    del pos_dict['ticksdiff']
    del pos_dict['dtiist']
    del pos_dict['dtoist']
    del pos_dict['bo']
    del pos_dict['ao']
    del pos_dict['extensions']
    send_pos_email(pos_dict, pos_dict['dtisoll'], 'open')
    # update dictinary tracking open positions
    # global opened_positions
    # opened_positions[id] = {'asset':json_data['asset'],
    #                         'direction':json_data['direction'],
    #                         'dtisoll':json_data['dtisoll'],
    #                         'espread':json_data['espread']}
    return jsonify({
        'message': mess,
        'Position': result,
    })

@bp.route('/traders/positions/<int:id>/close', methods=['PUT'])
@token_auth.login_required
def close_position(id):
    """  """
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
    json_data = request.get_json() or {}
    if 'dtosoll' not in json_data:
        return bad_request('dtosoll must be included.')
    if 'bo' not in json_data:
        return bad_request('bo must be included.')
    if 'ao' not in json_data:
        return bad_request('ao must be included.')
    if 'spread' not in json_data:
        return bad_request('spread must be included.')
    if 'groisoll' not in json_data:
        return bad_request('groisoll must be included.')
    if 'roisoll' not in json_data:
        return bad_request('roisoll must be included.')
    if 'returns' not in json_data:
        return bad_request('returns must be included.')
    
    json_data['closed'] = True
    position = Position.query.filter_by(id=id).first()
    if position.closed:
        return bad_request('Position must be open.')
    if position == None:
        return bad_request('Position does not exist.')
    code = position.set_attributes(json_data)
    #print(json_data['filename'])
    #print(position.filename)
    splits = update_results(position)
    db.session.commit()
    mess = "Position closed with code "+str(code)
    result = PositionSchema().dump(position)
    
    #if Session.query.get(position.session_id).sessiontype == 'live':
    pos_dict = result[0]
    del pos_dict['positionsplits']
    del pos_dict['filecontent']
    del pos_dict['extensions']
    send_pos_email(pos_dict, pos_dict['dtosoll'], 'close')
    if len(splits)>0:
        splits_result = PositionSplitSchema().dump(splits[0])
    else:
        splits_result = []
    # global opened_positions
    # del opened_positions[id]
    return jsonify({
        'message': mess,
        'Position': result,
        'Splits':splits_result
    })

@bp.route('/traders/positions/<int:id>/upload', methods=['POST'])
@token_auth.login_required
def upload_position(id):
    """ Upload position evolution over time to DB """
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
    if 'file' not in request.files:
        bad_request("File file not included")
    file = request.files['file']
    position = Position.query.filter_by(id=id).first()
    if position == None:
        bad_request("position does not exist")
    position.filecontent = file.read()
    #print(str(position.filecontent))
    #print(position.filename)
    if position.filename==None:
        position.filename = ''
    db.session.commit()
    return jsonify({
        'message': "File "+position.filename+" added to position "+str(id)
    })
    
@bp.route('/traders/positions/<int:id>/extend', methods=['POST'])
@token_auth.login_required
def extend_position(id):
    """  """
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
    json_data = request.get_json() or {}
    position = Position.query.filter_by(id=id).first()
    if position == None:
        return bad_request('Position does not exist.')
    if position.closed:
        return bad_request('Position already closed. It cannot be extended')
    extension_sch = ExtensionSchema()
    extension = extension_sch.load(json_data)[0]
    position.add_extension(extension)
    position.nofext += 1
    position.groisoll = json_data['groi']
    #code = position.set_attributes(json_data)
    db.session.commit()
    mess = "Position extended. Number Extensions: "+str(position.nofext)
    result_pos = PositionSchema().dump(position)
    #if Session.query.get(position.session_id).sessiontype == 'live':
    pos_dict = result_pos[0]
    # update p_mc/p_md
    pos_dict['p_mc'] = extension.p_mc
    pos_dict['p_md'] = extension.p_md
    # delete unnecessary fields
    del pos_dict['positionsplits']
    del pos_dict['filecontent']
    del pos_dict['filename']
    del pos_dict['ticksdiff']
    del pos_dict['dtiist']
    del pos_dict['dtoist']
    del pos_dict['dtosoll']
    del pos_dict['groiist']
    del pos_dict['roiist']
    del pos_dict['bo']
    del pos_dict['ao']
    del pos_dict['extensions']
    #del pos_dict['closed']
    del pos_dict['spread']
    del pos_dict['slfalg']
    send_pos_email(pos_dict, extension.dt, 'extend')
    result_ext = extension_sch.dump(extension)
    #print(result_ext)
    # global opened_positions
    # opened_positions[id]['groi'] = json_data['groi']
    # opened_positions[id]['roi'] = json_data['roi']
    return jsonify({
        'message': mess,
        'Extension': result_ext,
        'Position': result_pos
    })

@bp.route('/traders/positions/<int:id>/notextend', methods=['POST'])
@token_auth.login_required
def not_extend_position(id):
    """  """
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
    json_data = request.get_json() or {}
    position = Position.query.filter_by(id=id).first()
    if position == None:
        return bad_request('Position does not exist.')
    if position.closed:
        return bad_request('Position already closed. It cannot be extended')
    position.groisoll = json_data['groi']
    db.session.commit()
    
    mess = "Position NOT extended"
    print("Position NOT extended")
    print((pd.DataFrame(json_data, index=[0])[pd.DataFrame(columns=json_data.keys()).columns.tolist()]).to_string())
    # global opened_positions
    # opened_positions[id]['groi'] = json_data['groi']
    # opened_positions[id]['roi'] = json_data['roi']
    return jsonify({
        'message': mess
    })

#@bp.route('/traders/<int:id>/delete', methods=['POST'])
#@token_auth.login_required
#def delete_trader(id):
#    """  """
#    trader = Trader.query.get_or_404(id)
#    db.session.delete(trader)
#    db.session.commit()
#    return jsonify({'Output': 'Trader deleted'})

# def get_trader(id):
#     """  """
#     trader_sch = TraderSchema()
#     trader = Trader.query.get_or_404(id)
#     # Serialize the queryset
#     result = trader_sch.dump(trader)
#     return jsonify({'trader': result})

#def get_traders():
#    """  """
#    trader_sch = TraderSchema(many=True)
#    traders = Trader.query.all()
#    # Serialize the queryset
#    result = trader_sch.dump(traders)
#    return jsonify({'traders': result})

@bp.route('/traders/sessions/set_sessiontest', methods=['PUT'])
@token_auth.login_required
def init_sessions_sessiontest():
    """  """
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
    sessions = Session.query.all()
    sessions_id = []
    for session in sessions:
        if session.sessiontest==None:
            session.sessiontest = False
            sessions_id.append(session.id)
    db.session.commit()
    return jsonify({'sessions_id':sessions_id})
    

def update_results(position):
    """ Set splits corresponding to users for the position """
    session = Session.query.filter_by(id=position.session_id).first()
    session.update(position)
    if session.sessiontype == 'live' and not session.sessiontest:
        trader = Trader.query.filter_by(id=session.trader_id).first()
        splits = []
        for usertrader in trader.users:
            usertrader.budget += usertrader.poslots*position.roiist*Config.LOT/100
            positionsplit = PositionSplit(userlots=usertrader.poslots)
            position.add_split(positionsplit)
            user = User.query.filter_by(id=usertrader.user_id).first()
            user.add_position(positionsplit)
            user.budget += usertrader.poslots*position.roiist*Config.LOT/100
            splits.append(positionsplit)
        return splits
    else:
        return []

@bp.route('/traders/account/status', methods=['PUT'])
@token_auth.login_required
def account_status():
    """ Change parameters of opened sessions """
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
    json_data = request.get_json() or {}
    print("tradername: {0:s} leverage {1:.1f} balance {2:.2f} equity {3:.2f}  profits {4:.2f}"\
              .format(json_data['tradername'], json_data['leverage'], json_data['balance'], 
                      json_data['equity'], json_data['profits']))
    # update status
    trader = Trader.query.filter_by(tradername=json_data['tradername']).first()
    if trader:
        trader.balance = json_data['balance']
        trader.leverage = json_data['leverage']
        trader.equity = json_data['equity']
        trader.profits = json_data['profits']
        db.session.commit()
    else:
        return bad_request('Trader '+json_data['tradername']+' does not exist.')
    return jsonify(json_data)

@bp.route('/traders/positions/status', methods=['PUT'])
@token_auth.login_required
def positions_status():
    """ Change parameters of opened sessions """
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
    json_data = request.get_json() or {}
    # print current state of positions
    print("Total open positions: "+str(len(json_data)))
    for asset in json_data:
        # print(asset)
        # print(json_data[asset])
        print(asset+": pos_id {0:d} volume {1:.2f} open price {2:.4f} current price {3:.4f}  swap {5:.2f} deadline in {6:d} current profit {4:.2f}"\
              .format(json_data[asset]['pos_id'], json_data[asset]['volume'], json_data[asset]['open_price'], 
                      json_data[asset]['current_price'], json_data[asset]['current_profit'], json_data[asset]['swap'], json_data[asset]['deadline']))
    # update status
    response = jsonify({'message': 'positions status updated'})
    response.status_code = 200
    return response

@bp.route('/traders/reset_positions', methods=['POST'])
@token_auth.login_required
def reset_positions():
    """ Delete all positions/positionSplits/Sessions/Extensions from DB """
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
    Extension.query.delete()
    PositionSplit.query.delete()
    Position.query.delete()
    # delete SessionStratetgy links in session
    sessions = Session.query.all()
    for session in sessions:
        session.sessionstrategies = []
    Session.query.delete()
    
    db.session.commit() 
    return jsonify({'message':'Positions reset'})


@bp.route('/traders/number_positions', methods=['GET'])
@token_auth.login_required
def get_number_positions():
    """ Get number of positions in DB """
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
    n_positions = Position.query.count()
    n_positionsplits = PositionSplit.query.count()
    n_extensions = Extension.query.count()
    n_sessions = Session.query.count()
    return jsonify({'n_positions':n_positions,
                    'n_positionsplits':n_positionsplits,
                    'n_extensions':n_extensions,
                    'n_sessions':n_sessions})

