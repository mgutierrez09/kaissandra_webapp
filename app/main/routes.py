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
from app.util import (calculate_performance_user, get_positions_from_splits, 
                    get_positions_dti, sort_positions, get_positions_dto, 
                    get_positions_groi, get_positions_roi)
from werkzeug.urls import url_parse

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    positions = get_positions_from_splits(current_user)
    # get datetimes of positions
    dti_positions = get_positions_dti(positions)
    # get performance
    performance = calculate_performance_user(current_user, positions, dti_positions)
    # get indexes ordered
    idx_ordered = sort_positions(dti_positions)
    # log login event
    current_user.log_event("LOGIN")
    # render page
    return render_template('index.html', title='Home', performance=performance, vector_pos=idx_ordered)

@bp.route('/profile/<username>', methods=['GET'])
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', title='Profile')

@bp.route('/dashboard/<username>', methods=['GET'])
@login_required
def dashboard(username):
    user = User.query.filter_by(username=username).first_or_404()
    positions = get_positions_from_splits(user)
    # get opening datetimes of positions
    dti_positions = get_positions_dti(positions)
    # get closing datetimes of positions
    dto_positions = get_positions_dto(positions)
    # get closing datetimes of positions
    groi_positions = get_positions_groi(positions)
    # get closing datetimes of positions
    roi_positions = get_positions_roi(positions)
    # get indexes ordered
    idx_ordered = sort_positions(dti_positions)
    return render_template('dashboard.html', title=username+"'s Dashboard", positions=positions, 
                            vector_pos=idx_ordered, dti_positions=dti_positions, dto_positions=dto_positions, 
                            groi_positions=groi_positions, roi_positions=roi_positions)

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
        current_user.log_event("LOGIN")
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    current_user.log_event("LOGOUT")
    logout_user()
    return redirect(url_for('main.index'))