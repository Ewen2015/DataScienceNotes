#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22

@author: ewen
"""
import requests
import pandas as pd
import os 
from datetime import date

URL_CME_S1 = "https://www.quandl.com/api/v3/datasets/CHRIS/CME_S1/"
DATA_PATH = os.getcwd()+'/data/'

def fetchData(URL):
    response = requests.get(URL)
    d = response.json()
    return d 

def toDataFrame(data):
    ds = data["dataset"]
    df_col = ds["column_names"]
    df = pd.DataFrame(columns=df_col)
    for l in ds["data"]:
        df = df.append(pd.DataFrame(data=[l], columns=df_col))
    return df

def getDate():
    today = date.today()
    return today.strftime("%d%m%Y")

def filePath():
    if not os.path.isdir(DATA_PATH):
        os.makedirs(DATA_PATH)
    return DATA_PATH+'DATA_CME_S1_%s.csv' %getDate()

def main():
    print('[NOTE]fetching data from %s ...' %URL_CME_S1)
    d = fetchData(URL_CME_S1)
    print('[NOTE]converting data to DataFrame...')
    df = toDataFrame(d)
    file = filePath()
    print('[NOTE]saving data to %s ...' %file)
    df.to_csv(file, index=False)
    print('[NOTE]done.')

if __name__ == '__main__':
    main()