# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24
@author: mgutierrez

Views for flask admin
"""

from flask import url_for, redirect, flash
from flask_login import current_user
from app import db, Config, admin, login
from app.tables_test import User, Trader, Strategy, Network, Session, Position, Event
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView


class MyModelView(ModelView):
    """  """
    def is_accessible(self):
        return current_user.is_authenticated and current_user.isadmin

    def inaccessible_callback(self, name, **kwargs):
        flash('Not allowed')
        return redirect(url_for('main.login'))

# class MyAdminIndexView(AdminIndexView):
#     """ """
#     def is_accessible(self):
#         return current_user.is_authenticated and current_user.isadmin
    
#     def inaccessible_callback(self, name, **kwargs):
#         return redirect(url_for('main.login'))

# admin.index_view = MyAdminIndexView()

admin.add_view(MyModelView(User, db.session))

admin.add_view(MyModelView(Trader, db.session))

admin.add_view(MyModelView(Strategy, db.session))

admin.add_view(MyModelView(Network, db.session))

admin.add_view(MyModelView(Session, db.session))

admin.add_view(MyModelView(Position, db.session))

admin.add_view(MyModelView(Event, db.session))