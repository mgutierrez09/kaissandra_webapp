# -*- coding: utf-8 -*-
"""
Created on Sat May 11 19:03:02 2019

@author: mgutierrez
"""

import os
import jwt
import base64
from werkzeug.security import generate_password_hash, check_password_hash
from flask import url_for, current_app
from app import db, ma, Config
import re
import datetime as dt

TraderStratetgy = db.Table(
    'traderstratetgy',
    db.Column('trader_id', db.Integer, db.ForeignKey('trader.id')),
    db.Column('strategy_id', db.Integer, db.ForeignKey('strategy.id'))
)

#TraderOrale = db.Table(
#    'traderoracle',
#    db.Column('trader_id', db.Integer, db.ForeignKey('trader.id')),
#    db.Column('oracle_id', db.Integer, db.ForeignKey('oracle.id'))
#)

TraderAsset = db.Table(
    'traderasset',
    db.Column('trader_id', db.Integer, db.ForeignKey('trader.id')),
    db.Column('asset_id', db.Integer, db.ForeignKey('asset.assetname'))
)

StrategyNetwork = db.Table(
    'oraclenetwork',
    db.Column('strategy_id', db.Integer, db.ForeignKey('strategy.id')),
    db.Column('network_id', db.Integer, db.ForeignKey('network.id'))
)

#UserTrader = db.Table(
#    'usertrader',
#    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
#    db.Column('trader_id', db.Integer, db.ForeignKey('trader.id'))
#)

class UserTrader(db.Model):
    __tablename__ = 'usertrader'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    trader_id = db.Column(db.Integer, db.ForeignKey('trader.id'), primary_key=True)
    budget = db.Column(db.Float)
    leverage = db.Column(db.Float)
    poslots = db.Column(db.Float) # lots per position
    trader = db.relationship("Trader", back_populates="users")
    user = db.relationship("User", back_populates="traders")

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    isadmin = db.Column(db.Boolean)
    userid = db.Column(db.String(20), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    firstname = db.Column(db.String(64), index=True)
    surname = db.Column(db.String(64), index=True)
    address = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    datecreated = db.Column(db.DateTime, default=dt.datetime.utcnow)
    budget = db.Column(db.Float, default=0.0)
    traders = db.relationship("UserTrader", back_populates="user")
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    positionsplits = db.relationship("PositionSplit", backref="user")
    
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def validate_fields(self, data):
        """ Check if the user has valid fields. """
        if 'username' not in data or 'email' not in data or 'password' not in data:
            return -1
        if User.query.filter_by(username=data['username']).first():
            return -2
        if self.query.filter_by(email=data['email']).first() or not re.match(r"[^@]+@[^@]+\.[^@]+", data['email']):
            return -3
        if len(data['password'])<8:
            return -4
        return 1
    
    def add2db(self, data, new_user=True):
        """ Add a user to DB """
        code = 1
        for field in data:
            if hasattr(self, field):
                setattr(self, field, data[field])
            elif field!='password':
                #code = -1
                return -1
        if new_user and 'password' in data:
            self.set_password(data['password'])
        db.session.add(self)
        db.session.commit()
        return code
    
    def to_dict(self, include_email=False):
        """ Convert class to dictionary """
        data = {
            'id': self.id,
            'username': self.username,
            'datecreated': self.datecreated.isoformat() + 'Z',
            'firstname': self.firstname,
            'surname': self.surname,
            'address': self.address,
            'budget': self.budget,
            '_links': {
                'self': url_for('api.get_user', id=self.id),
                'traders': url_for('api.get_traders', id=self.id)
            }
        }
        if include_email:
            data['email'] = self.email
        return data
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def add_trader(self, usertrader):
        """  """
        if usertrader not in self.traders:
            self.traders.append(usertrader)
            #db.session.commit()
            return 1
        else:
            return 0 
        
    def set_attributes(self, data):
        """  """
        for attr in data:
            if hasattr(self, attr) and self.check_attribute(attr):
                setattr(self, attr, data[attr])
            else:
                return -1
        return 1
    
    def check_attribute(self, attr):
        """ """
        if attr == 'password_hash':
            return False
        return True
    
    def add_position(self, positionsplit):
        if positionsplit not in self.positionsplits:
            self.positionsplits.append(positionsplit)
            return 1
        else:
            return 0
        
    def get_token(self, expires_in=3600):
        now = dt.datetime.utcnow()
        if self.token and self.token_expiration > now + dt.timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + dt.timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = dt.datetime.utcnow() - dt.timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < dt.datetime.utcnow():
            return None
        return user

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)
    
