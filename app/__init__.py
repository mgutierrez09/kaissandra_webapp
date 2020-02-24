# -*- coding: utf-8 -*-
"""
Created on Sat May 11 18:16:09 2019

@author: mgutierrez
"""

from flask import Flask, redirect, url_for, flash
from config import Config
from logging.handlers import SMTPHandler
import logging
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_mail import Mail
from flask_login import LoginManager, current_user
from flask_admin import Admin, AdminIndexView


db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
mail = Mail()
login = LoginManager()
login.login_view = 'main.login'


class MyAdminIndexView(AdminIndexView):
    """ """
    def is_accessible(self):
        return current_user.is_authenticated and current_user.isadmin
    
    def inaccessible_callback(self, name, **kwargs):
        flash('Not allowed')
        return redirect(url_for('main.login'))

admin = Admin(template_mode='bootstrap3', index_view=MyAdminIndexView())

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    mail.init_app(app)
    login.init_app(app)

    #from app.adm.views import MyAdminIndexView
    admin.init_app(app)
    
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from app.adm import bp as admin_bp
    app.register_blueprint(admin_bp)
    
#    if not app.debug and not app.testing:
#        if app.config['MAIL_SERVER']:
#            auth = None
#            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
#                auth = (app.config['MAIL_USERNAME'],
#                        app.config['MAIL_PASSWORD'])
#            secure = None
#            if app.config['MAIL_USE_TLS']:
#                secure = ()
#            mail_handler = SMTPHandler(
#                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
#                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
#                toaddrs=app.config['ADMINS'], subject='Microblog Failure',
#                credentials=auth, secure=secure)
#            mail_handler.setLevel(logging.ERROR)
#            app.logger.addHandler(mail_handler)
    
    return app
    
    
from app import tables_test