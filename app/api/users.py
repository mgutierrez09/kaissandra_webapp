# -*- coding: utf-8 -*-
"""
Created on Mon May 13 15:35:41 2019

@author: mgutierrez
"""
import datetime as dt
from flask import jsonify, request, url_for, g
from app import db, Config
from app.api import bp
from app.util import get_positions_from_splits
from app.tables_test import (User, Trader, Position, UserSchema, UserTrader, PositionSplit,
                        Deposit, Session, UserTraderSchema, PositionSplitSchema, PositionUserSchema)
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
    if g.current_user.id !=id:
        return unauthorized_request("User ID does not correspond to user credentials. Access denied")
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

@bp.route('/users/signup', methods=['POST'])
@token_auth.login_required # temporary. Only admins are able to create new users
def create_user():
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
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
    if g.current_user.id !=id:
        return unauthorized_request("User ID does not correspond to user credentials. Access denied")
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
    #response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response

# @bp.route('/users/<int:id>/traders', methods=['GET'])
# @token_auth.login_required
# def get_traders(id):
#     response = jsonify({
#         'message': 'Not implemented.'
#     })
#     return response
# #    user = User.query.get_or_404(id)
# #    page = request.args.get('page', 1, type=int)
# #    per_page = min(request.args.get('per_page', 10, type=int), 100)
# #    data = User.to_collection_dict(user.followers, page, per_page,
# #                                   'api.get_followers', id=id)
# #    return jsonify(data)

@bp.route('/users/<int:id>/funds', methods=['POST', 'PUT'])
@token_auth.login_required
def add_funds(id):
    """ Add funds to account """
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
    data = request.get_json() or {}
    user = User.query.get(id)
    if not user:
        return bad_request('User does not exist.')
    # if not user.isadmin:
    #     return bad_request('Petition denied. User is not admin')
    if 'funds' in data:
        try:
            funds = float(data['funds'])
        except:
            return bad_request('Funds must be a float number.')
        user.budget += funds
        if not user.deposit:
            user.deposit = user.budget
        else:
            user.deposit += funds
        deposit = Deposit(volume=funds)
        user.add_deposit(deposit)
        db.session.commit()
        response = jsonify({
            'message': 'Funds added. New budget: '+str(user.budget)+" Total deposited funds: "+str(user.deposit),
        })
        return response
    else:
        return bad_request('Funds must be included.')

@bp.route('/users/<int:id>/set_deposits', methods=['POST'])
@token_auth.login_required
def set_deposits(id):
    """ Add funds to account retroactively """
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
    data = request.get_json() or {}
    user = User.query.get(id)
    if not user:
        return bad_request('User does not exist.')
    
    if 'deposits' in data:
        try:
            list_deposits = [float(deposit) for deposit in data['deposits'].split(",")]
            total_deposit = sum(list_deposits)
        except:
            return bad_request('Deposits must be a list of floats separated by commas.')
        for deposit in list_deposits:
            user.add_deposit(Deposit(volume=deposit))
        user.deposit = total_deposit
        user.budget = total_deposit
        db.session.commit()
        response = jsonify({
            'message': 'Deposits added. Total deposits: '+str(user.deposit),
        })
        return response
    return bad_request('deposits must be included.')

@bp.route('/users/<int:id>/set_budget', methods=['POST'])
@token_auth.login_required
def set_budget(id):
    """ Manually set current user's budget """
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
    data = request.get_json() or {}
    user = User.query.get(id)
    if not user:
        return bad_request('User does not exist.')
    
    if 'budget' in data:
        try:
            budget = float(data["budget"])
        except:
            return bad_request('Deposits must be a list of floats separated by commas.')
        user.budget = budget
        db.session.commit()
        response = jsonify({
            'message': 'Budget set. Current budget: '+str(user.budget),
        })
        return response
    return bad_request('deposits must be included.')


@bp.route('/users/<int:id>/traders', methods=['POST'])
@token_auth.login_required
def add_trader2user(id):
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
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

@bp.route('/users/<int:id>/traders', methods=['PUT'])
@token_auth.login_required
def update_trader_user(id):
    """  """
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
    user = User.query.get(id)
    if not user:
        return bad_request('User does not exist.')
    
    data = request.get_json() or {}
    if 'tradername' not in data:
        return bad_request('Tradername should be included in json.')
    
    trader = Trader.query.filter_by(tradername=data['tradername']).first()
    if trader == None:
        return bad_request('Trader does not exist.')
    # delete tradename from json to create Schema
    del data['tradername']
    usertrader = UserTrader.query.filter_by(user_id=id, trader_id=trader.id).first()

    if usertrader == None:
        return bad_request('User-trader relationship does not exit. Call POST instead.')
    else:
        if usertrader.set_attributes(data) == -1:
            return bad_request('Bad attributes. Check them and submit again')
        db.session.commit()
        result = UserTraderSchema().dump(usertrader)
        print(usertrader.poslots)
        mess = "User-trader relationship modified"
        response = jsonify({
            'message': mess,
            'User': result,
        })
        response.status_code = 202
        return response

