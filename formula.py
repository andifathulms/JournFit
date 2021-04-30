from math import exp
from sqlalchemy import create_engine
import pymysql
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sql import getLiftName

def tdeeCalc(gender, height, weight, bodyfat, activityLevel):
    
    if bodyfat == "" and gender == "Male" : 
        LBM = weight*0.407 + height*0.267 - 19.2
    elif bodyfat == "" and gender == "Female" : 
        LBM = weight*0.252 + height*0.473 - 48.3
    else : 
        LBM = weight*(100 - bodyfat)/100
    
    BMR = 370 + (21.6 * LBM)

    coeff = [1, 1.2, 1.375, 1.55, 1.725, 1.9]
    bmrList = [round(BMR * i) for i in coeff]
    TDEE = bmrList[activityLevel]
    return [TDEE, bmrList]

def bmiScore(weight,height):

    bmi = weight/pow((height/100),2)

    if bmi <= 18.5 : bmiClass = "Underweight"
    elif bmi <= 24.99 : bmiClass = "Normal Weight"
    elif bmi <= 29.99 : bmiClass = "Overweight"
    else: bmiClass = "Obese"

    return [round(bmi,2),bmiClass]

def macrosMaintenance(tdee):
    moderate = [round((30/100)*tdee/4), round((35/100)*tdee/9), round((35/100)*tdee/4)]
    lower = [round((40/100)*tdee/4), round((40/100)*tdee/9), round((20/100)*tdee/4)]
    higher = [round((30/100)*tdee/4), round((20/100)*tdee/9), round((50/100)*tdee/4)]
    return [moderate,lower,higher]

def macrosCutting(tdeeCalc):
    tdee = tdeeCalc - 500
    moderate = [round((30/100)*tdee/4), round((35/100)*tdee/9), round((35/100)*tdee/4)]
    lower = [round((40/100)*tdee/4), round((40/100)*tdee/9), round((20/100)*tdee/4)]
    higher = [round((30/100)*tdee/4), round((20/100)*tdee/9), round((50/100)*tdee/4)]
    return [moderate,lower,higher]

def macrosBulking(tdeeCalc):
    tdee = tdeeCalc + 500
    moderate = [round((30/100)*tdee/4), round((35/100)*tdee/9), round((35/100)*tdee/4)]
    lower = [round((40/100)*tdee/4), round((40/100)*tdee/9), round((20/100)*tdee/4)]
    higher = [round((30/100)*tdee/4), round((20/100)*tdee/9), round((50/100)*tdee/4)]
    return [moderate,lower,higher]

def macros(tdee):
    print(macrosMaintenance(tdee))
    print(macrosCutting(tdee))
    print(macrosBulking(tdee))

def maxMP(height):
    base = height - 98
    return [base, round(base*1.03), round(base*1.05), round(base*1.07), round(base*1.1)]

def oneRepMax(w,r):
    r1 = round((100*w/(48.8 + (53.8*exp(-0.075*r)))))
    r2 = round(0.95*r1)
    r3 = round(0.92*r1)
    return r1

def wilksFactor(w):
    cM = [-216.0475144,16.2606339,-0.002388645,-0.00113732,7.01863*pow(10,-6),-1.291*pow(10,-8)]
    cW = [594.31747775582,-27.23842536447,0.82112226871,-0.00930733913,4.731582*pow(10,-5),-9.054*pow(10,-8)]

    wilkCoeffM = 500/(cM[0] + cM[1]*w + cM[2]*pow(w,2) + 
        cM[3]*pow(w,3) + cM[4]*pow(w,4) + cM[5]*pow(w,5))

    wilkCoeffW = 500/(cW[0] + cW[1]*w + cW[2]*pow(w,2) + 
        cW[3]*pow(w,3) + cW[4]*pow(w,4) + cW[5]*pow(w,5))

    return [wilkCoeffM, wilkCoeffW]

def findBestLiftOf(lift):
    sqlEngine = create_engine('mysql+pymysql://root:@127.0.0.1', pool_recycle=3600)
    dbConnection = sqlEngine.connect()
    df = pd.read_sql("select * from journfit.lift", dbConnection);
    pd.set_option('display.expand_frame_repr', False)

    df = df[df["exercise"] == lift]
    df['oneRep'] = np.vectorize(oneRepMax)(df['weights'],df['reps'])
    df = df[df.oneRep == df.oneRep.max()]
    #print(df['oneRep'].values[0])
    return [df['dateCreated'].values[0],df['oneRep'].values[0]]
    

def estimatedPLTotal():
    bp = findBestLiftOf("BP")[1]
    bs = findBestLiftOf("BS")[1]
    dl = findBestLiftOf("DL")[1]
    #print(bp+bs+dl)
    return bp+bs+dl

def wilksScore(w):
    return wilksFactor(w)[0]*estimatedPLTotal()

def repMaxHistoryOf(lift):
    sqlEngine = create_engine('mysql+pymysql://root:@127.0.0.1', pool_recycle=3600)
    dbConnection = sqlEngine.connect()
    df = pd.read_sql("select * from journfit.lift", dbConnection);
    pd.set_option('display.expand_frame_repr', False)

    df = df[df["exercise"] == lift]
    df['oneRep'] = np.vectorize(oneRepMax)(df['weights'],df['reps'])
    df = df.groupby(['dateCreated'])
    df = df['oneRep'].max()
    df = df.reset_index()

    bl = findBestLiftOf(lift)

    ax = plt.gca()
    df.plot(kind='line',x='dateCreated',y='oneRep',ax=ax)
    ymax = bl[1]
    xmax = bl[0]
    
    ax.annotate("Best Lift", xy = (xmax,ymax), xytext=(xmax,ymax+5,),
        arrowprops=dict(facecolor='black', shrink=1))
    #arrowprops=dict(arrowstyle="-",connectionstyle="arc3,rad=0.1")
    plt.title(getLiftName(lift))
    plt.show()

if __name__ == '__main__':
    
    #print(findBestLiftOf("OHP"))
    repMaxHistoryOf("BP")
    #getLiftName("SDL")
    #estimatedPLTotal()
    #print(wilksScore(85))