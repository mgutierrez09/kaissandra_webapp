# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 11:48:56 2020

@author: mgutierrez
"""
import datetime as dt

from app import Config
from app.tables_test import Position

def calculate_performance_user(user, positions, dti_positions):
    """ Calculate KPIs user. """
    # get now
    now = dt.datetime.now()
    # get current day
    today = now.strftime("%Y%m%d")
    # get current week
    thisweek = now.strftime("%V")
    # get this month positions
    thismonth = now.strftime("%m")
    # get this year positions
    thisyear = now.strftime("%Y")
    # init rois
    dayly_roi = 0.0
    weekly_roi = 0.0
    monthly_roi = 0.0
    yearly_roi = 0.0
    total_roi = 0.0
    # init returns
    dayly_return = 0.0
    weekly_return = 0.0
    monthly_return = 0.0
    yearly_return = 0.0
    total_return = 0.0
    # loop over positions
    for i in range(len(dti_positions)):
        roi_i = positions[i].roiist
        lots_i = user.positionsplits[i].userlots
        if dti_positions[i].strftime("%Y%m%d")==today:
            dayly_roi += roi_i
            dayly_return += lots_i*Config.LOT*roi_i/100
        if dti_positions[i].strftime("%V")==thisweek:
            weekly_roi += roi_i
            weekly_return += lots_i*Config.LOT*roi_i/100
        if dti_positions[i].strftime("%m")==thismonth:
            monthly_roi += roi_i
            monthly_return += lots_i*Config.LOT*roi_i/100
        if dti_positions[i].strftime("%Y")==thisyear:
            yearly_roi += roi_i
            yearly_return += lots_i*Config.LOT*roi_i/100
        total_roi += roi_i
        total_return += lots_i*Config.LOT*roi_i/100
    # build performance dictionary
    performance = {"dayly_roi":dayly_roi,
                   "weekly_roi":weekly_roi,
                   "monthly_roi":monthly_roi,
                   "yearly_roi":yearly_roi,
                   "total_roi":total_roi,
                   
                   "dayly_return":dayly_return,
                   "weekly_return":weekly_return,
                   "monthly_return":monthly_return,
                   "yearly_return":yearly_return,
                   "total_return":total_return}
    
    return performance

def get_idx_same_datetime(datetimes, value, code):
    """ Get positions sharing same datetime value """
    idxs = [i for i in range(len(datetimes)) if datetimes[i].strftime(code)==value]
    return idxs

def get_positions_dti(positions):
    """ Get DTi of all positions """
    dts = []
    for position in positions:
        if type(position.dtiist)==str and len(position.dtiist)>0:
            dts.append(dt.datetime.strptime(position.dtiist,'%Y.%m.%d %H:%M:%S'))
        elif type(position.dtisoll)==str and len(position.dtisoll)>0:
            dts.append(dt.datetime.strptime(position.dtisoll,'%Y.%m.%d %H:%M:%S'))
        elif type(position.dtoist)==str and len(position.dtoist)>0:
            dts.append(dt.datetime.strptime('2018.01.01 23:59:59','%Y.%m.%d %H:%M:%S'))
    return dts

def get_positions_dto(positions):
    """ Get DTi of all positions """
    dts = []
    for position in positions:
        if type(position.dtoist)==str and len(position.dtoist)>0:
            dts.append(dt.datetime.strptime(position.dtoist,'%Y.%m.%d %H:%M:%S'))
        elif type(position.dtosoll)==str and len(position.dtosoll)>0:
            dts.append(dt.datetime.strptime(position.dtisoll,'%Y.%m.%d %H:%M:%S'))
        elif type(position.dtoist)==str and len(position.dtoist)>0:
            dts.append(dt.datetime.strptime('2018.01.01 23:59:59','%Y.%m.%d %H:%M:%S'))
    return dts

def get_positions_groi(positions):
    """ Get DTi of all positions """
    ret = []
    for position in positions:
        if type(position.groiist)==float:
            ret.append(position.groiist)
        elif type(position.groisoll)==float:
            ret.append(position.groisoll)
        else:
            ret.append(0.0)
    return ret

def get_positions_roi(positions):
    """ Get DTi of all positions """
    ret = []
    for position in positions:
        if type(position.roiist)==float:
            ret.append(position.roiist)
        elif type(position.roisoll)==float:
            ret.append(position.roisoll)
        else:
            ret.append(0.0)
    return ret

def get_positions_from_splits(user):
    """ Get positions from user splits """
    return [Position.query.filter_by(id=split.position_id).first() for split in user.positionsplits]

def sort_positions(dti_positions, reverse=True):
    """ Sort positions from older to newer """
    return [i[0] for i in sorted(enumerate(dti_positions), key=lambda x:x[1], reverse=reverse)]