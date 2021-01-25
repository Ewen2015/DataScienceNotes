#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22

@author: ewen
"""
import requests
import pandas as pd
import json
from datetime import datetime, date
import os

DATA_PATH = os.getcwd()+'/data/'
STATION_PATH = DATA_PATH+'StationID.csv'

datatypeList = ["PRCP","SNOW","SNWD","TMAX","TMIN","TOBS","WESF"]
df_stations = pd.read_csv(STATION_PATH)
token = 'ZnqyjnhsxDGhDNENHdnokRwIHMHJLCdo'


def SoybeanAreaClimate(df_stations, datatypeList, startdate, enddate, token, limit):
    d = _requestNOAA(df_stations, datatypeList, startdate, enddate, token, limit)
    df_SAC = _MultiStationMultiType(d, df_stations)
    return df_SAC

def _requestNOAA(df_stations, datatypeList, startdate, enddate, token, limit=1000):
    stationLine = ''
    for s in df_stations.STATIONID:
        stationLine += 'stationid=%s&' %s
    datatypeLine = ''
    for t in datatypeList:
        datatypeLine += 'datatypeid=%s&' %t
    r = requests.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&%slimit=%s&%sstartdate=%s&enddate=%s' \
                     %(datatypeLine, limit, stationLine, startdate, enddate),
                     headers={'token':token})
    print('[NOTE]request status: %s' %r.status_code)
    d = r.json()
    return d

def _OneStationOneType(d, stationid, state, datatypeid):
    print('[NOTE]station id: ' + stationid)
    print('[NOTE]state: ' + state)
    print('[NOTE]datatype: ' + datatypeid)

    df = pd.DataFrame()
    col_name = ['DATE', '%s_%s' %(datatypeid, state)]
    dat = []
    val = []

    for item in d['results']:
        if item['datatype'] == datatypeid and item['station'] == stationid:
            dat += [item['date']]
            val += [item['value']]

    df[col_name[0]] = [datetime.strptime(d, "%Y-%m-%dT%H:%M:%S") for d in dat]
    df[col_name[1]] = val
    return df

def _OneStationMultiType(d, station_id, state, datatypeList):   
    df_station = pd.DataFrame()
    for ind, datatypeid in enumerate(datatypeList):
        df_temp = _OneStationOneType(d, station_id, state, datatypeid)
        if ind == 0:
            df_station = df_temp
        else:
            df_station = pd.merge(df_station, df_temp, on='DATE', how='outer')
    return df_station

def _MultiStationMultiType(d, df_stations):
    df_area = pd.DataFrame()
    for ind, station in enumerate(df_stations.values):
        df_temp = _OneStationMultiType(d, station[0], station[1], datatypeList)
        if ind == 0:
            df_area = df_temp
        else:
            df_area = pd.merge(df_area, df_temp, on='DATE', how='outer')
    return df_area


def getDate(dash=True):
    today = date.today()
    if dash:
        return today.strftime("%Y-%m-%d")
    else:
        return today.strftime("%d%m%Y")

def filePath(startdate, enddate):
    if not os.path.isdir(DATA_PATH):
        os.makedirs(DATA_PATH)
    return DATA_PATH+'DATA_NOAA_SAC_%s_%s.csv' %(startdate, enddate)

def main():
    startdate = '2020-07-01'
    enddate = '2020-12-31'
    limit = 1000
    df = SoybeanAreaClimate(df_stations, datatypeList, startdate, enddate, token, limit)
    file = filePath(startdate, enddate)
    print('[NOTE]saving data to %s ...' %file)
    df.to_csv(file, index=False)
    print('[NOTE]done.')

if __name__ == '__main__':
    main()