# -*- coding: utf-8 -*-
"""
Created on Tue May 14 11:00:24 2019

@author: mgutierrez
"""

import datetime as dt
from flask import jsonify, request, url_for, g
from app import db, ma, Config
from app.api import bp
from app.tables import (Trader, Strategy, Asset, Network, Session, Position, PositionSplit,
                        User, TraderSchema, StrategySchema, NetworkSchema, SessionSchema, 
                        PositionSchema, PositionSplitSchema)
from app.api.errors import bad_request, error_response, unauthorized_request
from app.api.auth import token_auth

str_sch = StrategySchema()
#oracle_sch = OracleSchema()
network_sch = NetworkSchema()

@bp.route('/traders/<int:id>', methods=['GET'])
@token_auth.login_required
#@is_admin
def get_trader_entry(id):
    """  """
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
    #jsonify(Trader.query.get_or_404(id).to_dict())
    return get_trader(id)

@bp.route('/traders', methods=['GET'])
@token_auth.login_required
def traders():
    return get_traders()

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
    
@bp.route('/traders/sessions', methods=['GET'])
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
    
@bp.route('/traders/sessions/all', methods=['GET'])
@token_auth.login_required
def get_sessions():
    """  """
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
    #json_data = request.get_json() or {}
#    if 'sessionname' not in json_data:
#        return bad_request('sessionname must be included.')
    sessions = Session.query.all()
    result = SessionSchema(many=True).dump(sessions)
    return jsonify({
        'Sessions': result,
    })
    
@bp.route('/traders/strategies/all', methods=['GET'])
@token_auth.login_required
def get_strategies():
    """  """
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
    str_sch = StrategySchema(many=True)
    strategies = Strategy.query.all()
    # Serialize the queryset
    result = str_sch.dump(strategies)
    return jsonify({'strategies': result})

@bp.route('/traders/strategies/<int:id>', methods=['GET'])
@token_auth.login_required
def get_strategy(id):
    """  """
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
    strategy = Strategy.query.filter_by(id=id).first()
    # Serialize the queryset
    result = StrategySchema().dump(strategy)
    return jsonify({'strategy': result})

@bp.route('/traders/<int:id>/strategies', methods=['GET'])
@token_auth.login_required
def get_strategies_trader(id):
    """  """
    str_sch = StrategySchema(many=True)
    trader = Trader.query.filter_by(id=id).first()
    strategies = trader.strategies
    # Serialize the queryset
    result = str_sch.dump(strategies)
    return jsonify({'strategies': result})

@bp.route('/traders/networks/all', methods=['GET'])
@token_auth.login_required
def get_networks():
    """  """
    networks = Network.query.all()
    return jsonify({'networks':NetworkSchema(many=True).dump(networks)})

@bp.route('/traders/strategies/<int:id>/networks', methods=['GET'])
@token_auth.login_required
def get_networks_from_strategy(id):
    """  """
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
    position = Position.query.filter_by(id=id).first()
    result = PositionSchema().dump(position)
    print(result)
    return jsonify({
        'Position':result
    })

@bp.route('/traders/positions/all', methods=['GET'])
@token_auth.login_required
def get_positions():
    """  """
    positions = Position.query.all()
    
    result = PositionSchema(many=True).dump(positions)
    return jsonify({
        'Positions':result
    })
    
@bp.route('/traders/sessions/<int:id>/positions', methods=['GET'])
@token_auth.login_required
def get_positions_from_session(id):
    """  """
    session = Session.query.filter_by(id=id).first()
    if session == None:
        return bad_request('Session does not exist')
    result = PositionSchema(many=True).dump(session.positions)
    return jsonify({
        'Positions':result
    })
    
@bp.route('/traders/positions/filter', methods=['GET'])
@token_auth.login_required
def get_positions_filter():
    """  """
    data = request.get_json() or {}
    if 'asset' in data:
        positions = Position.query.filter_by(asset=data['asset']).all()
    
    result = PositionSchema(many=True).dump(positions)
    return jsonify({
        'Positions':result
    })
    
@bp.route('/traders', methods=['POST','PUT'])
@token_auth.login_required
def set_trader():
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
        response.status_code = 202
        response.headers['Location'] = url_for('api.get_trader_entry', id=trader.id)
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
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_trader_entry', id=trader.id)
    return response

