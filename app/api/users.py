# -*- coding: utf-8 -*-
"""
Created on Mon May 13 15:35:41 2019

@author: mgutierrez
"""

from flask import jsonify, request, url_for, g
from app import db
from app.api import bp
#from app.tables_test import User, UserSchema
from app.tables_test import (User, Trader, UserSchema, UserTrader, UserTraderSchema, 
                        PositionSplitSchema, PositionUserSchema)
from app.api.errors import bad_request, unauthorized_request
from app.api.auth import token_auth, basic_auth

@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    """  """
    if g.current_user.id !=id:
        return unauthorized_request("User ID does not correspond to user credentials. Access denied")
    user = User.query.get_or_404(id)
    result = UserSchema().dump(user)
    response = jsonify({
        'User': result,
    })
    return response

@bp.route('/users/<int:id>/positions/all', methods=['GET'])
@token_auth.login_required
def get_positions_user(id):
    """  """
    user = User.query.filter_by(id=id).first()
    result_split = PositionSplitSchema(many=True).dump(user.positionsplits)
    positions = []
    for split in user.positionsplits:
        positions.append(split.position)
    result_pos = PositionUserSchema(many=True).dump(positions)
    return jsonify({
        'Positions':result_pos,
        'Splits':result_split
    })

@bp.route('/users/<int:id>/create', methods=['POST'])
@token_auth.login_required # temporary. Only admins are able to create new users
def create_user():
    admin_user = User.query.get(id)
    if not admin_user and not admin_user.isadmin:
        return bad_request('Only admins can create users')
    data = request.get_json() or {}
    user = User()
    # Validate fields
    code = user.validate_fields(data)
    if code==-1:
        return bad_request('must include username, email and password fields')
    if code==-2:
        return bad_request('please use a different username')
    if code==-3:
        return bad_request('please use a different email address')
    if code==-4:
        return bad_request('pasword has to contain at least 8 characters')
    if code<0:
        return bad_request('unkown error when validating user')
    if 'isadmin' in data:
        if data['isadmin'] == 'True' or data['isadmin'] == 'true' or\
           data['isadmin'] == 'y' or data['isadmin'] == 'yes' or data['isadmin'] == '1':
            data['isadmin'] = True
        else:
            data['isadmin'] = False
    else:
        data['isadmin'] = False
    # add to DB
    if user.add2db(data)==-1:
        return bad_request('please use valid user fields')
    user_sch = UserSchema()
    result = user_sch.dump(user)
    mess = "User created"
    response = jsonify({
        'message': mess,
        'User': result,
    })
    response.status_code = 201
    #response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response

@bp.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def modify_user(id):
    """  """
    user = User.query.get(id)
    if user == None:
        return bad_request('User does not exist.')
    json_data = request.get_json() or {}
    if user.set_attributes(json_data) == -1:
        return bad_request('Attributes not allowed.')
    result = UserSchema().dump(user)
    mess = "User modified"
    response = jsonify({
        'message': mess,
        'User': result,
    })
    response.status_code = 202
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response

@bp.route('/users/<int:id>/traders', methods=['GET'])
@token_auth.login_required
def get_traders(id):
    response = jsonify({
        'message': 'Not implemented.'
    })
    return response
#    user = User.query.get_or_404(id)
#    page = request.args.get('page', 1, type=int)
#    per_page = min(request.args.get('per_page', 10, type=int), 100)
#    data = User.to_collection_dict(user.followers, page, per_page,
#                                   'api.get_followers', id=id)
#    return jsonify(data)

@bp.route('/users/<int:id>/funds', methods=['POST', 'PUT'])
@token_auth.login_required
def add_funds(id):
    """ Add funds to account """
    data = request.get_json() or {}
    user = User.query.get(id)
    if not user:
        return bad_request('User does not exist.')
    if 'funds' in data:
        try:
            funds = float(data['funds'])
        except:
            return bad_request('Funds must be a float number.')
        user.budget += funds
        db.session.commit()
        response = jsonify({
            'message': 'Funds added. New budget: '+str(user.budget),
        })
        return response
    else:
        return bad_request('Funds must be included.')
    

@bp.route('/users/<int:id>/traders', methods=['POST', 'PUT'])
@token_auth.login_required
def add_trader(id):
    user = User.query.get(id)
    if not user:
        return bad_request('User does not exist.')
    
    data = request.get_json() or {}
    if 'tradername' not in data or 'budget' not in data or \
        'leverage' not in data or 'poslots' not in data:
        return bad_request('tradername, budget, leverage and poslots must be specified.')
    try:
        budget = float(data['budget'])
        poslots = float(data['poslots'])
        leverage = float(data['leverage'])
    except:
        return bad_request('Error in the inputs. Make sure they are float numbers.')
    if user.budget<budget:
         return bad_request('User has not enough budget. Please add first funds')
    trader = Trader.query.filter_by(tradername=data['tradername']).first()
    if trader == None:
        return bad_request('Trader does not exist.')
    #trader.add_client(user)
    usertrader = UserTrader.query.filter_by(user_id=id, trader_id=trader.id).first()
    print(usertrader)
    if usertrader == None:
        code = 1
        usertrader = UserTrader(user_id=id, trader_id=trader.id, 
                                budget=budget, leverage=leverage, 
                                poslots=poslots)
        usertrader.trader = trader
        user.add_trader(usertrader)
    else:
        # usertrader assotiation already exists
        code = 0
        usertrader.budget = data['budget']
        usertrader.leverage = data['leverage']
        usertrader.poslots = data['poslots']
#        return bad_request('usertrader assotiation already exists. Case not im'+
#                           'plemented yet')
    # user.budget += float(data['budget'])
    db.session.commit()
    user_sch = UserSchema()
    usertrader_sch = UserTraderSchema(many=True)
    usertraders = UserTrader.query.filter_by(user_id=id).all()
#    
    if code == 1:
        mess = "Trader adder to user"
        status_code = 201
    elif code == 0:
        mess = 'User-trader association already exists. Parameters updated'
        status_code = 202
    else:
        return bad_request('Something happened when strategy added to trader. Check fields and try again')
    result_user = user_sch.dump(user)
    result_usertraders = usertrader_sch.dump(usertraders)
    response = jsonify({
        'message': mess,
        'User': result_user,
        'UserTraders':result_usertraders
    })
    response.status_code = status_code
    #response.headers['Location'] = url_for('api.get_strategy', id=trader.id)
    return response