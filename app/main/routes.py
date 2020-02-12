# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 15:20:43 2020

@author: magut
"""

from app import db
from app.main import bp
from flask import render_template, flash, redirect, url_for, request
from app.main.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.tables_test import User, Position
from werkzeug.urls import url_parse

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    positions = [Position.query.filter_by(id=split.position_id).first() for split in current_user.positionsplits]
    total_roi = sum([position.roiist for position in positions])
    vector_pos = [i for i in range(len(positions))]
    return render_template('index.html', title='Home', positions=positions, total_roi=total_roi, vector_pos=vector_pos)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: 
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))