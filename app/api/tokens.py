# -*- coding: utf-8 -*-
"""
Created on Mon May 13 15:43:44 2019

@author: mgutierrez
"""

from flask import jsonify, g
from app import db
from app.api import bp
from app.api.auth import basic_auth, token_auth

@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = g.current_user.get_token()
    user_id = g.current_user.id
    db.session.commit()
    return jsonify({'token': token,
                    'id':user_id})

@bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    g.current_user.revoke_token()
    db.session.commit()
    return '', 204