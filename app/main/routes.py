# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 15:20:43 2020

@author: magut
"""
import datetime as dt
import time
from app import db, Config
from app.main import bp
from flask import render_template, flash, redirect, url_for, request, Response
from app.main.forms import LoginForm, FilterTable
from flask_login import current_user, login_user, logout_user, login_required
from app.tables_test import User, Position, LogMessage
from app.util import (calculate_performance_user, get_positions_from_splits, 
                    get_positions_dti, sort_positions, get_positions_dto, 
                    get_positions_groi, get_positions_roi, filter_positions_date)
from werkzeug.urls import url_parse

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if not  current_user.isadmin:
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
    else: return redirect('/admin')

@bp.route('/profile/<username>', methods=['GET'])
@login_required
def profile(username):
    # user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', title='Profile')

@bp.route('/dashboard/<username>', methods=['GET','POST'])
@login_required
def dashboard(username):
    if current_user.username!=username:
        return redirect(url_for('main.login'))
    user = User.query.filter_by(username=username).first_or_404()
    filterform = FilterTable()
    #get user's splits
    positions = get_positions_from_splits(user)
    # get opening datetimes of positions
    dti_positions = get_positions_dti(positions)
    if not filterform.validate_on_submit():
        # GET request
        start_date = None
        end_date = None
    else:
        # POST request
        today = dt.datetime.today()
        tomorrow = today+dt.timedelta(days=1)
        yesterday = today-dt.timedelta(days=1)
        if filterform.dates.data=='today':
            start_date = dt.datetime(today.year, today.month, today.day)
            end_date = dt.datetime(tomorrow.year, tomorrow.month, tomorrow.day)
        elif filterform.dates.data=='yesterday':
            start_date = dt.datetime(yesterday.year, yesterday.month, yesterday.day)
            end_date = dt.datetime(today.year, today.month, today.day)
        elif filterform.dates.data=='week':
            first_weekday = today-dt.timedelta(days=today.weekday())
            start_date = dt.datetime(first_weekday.year, first_weekday.month, first_weekday.day)
            end_date = dt.datetime(tomorrow.year, tomorrow.month, tomorrow.day)
            print(today.weekday())
        elif filterform.dates.data=='month':
            #first_monthday = today-dt.timedelta(days=today.day-1)
            start_date = dt.datetime(today.year, today.month, 1)
            end_date = dt.datetime(tomorrow.year, tomorrow.month, tomorrow.day)
        elif filterform.dates.data=='YTD':
            start_date = dt.datetime(today.year, 1, 1)
            end_date = dt.datetime(tomorrow.year, tomorrow.month, tomorrow.day)
        else:
            start_date = None
            end_date = None
            flash('Not implemented yet')

        # start_date_str='2020.01.06 00:00:00'
        # end_date_str='2020.01.06 04:00:00'
    print(start_date)
    print(end_date)
    filtered_dtis = filter_positions_date(positions, dti_positions, 
                                        start_date=start_date, 
                                        end_date=end_date)
    dti_positions_filtered = [dti_positions[i] for i in filtered_dtis]
    positions_filtered = [positions[i] for i in filtered_dtis]
    # get closing datetimes of positions
    dto_positions = get_positions_dto(positions_filtered)
    # get closing datetimes of positions
    groi_positions = get_positions_groi(positions_filtered)
    # get closing datetimes of positions
    roi_positions = get_positions_roi(positions_filtered)
    # get indexes ordered
    idx_ordered = sort_positions(dti_positions_filtered)
    return render_template('dashboard.html', title=username+"'s Dashboard", positions=positions_filtered, 
                            vector_pos=idx_ordered, dti_positions=dti_positions_filtered, dto_positions=dto_positions, 
                            groi_positions=groi_positions, roi_positions=roi_positions, filterform=filterform)

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

@bp.route('/favicon.ico', methods=['GET'])
#@login_required
def icon():
    return "ICON NOT ADDED"

# @bp.route('/streamNetwork')
# def streamNetwork():
#     def eventStream():
#         ass_idx = -1
#         assets = Config.ASSETS
#         indx_assets = Config.indx_assets
#         while True:
#             ass_idx = (ass_idx+1) % len(assets)
#             asset = assets[indx_assets[ass_idx]]
#             yield 'data: {}/{}\n\n'.format(get_log_network(asset), asset)
#     return Response(eventStream(), mimetype="text/event-stream")

# @bp.route('/streamTrader')
# def streamTrader():
#     def eventStream():
#         ass_idx = -1
#         assets = Config.ASSETS
#         indx_assets = Config.indx_assets
#         while True:
#             # update asset index
#             ass_idx = (ass_idx+1) % len(assets)
#             asset = assets[indx_assets[ass_idx]]
#             # wait for source data to be available, then push it
#             yield "data: {}/{}\n\n".format(get_log_trader(asset), asset)
#     return Response(eventStream(), mimetype="text/event-stream")

# def get_log_trader(asset):
#     '''this could be any function that blocks until data is ready'''
    
#     time.sleep(0.1)
#     # user = User.query.filter_by(username="kaissandra").first()
#     global tradeLogMsg
#     logmessage = LogMessage.query.filter_by(origin="TRADER", asset=asset).first()
#     if not logmessage:
#         return "WAITING FOR CONNECTION"
#     else:
#         return tradeLogMsg#logmessage.message

# def get_log_network(asset):
#     '''this could be any function that blocks until data is ready'''
#     time.sleep(0.1)
#     # user = User.query.filter_by(username="kaissandra").first()
#     global netLogMsg
#     logmessage = LogMessage.query.filter_by(origin="NETWORK", asset=asset).first()
#     if not logmessage:
#         return "WAITING FOR CONNECTION"
#     else:
#         return netLogMsg#logmessage.message
#         # s = time.ctime(time.time())