class Trader(db.Model):
    __tablename__ = 'trader'
    id = db.Column(db.Integer, primary_key=True)
    tradername = db.Column(db.String(64), index=True, unique=True)
    machine = db.Column(db.String(64), index=True)
    magicnumber = db.Column(db.Integer, index=True)
    budget = db.Column(db.Float)
    performance = db.Column(db.Float, default=0.0)
    datecreated = db.Column(db.DateTime, default=dt.datetime.utcnow)
    users = db.relationship("UserTrader", back_populates="trader")
    strategies = db.relationship("Strategy",
                                 secondary=TraderStratetgy, 
                                 backref="traders")
#    oracles = db.relationship("Oracle",
#                              secondary=TraderOrale, 
#                              backref="traders")
    assets = db.relationship("Asset",
                             secondary=TraderAsset, 
                             backref="traders")
    sessions = db.relationship("Session", backref="trader")
    
    def __repr__(self):
        return '<Trader {}>'.format(self.tradername)
    
    @staticmethod
    def validate_fields(data):
        """ Check if the user has valid fields. """
        if 'tradername' not in data:
            return -1, None
        trader = Trader.query.filter_by(tradername=data['tradername']).first()
        if trader:
            return 2, trader 
        return 1, trader
    
    def check_attribute(self, attr):
        """ """
        # TODO: make sure that attribute follows the requirements
        return True
    
    def set_attributes(self, data):
        """  """
        for attr in data:
            if hasattr(self, attr) and self.check_attribute(attr):
                setattr(self, attr, data[attr])
            else:
                return -1
        return 1
        
    def add2db(self, data):
        """ Add a user to DB """
        code = self.set_attributes(data)
        if code>0:
            db.session.add(self)
            db.session.commit()
        return code
    
    def modify_attributes(self, data):
        """ modify trader attributes """
        code = self.set_attributes(data)
        if code>0:
            db.session.commit()
        return code
    
    def to_dict(self):
        """ Convert class to dictionary """
        data = {
            'id': self.id,
            'tradername': self.tradername,
            'datecreated': self.datecreated.isoformat() + 'Z',
            'machine': self.machine,
            'magicnumber': self.magicnumber,
            'budget': self.budget,
            'performance': self.performance,
            '_links': {
                'self': url_for('api.get_trader', id=self.id),
                'strategies': url_for('api.get_strategies', id=self.id),
                'oracles': url_for('api.get_oracles', id=self.id),
                'assets': url_for('api.get_assets', id=self.id),
                'sessions': url_for('api.get_sessions', id=self.id)
            }
        }
        return data
    
    def add_strategy(self, strategy):
        if strategy not in self.strategies:
            self.strategies.append(strategy)
            #db.session.commit()
            return 1
        else:
            return 0
    
        
    def add_assets(self, assets):
        """ assets = list of assets """
        code = 0
        for asset in assets:
            if asset not in self.assets:
                self.assets.append(asset)
                code += 1
#        if code > 0:
#            db.session.commit()
        return code
    
    def add_client(self, user):
        """  """
        if user not in self.users:
            self.users.append(user)
            #db.session.commit()
            return 1
        else:
            return 0 
        
    def add_session(self, session):
        if session not in self.sessions:
            self.sessions.append(session)
            return 1
        else:
            return 0
    
