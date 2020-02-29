# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 16:17:10 2020

@author: magut
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class FilterTable(FlaskForm):
    dates = SelectField('Dates',choices=[('today','today'),('yesterday','yesterday'),('week','this week'),
                                        ('month','this month'),('YTD','YTD'),('custom','custom')])
    start_date = DateField('From', render_kw = {'disabled': 'disabled'})
    end_date = DateField('Until', render_kw = {'disabled': 'disabled'})
    submit = SubmitField('Update')