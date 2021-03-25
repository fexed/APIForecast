import json
import APIForecast as api
import Utils as u
import CreateDatasets
from datetime import datetime, time, timedelta
from random import *

# Custom print and input
def inputYellow(str):
    CEND = '\33[0m'
    CYELLOW = '\33[33m'
    r = input(CYELLOW + str + CEND)
    return r

def printYellow(str):
    CEND = '\33[0m'
    CYELLOW = '\33[33m'
    print(CYELLOW + str + CEND)

def printGreen(str):
    CEND = '\33[0m'
    CGREEN  = '\33[32m'
    print(CGREEN + str + CEND)

# MAIN
print("")
printGreen("********************************************")
printGreen("******************* TEST *******************")
printGreen("********************************************")

# Creazione Dataset
printYellow("Generazione del dataset")
dataset = "dataset.json"
series = json.load(open(dataset, "r"))
intervals = []
interval = 300 # 5 minuti
now = datetime.combine(datetime.today(), time.min)
for i in series:
    intervals.append(now)
    now = now + timedelta(0, interval) 
lastdate = now

# Test Holt-Winters
n_preds = 288
slen = 288

alpha = 0.26
beta = 0.19
gamma = 0.00195

alpha = 0.57300
beta = 0.00667
gamma = 0.92767

alpha = 0.7
beta = 0.0000000000000000000000000000000000001
gamma = 0.8

for i in range (n_preds):
    lastdate = lastdate + timedelta(0, interval)
    intervals.append(lastdate)
#alpha, beta, gamma, SSE = api.fit_neldermead(series, n_preds)
res, dev, ubound, lbound = api.holt_winters(series, slen, alpha, beta, gamma, n_preds)


#Experimental

anomalousDay = CreateDatasets.createDataset()
anomalousDay = CreateDatasets.createAnomalousDataset()
forecastDeviation = []
forecastubound = []
forecastlbound = []

for i in range (len(anomalousDay)):
    index = i + len(series)
    dev.append(gamma * abs(anomalousDay[i] - res[index]) + (1 - gamma) * dev[i-len(series)+1])
    forecastubound.append(res[index] + 3 * dev[i])
    forecastlbound.append(res[index] - 3 * dev[i])

series += anomalousDay
ubound += forecastubound
lbound += forecastlbound

u.plot(series, intervals, res, ubound, lbound, None, f"alpha ={alpha}, beta = {beta}, gamma = {gamma}")

#prova