@bp.route('/traders/<int:id>/strategies', methods=['POST', 'PUT'])
@token_auth.login_required
def set_strategy(id):
    """  """
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
#    print("strategy.strategyname")
#    print(strategy.strategyname)
    list_strategies = Strategy.query.all()
    new_strategy = data[0]
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
    db.session.commit()
    
    if code == 1:
        mess = 'New stratedy added'
        status_code = 201
    elif code == 0:
        mess = 'Strategy already existed. Parameters updated'
        status_code = 202
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
    print(list_assetnames)
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
    return jsonify({
        'message': mess,
        'Session': result,
    })
    
@bp.route('/traders/sessions/<int:id>/close', methods=['PUT'])
@token_auth.login_required
def close_session(id):
    """  """
    session = Session.query.filter_by(id=id).first()
    if session == None:
        bad_request("Session does not exist")
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
  
@bp.route('/traders/sessions/<int:id>/positions/open', methods=['POST'])
@token_auth.login_required
def open_position(id):
    """  """
    session = Session.query.get(id)
    if session == None:
        return bad_request("Session does not exist.")
    if not session.running:
        return bad_request("Session not running.")
    json_data = request.get_json() or {}
    if 'asset' not in json_data:
        return bad_request('asset must be included.')
    code = Asset.is_asset(json_data['asset'])
    if code < 0:
        return bad_request('Asset '+json_data['asset']+' does not exist.')
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
        print(data_sch)
        code = session.add_position(position)
        mess = "Position opened with code "+str(code)
    except ma.ValidationError as err:
        return jsonify(err.messages), 422
    
    db.session.commit()
    result = position_sch.dump(position)
    return jsonify({
        'message': mess,
        'Position': result,
    })

@bp.route('/traders/positions/<int:id>/close', methods=['PUT'])
@token_auth.login_required
def close_position(id):
    """  """
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
    print(type(json_data['roisoll']))
    print(json_data['groisoll'])
    code = position.set_attributes(json_data)
    print(type(position.groisoll))
    splits = update_results(position)
    db.session.commit()
    mess = "Position closed with code "+str(code)
    result = PositionSchema().dump(position)
    print(splits[0].userlots)
    splits_result = PositionSplitSchema().dump(splits[0])
    return jsonify({
        'message': mess,
        'Position': result,
        'Splits':splits_result
    })
    
    
@bp.route('/traders/positions/<int:id>/extend', methods=['PUT'])
@token_auth.login_required
def extend_position(id):
    """  """
    #json_data = request.get_json() or {}
    position = Position.query.filter_by(id=id).first()
    if position == None:
        return bad_request('Position does not exist.')
    if position.closed:
        return bad_request('Position already closed. It cannot be extended')
    position.nofext += 1
    
    #code = position.set_attributes(json_data)
    db.session.commit()
    mess = "Position extended. Number Extensions: "+str(position.nofext)
    result = PositionSchema().dump(position)
    return jsonify({
        'message': mess,
        'Position': result,
    })

#@bp.route('/traders/<int:id>/delete', methods=['POST'])
#@token_auth.login_required
#def delete_trader(id):
#    """  """
#    trader = Trader.query.get_or_404(id)
#    db.session.delete(trader)
#    db.session.commit()
#    return jsonify({'Output': 'Trader deleted'})

def get_trader(id):
    """  """
    trader_sch = TraderSchema()
    trader = Trader.query.get_or_404(id)
    # Serialize the queryset
    result = trader_sch.dump(trader)
    return jsonify({'trader': result})

def get_traders():
    """  """
    trader_sch = TraderSchema(many=True)
    traders = Trader.query.all()
    # Serialize the queryset
    result = trader_sch.dump(traders)
    return jsonify({'traders': result})

def update_results(position):
    """ Set splits corresponding to users for the position """
    session = Session.query.filter_by(id=position.session_id).first()
    session.update(position)
    trader = Trader.query.filter_by(id=session.trader_id).first()
    splits = []
    for usertrader in trader.users:
        usertrader.budget += usertrader.poslots*position.roiist*Config.LOT
        positionsplit = PositionSplit(userlots=usertrader.poslots)
        position.add_split(positionsplit)
        user = User.query.filter_by(id=usertrader.user_id).first()
        user.add_position(positionsplit)
        splits.append(positionsplit)
    return splits

#def update_session(session, position):
#    """  """
#    pass