class Strategy(db.Model):
    __tablename__ = 'strategy'
    id = db.Column(db.Integer, primary_key=True)
    strategyname = db.Column(db.String(64), index=True, unique=True)
    spreadthr = db.Column(db.Float) # spread threshold
    mcthr = db.Column(db.Float) # market change threshold
    mdthr = db.Column(db.Float) # market direction threshold
    diropts = db.Column(db.String(4)) # direction options {'BIDS','ASKS','COMB'}
    slthr = db.Column(db.Float) # sl thr
    extthr = db.Column(db.Float) # extension thr
    poslots = db.Column(db.Float) # lots per position
    phaseshift = db.Column(db.Integer)
    
    #oracle = db.relationship("Oracle", backref=db.backref("strategy", uselist=False))
    
    oraclename = db.Column(db.String(64), index=True, unique=True)
    mw = db.Column(db.Integer) # moving window
    nexs = db.Column(db.Integer) # number events per samp
    og = db.Column(db.Float) # output gain
    symbol = db.Column(db.String(3)) # symbol from which get features: {'BID','ASK'}
    combine = db.Column(db.String(5)) # algo for combining networks {'mean','wmean',...}
    combineparams = db.Column(db.String(30)) # combine parameters if needed (COMB/BID/ASK)
    networks = db.relationship("Network",
                             secondary=StrategyNetwork, 
                             backref="strategies")
    
    def __repr__(self):
        return '<Strategy {}>'.format(self.strategyname)
    
    def check_attribute(self, attr):
        """ """
        # TODO: make sure that attribute follows the requirements
        return True
    
    def set_attributes(self, data):
        """  """
        for attr in data:
            if hasattr(self, attr) and self.check_attribute(attr):
                setattr(self, attr, data[attr])
            else:
                return -1
        return 1
    
    def add2db(self, data):
        """ Add a user to DB """
        code = self.set_attributes(data)
        if code>0:
            db.session.add(self)
            db.session.commit()
        return code
    
        
    def add_network(self, network):
        """ Add network to oracle """
        if network not in self.networks:
            self.networks.append(network)
            #db.session.commit()
            return 1
        else:
            return 0
    
class Network(db.Model):
    __tablename__ = 'network'
    id = db.Column(db.Integer, primary_key=True)
    networkname = db.Column(db.String(64), index=True, unique=True)
    weightsfile = db.Column(db.String(30))
    epoch = db.Column(db.Integer)
    
    def __repr__(self):
        return '<Network {}>'.format(self.weightsfile)
    
    def check_attribute(self, attr):
        """ """
        # TODO: make sure that attribute follows the requirements
        return True
    
    def set_attributes(self, data):
        """ Set network attributes from dict data """
        for attr in data:
            if hasattr(self, attr) and self.check_attribute(attr):
                setattr(self, attr, data[attr])
            else:
                return -1
        return 1
    
class Asset(db.Model):
    __tablename__ = 'asset'
    #id = db.Column(db.Integer, primary_key=True)
    assetname = db.Column(db.String(6), primary_key=True, index=True, unique=True)
    
    def __repr__(self):
        return '<Asset {}>'.format(self.assetname)
    
    def set_attributes(self, data):
        """ Set network attributes from dict data """
        for attr in data:
            if hasattr(self, attr) and self.check_attribute(attr):
                setattr(self, attr, data[attr])
            else:
                return -1
        return 1
    
    def add2db(self, data):
        """ Add a user to DB """
        code = self.set_attributes(data)
        if code>0:
            db.session.add(self)
            db.session.commit()
        return code
    
    @staticmethod
    def is_asset(assetname):
        """  """
        if assetname in Config.ASSETS.values():
            return 1
        return -1

class Session(db.Model):
    __tablename__ = 'session'
    id = db.Column(db.Integer, primary_key=True)
    running = db.Column(db.Boolean, default=True)
    sessionname = db.Column(db.String(64), index=True, unique=True)
    sessiontype = db.Column(db.String(10)) # backtest/live
    dti = db.Column(db.DateTime, default=dt.datetime.utcnow)
    dto = db.Column(db.DateTime)
    groisoll = db.Column(db.Float, default=0.0)
    groiist = db.Column(db.Float, default=0.0)
    roisoll = db.Column(db.Float, default=0.0)
    roiist = db.Column(db.Float, default=0.0)
    returns = db.Column(db.Float, default=0.0)
    meanspread = db.Column(db.Float)
    trader_id = db.Column(db.Integer, db.ForeignKey('trader.id'))
    positions = db.relationship("Position", backref="session")
    
    def __repr__(self):
        return '<Session {}>'.format(self.sessionname)
    
    def check_attribute(self, attr):
        """ """
        # TODO: make sure that attribute follows the requirements
        return True
    
    def set_attributes(self, data):
        """  """
        for attr in data:
            if hasattr(self, attr) and self.check_attribute(attr):
                setattr(self, attr, data[attr])
            else:
                return -1
        return 1
    
    def add_position(self, position):
        if position not in self.positions:
            self.positions.append(position)
            return 1
        else:
            return 0
    
    def update(self, position):
        """  """
        self.groisoll += float(position.groisoll)
        self.groiist += float(position.groiist)
        self.roisoll += float(position.roisoll)
        self.roiist += float(position.roiist)
        self.returns += position.lots*float(position.roiist)*Config.LOT
    
