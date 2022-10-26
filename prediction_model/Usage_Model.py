# coding: utf-8
import sys

import numpy as np
import pandas as pd
from datetime import datetime
from pandas.plotting import autocorrelation_plot
import statsmodels.api as sm
from statsmodels.tsa.statespace.sarimax import SARIMAXResults as SARIMAXResults
from pandas import datetime
from pylab import rcParams
import itertools
import warnings
from sklearn.metrics import mean_absolute_error,mean_squared_error
from datetime import timedelta
import pprint
from influxdb import InfluxDBClient
from copy import deepcopy
import json

#Fitting Model and Generate Model File
def fit(data_resample,pdq,seasonal_pdq,did):
    warnings.filterwarnings("ignore")
    results_list = []
    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                mod = sm.tsa.statespace.SARIMAX(data_resample,order=param,seasonal_order=param_seasonal,
                                                enforce_stationarity=True,enforce_invertibility=True)
                results = mod.fit(disp=0)
                results_list.append([param, param_seasonal, results.aic])
            except:
                continue
    results_list = np.array(results_list)
    lowest_AIC = np.argmin(results_list[:, 2])
    
    mod = sm.tsa.statespace.SARIMAX(data_resample,order=results_list[lowest_AIC, 0],seasonal_order=results_list[lowest_AIC, 1],enforce_stationarity=False,enforce_invertibility=False)
    final_result = mod.fit()

    final_result = sm.tsa.statespace.SARIMAX(data_resample,order=results_list[lowest_AIC, 0],seasonal_order=results_list[lowest_AIC, 1],enforce_stationarity=False,enforce_invertibility=False).fit()
    final_result.save('../model/{0}.pkl'.format(did))

#Load Model File and Predict
def pred(did, start,pred_range):
    loaded = SARIMAXResults.load('../model/{0}.pkl'.format(did))
    pred_uc = loaded.get_prediction(start = start, end = start + timedelta(days= int(pred_range)))
    pred_uc_df=pd.DataFrame(pred_uc.predicted_mean)
    return pred_uc_df

#Connect to DB
def get_ifdb(db, host='localhost', port='8086', user='root', passwd='root'):
    # DB Connection
    client = InfluxDBClient(host, port, user, passwd, db)
    try:
        # connection check
        client.create_database(db)
    except Exception as e:
        print('connection fail')
        print(e)
        pass
    return client

#Read Data from DB
def get_ifdb_data(did):
    client = get_ifdb(db='water_management', host='localhost', port='8086', user='root', passwd='root')
    client.get_list_database()  # 데이터베이스 리스트 조회
    client.get_list_measurements()  # 현재 선택된 데이터베이스 measurements 리스트 조회
    data = client.query("SELECT gauge, time FROM water_usage where did = '{0}'".format(did)).get_points()
    
    df = pd.DataFrame()
    
    for point in data:
        df2 = pd.DataFrame(point, index=['time'])
        df2['time'][0] = datetime.strptime(df2['time'][0], "%Y-%m-%dT%H:%M:%SZ")
        df = df.append(df2,sort=True)
    
    return df.set_index('time')

#Get did list from DB
def get_did_list():
    client = get_ifdb(db='water_management', host='localhost', port='8086', user='root', passwd='root')
    client.get_list_database()  # 데이터베이스 리스트 조회
    client.get_list_measurements()  # 현재 선택된 데이터베이스 measurements 리스트 조회

    data = client.query('SHOW TAG VALUES FROM "water_usage" WITH KEY = "did"')

    did_list = pd.DataFrame()
    for point in data.get_points():
        df2 = pd.DataFrame(point, index=['key'])
        did_list = did_list.append(df2['value'])

    return did_list.reset_index(drop=True)

#Write Result into DB
def write_data(df, did):
    client = get_ifdb(db='water_management', host='localhost', port='8086', user='root', passwd='root')

    json_body = []
    #Declare vars here
    tablename = 'model_output'
    tag1 = 'did'
    field1 = 'predicted'

    point = {
        # initialize data
        "measurement": tablename,
        "tags": {
            tag1: ""  # 
        },
        "fields": {
            field1:0, 
        },
        "time": None,
    }

    # insert data
    for i in range(len(df)):
        np = deepcopy(point)
        np['tags'][tag1] = did
        np['fields'][field1] = df['predicted_mean'][i]

        # UTC timestamp
        np['time'] = df.index[i]

        json_body.append(np)

        # write data
        try:
            client.write_points(json_body)
            del json_body[-1]
        except:
            del json_body[-1]
            continue

def main_func():
    
    flag = sys.argv[1]
    dateRange = int(sys.arge[2])
    #Get did list
    did_list = get_did_list()
    
    if flag == 'F': #Fitting
    
        #Generateing seasonal parameter
        p=d=q=range(0,2)

        #Generate all different combinations of seasonal p, q and q triplets
        pdq = list(itertools.product(p, d, q))

        #The seasonal periodicy is  24 hours
        seasonal_para = 24
        seasonal_pdq = [(x[0], x[1], x[2], seasonal_para)for x in list(itertools.product(p, d, q))]
    
        for i in range(dateRange * 5,(dateRange + 1) * 5):
            did = did_list['key'][i]
            
            #Get data
            train_data=get_ifdb_data(did)
            fit(train_data,pdq,seasonal_pdq,did)

    elif flag == 'P': #Predicting
        for i in range(len(did_list)):
            did = did_list['key'][i]   
            
            #Date is the last timestamp from DB
            date = train_data.index[-1]

            #Get Prediction
            predicted = pred(did, date, 3)
            write_data(predicted, did)

    else : print("wrong Arguments!")

if __name__ == '__main__':
    main_func()
