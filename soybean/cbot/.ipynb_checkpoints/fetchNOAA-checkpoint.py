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

Token = 'ZnqyjnhsxDGhDNENHdnokRwIHMHJLCdo'
datatypeList = ["PRCP","SNOW","SNWD","TMAX","TMIN","TOBS","WESF"]
DATA_PATH = os.getcwd()+'/data/'
STATION_PATH = DATA_PATH+'StationID.csv'

def OneStationOneType(station_id, state, datatypeid, startdate, enddate):
    print('[NOTE]station id: ' + station_id)
    print('[NOTE]state: ' + state)
    print('[NOTE]datatype: ' + datatypeid)
    print('[NOTE]start date: ' + startdate)
    print('[NOTE]end date: ' + enddate)
    r = requests.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=%s&limit=1000&stationid=%s&startdate=%s&enddate=%s' \
                     %(datatypeid, station_id, startdate, enddate), 
                     headers={'token':Token})
    d = r.json()
    df = pd.DataFrame()
    col_name = ['DATE', '%s_%s' %(datatypeid, state)]
    dat = []
    val = []

    dat += [item['date'] for item in d['results']]
    val += [item['value'] for item in d['results']]

    df[col_name[0]] = [datetime.strptime(d, "%Y-%m-%dT%H:%M:%S") for d in dat]
    df[col_name[1]] = val
    return df

def OneStationMultiType(station_id, state, startdate, enddate):   
    df_station = pd.DataFrame()
    for ind, datatypeid in enumerate(datatypeList):
        df_temp = OneStationOneType(station_id, state, datatypeid, startdate, enddate)
        if ind == 0:
            df_station = df_temp
        else:
            df_station = pd.merge(df_station, df_temp, on='DATE', how='outer')
    return df_station

def SoybeanAreaClimate(df_stations, startdate, enddate):
    df_SAC = pd.DataFrame()
    for ind, station in enumerate(df_stations.values):
        df_temp = OneStationMultiType(station[0], station[1], startdate, enddate)
        if ind == 0:
            df_SAC = df_temp
        else:
            df_SAC = pd.merge(df_SAC, df_temp, on='DATE', how='outer')
    return df_SAC

def getDate(dash=True):
    today = date.today()
    if dash:
        return today.strftime("%Y-%m-%d")
    else:
        return today.strftime("%d%m%Y")

def filePath():
    if not os.path.isdir(DATA_PATH):
        os.makedirs(DATA_PATH)
    return DATA_PATH+'DATA_NOAA_SAC_%s.csv' %getDate(dash=False)

def main():
    df_stations = pd.read_csv(STATION_PATH)
    startdate = '2020-01-01'
    enddate = getDate()
    df = SoybeanAreaClimate(df_stations, startdate, enddate)
    file = filePath()
    print('[NOTE]saving data to %s ...' %file)
    df.to_csv(file, index=False)
    print('[NOTE]done.')

if __name__ == '__main__':
    main()