# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24
@author: mgutierrez

Views for flask admin
"""

from flask import url_for, redirect, flash, render_template
from flask_login import current_user
from app.adm import bp
from app import db, Config, admin, login
from app.tables_test import User, Trader, Strategy, Network, Session, Position, Event
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, BaseView, expose, Admin


class MyModelView(ModelView):
    """  """
    def is_accessible(self):
        return current_user.is_authenticated and current_user.isadmin

    def inaccessible_callback(self, name, **kwargs):
        flash('Not allowed')
        return redirect(url_for('main.login'))

# class TraderView(BaseView):
#     @expose('/adm/trader')
#     def index(self):
#         return self.render('admin/trader.html')

class AccountState(BaseView):
    def __init__(self, *args, **kwargs):
        self._default_view = True
        super(AccountState, self).__init__(*args, **kwargs)
        self.admin = admin#Admin(template_mode='bootstrap3', index_view=MyAdminIndexView())

@bp.route('/adm/account')
def account():
    trader = Trader.query.filter_by(tradername='farnamstreet').first()
    return AccountState().render('admin/account.html', balance=trader.balance, 
                    leverage=trader.leverage, equity=trader.equity, profits=trader.profits)

# admin.index_view = MyAdminIndexView()

# admin.add_view(TraderView(name='Broker'))

admin.add_view(MyModelView(User, db.session))

admin.add_view(MyModelView(Trader, db.session))

admin.add_view(MyModelView(Strategy, db.session))

admin.add_view(MyModelView(Network, db.session))

admin.add_view(MyModelView(Session, db.session))

admin.add_view(MyModelView(Position, db.session))

admin.add_view(MyModelView(Event, db.session))