@bp.route('/users/<int:id>/traders', methods=['GET'])
@token_auth.login_required
def get_trader_user(id):
    """  """
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
    user = User.query.get(id)
    if not user:
        return bad_request('User does not exist.')
    
    data = request.get_json() or {}
    if 'tradername' not in data:
        return bad_request('Tradername should be included in json.')
    
    trader = Trader.query.filter_by(tradername=data['tradername']).first()
    if trader == None:
        return bad_request('Trader does not exist.')
    # delete tradename from json to create Schema
    del data['tradername']
    usertrader = UserTrader.query.filter_by(user_id=id, trader_id=trader.id).first()

    if usertrader == None:
        return bad_request('User-trader relationship does not exit. Call POST instead.')
    else:
        result = UserTraderSchema().dump(usertrader)
        mess = "User-trader relationship"
        response = jsonify({
            'message': mess,
            'User': result,
        })
        response.status_code = 202
        return response

@bp.route('/users/<int:id>/add_splits', methods=['PUT'])
@token_auth.login_required
def add_splits_to_user(id):
    """ Add splits to a user """
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
    data = request.get_json() or {}
    user = User.query.get(id)
    if not user:
        return bad_request('User does not exist.')
    if 'starting' not in data:
        return bad_request('starting field as starting date should be included')
    if 'ending' not in data:
        return bad_request('ending field as starting date should be included')
    if 'lots' not in data:
        return bad_request('lots should be included')
    try:
        lots = float(data['lots'])
    except:
        return bad_request("Incorrect format for lots. Required: float")
    try:
        init_date = dt.datetime.strptime(data['starting'],'%Y.%m.%d_%H:%M:%S')
        end_date = dt.datetime.strptime(data['ending'],'%Y.%m.%d_%H:%M:%S')
    except:
        return bad_request("Incorrect format for dates. Required: %Y.%m.%d_%H:%M:%S")
    # find positions from given date
    positions = Position.query.all()
    splits = get_positions_from_splits(user)
    pos_id_splits = [split.id for split in splits]
    added_pos_ids = []
    counter = 0
    mess = "Splits added"
    for p in positions:
        try:
            # check if dti is newwer than starting and if pos not yet in user splits
            if not p.dtiist:
                dti = p.dtisoll
            else:
                dti = p.dtiist
            #print(dti)
            pos_date = dt.datetime.strptime(dti,'%Y.%m.%d %H:%M:%S')
            session = Session.query.filter_by(id=p.session_id).first()
            if pos_date-init_date>=dt.timedelta(0) and end_date-pos_date>=dt.timedelta(0) and \
                p.id not in pos_id_splits and \
                session.sessiontype=='live' and not session.sessiontest:
                # add position to user splits
                positionsplit = PositionSplit(userlots=lots)
                p.add_split(positionsplit)
                user.add_position(positionsplit)
                #user.budget += lots*p.roiist*Config.LOT/100
                added_pos_ids.append(p.id)
                db.session.commit()
                counter += 1
        except (TypeError,ValueError):
            pass
        if counter==10:
            mess="Stopped before addind all splits"
            break
    # print(init_date)
    # print(pos_id_splits)
    #db.session.commit()
    # if len(added_pos_ids)>0:
    #     mess = "Splits added."
    # else:
    #     mess = "No splits added."
    response = jsonify({
            'message': mess,
            'pos_ids': added_pos_ids,
    })
    response.status_code = 202
    return response

@bp.route('/users/<int:id>/delete_splits', methods=['POST'])
@token_auth.login_required
def delete_splits(id):
    """ Delete user's splits """
    if not g.current_user.isadmin:
        return unauthorized_request("User is not admin. Access denied")
    user = User.query.get(id)
    if not user:
        return bad_request('User does not exist.')
    for split in user.positionsplits:
        db.session.delete(split)
    db.session.commit()
    id_splits = [split.id for split in user.positionsplits]
    return jsonify({"splits":id_splits})

@bp.route('/users', methods=['GET'])
def get_users():
    """ """
    users = User.query.all()
    usersname = [user.username for user in users]
    return jsonify({"usersname":usersname})