class Position(db.Model):
    __tablename__ = 'position'
    id = db.Column(db.Integer, primary_key=True)
    #asset_id = db.Column(db.String(6), db.ForeignKey('asset.assetname'))
    asset = db.Column(db.String(6))
    dtisoll = db.Column(db.String(20))
    dtosoll = db.Column(db.String(20))
    dtiist = db.Column(db.String(20))
    dtoist = db.Column(db.String(20))
    bi = db.Column(db.Float)
    bo = db.Column(db.Float)
    ai = db.Column(db.Float)
    ao = db.Column(db.Float)
    groisoll = db.Column(db.Float, default=0.0)
    groiist = db.Column(db.Float, default=0.0)
    roisoll = db.Column(db.Float, default=0.0)
    roiist = db.Column(db.Float, default=0.0)
    returns = db.Column(db.Float, default=0.0)
    espread = db.Column(db.Float)
    spread = db.Column(db.Float)
    lots = db.Column(db.Float)
    slfalg = db.Column(db.Boolean) # Make sure this is well defined
    ticksdiff = db.Column(db.Integer)
    nofext = db.Column(db.Integer, default=0) # number o extensions
    direction =  db.Column(db.Integer)
    closed = db.Column(db.Boolean, default=False)
    strategyname = db.Column(db.String(64))
    #oraclename = db.Column(db.String(64))
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    positionsplits = db.relationship("PositionSplit", backref="position")
    
    def __repr__(self):
        # TODO: Print position values in a table
        return '<Position {}>'.format(self.__tablename__)
    
    def check_attribute(self, attr):
        """ """
        # TODO: make sure that attribute follows the requirements
        return True
    
    def set_attributes(self, data):
        """  """
        for attr in data:
            if hasattr(self, attr) and self.check_attribute(attr):
                setattr(self, attr, data[attr])
            else:
                return -1
        return 1
    
    def add_split(self, positionsplit):
        if positionsplit not in self.positionsplits:
            self.positionsplits.append(positionsplit)
            return 1
        else:
            return 0
    
class PositionSplit(db.Model):
    """ Helper table that describes the split of slots among users participating
    in the position """
    __tablename__ = 'positionsplit'
    id = db.Column(db.Integer, primary_key=True)
    userlots = db.Column(db.Float)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        # TODO: Print position values in a table
        return '<PositionSplit>'

class StrategySchema(ma.ModelSchema):
    class Meta:
        model = Strategy
        sqla_session = db.session
        
#class OracleSchema(ma.ModelSchema):
#    class Meta:
#        model = Oracle
#        sqla_session = db.session
        
class NetworkSchema(ma.ModelSchema):
    class Meta:
        model = Network
        sqla_session = db.session
    
class TraderSchema(ma.ModelSchema):
    class Meta:
        model = Trader
        sqla_session = db.session
    #strategies = ma.Nested(StrategySchema)
    
class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        sqla_session = db.session
        
class UserTraderSchema(ma.ModelSchema):
    class Meta:
        model = UserTrader
        sqla_session = db.session

class SessionSchema(ma.ModelSchema):
    class Meta:
        model = Session
        sqla_session = db.session
        
class PositionSchema(ma.ModelSchema):
    class Meta:
        model = Position
        sqla_session = db.session  
        
class PositionUserSchema(ma.ModelSchema):
    class Meta:
        fields = ("id","asset", "dtiist","dtoist","groiist","roiist","spread",
                  "slfalg","nofext","direction","closed")

class PositionSplitSchema(ma.ModelSchema):
    class Meta:
        model = PositionSplit
        sqla_session = db.session  