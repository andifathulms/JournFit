from math import exp
from sqlalchemy import create_engine
import pymysql
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from model import Connection
import csv
import io
from PIL import Image

def getLastSession():
    query = "SELECT MAX(id) FROM session"
    record = ""
    con = Connection(query,record)
    user = con.fetchOneQuerySQL()

    query = """
            SELECT user FROM session 
            WHERE id = %s
            """
    record = (user[0],)
    con = Connection(query,record)
    result = con.fetchOneQuerySQL()
    return result[0]

def checkLoginValid(username,password):
    query = "SELECT password FROM user WHERE name = %s"
    record = (username,)
    con = Connection(query,record)
    result = con.fetchOneQuerySQL()
    
    if result == None:
        return 0
    elif result[0] != password:
        return -1
    else:
        return 1

def idFromUser(user):
    query = "SELECT user_id FROM user WHERE name = %s"
    record = (user,)
    con = Connection(query,record)
    result = con.fetchOneQuerySQL()
    return result[0]

def ifUser(username):
    query = "SELECT user_id FROM user WHERE name = %s"
    record = (username,)
    con = Connection(query,record)
    result = con.fetchOneQuerySQL()
    if result == None:
        return 0
    else:
        return result[0]

def listOfExcercise():
    query = "SELECT name FROM excercise ORDER BY type DESC, name"
    record = ""
    con = Connection(query,record)
    result = con.fetchAllQuerySQL()
    exc = [r[0] for r in result]
    #exc.append(" ")
    return exc

def getLiftName(lift):
    query = "SELECT name FROM excercise WHERE abbreviation = %s"
    record = (lift,)
    con = Connection(query,record)
    result = con.fetchOneQuerySQL()
    return result[0]

def countRecordOf(user):
    query = "SELECT COUNT(user_id) FROM lift WHERE user_id = %s"
    record = (user,)
    con = Connection(query,record)
    result = con.fetchOneQuerySQL()
    return result[0]

def countLoginOf(user):
    query = "SELECT COUNT(user) FROM session WHERE user = %s"
    record = (user,)
    con = Connection(query,record)
    result = con.fetchOneQuerySQL()
    return result[0]

def countPswChangeOf(user):
    query = "SELECT COUNT(user_id) FROM passwordchanges WHERE user_id = %s"
    record = (user,)
    con = Connection(query,record)
    result = con.fetchOneQuerySQL()
    return result[0]

def getLastFiveSession(user):
    query = "SELECT dateLogin FROM session WHERE user = %s ORDER BY id DESC LIMIT 5"
    record = (user,)
    con = Connection(query,record)
    result = con.fetchAllQuerySQL()
    temp = [r[0] for r in result]
    res = [r.strftime('%Y-%m-%d %H:%M:%S') for r in temp]
    res = res + ["","","",""]
    return res

def getLastFiveRecord(user):
    query = "SELECT DISTINCT dateCreated FROM lift WHERE user_id = %s ORDER BY dateCreated DESC LIMIT 5"
    record = (user,)
    con = Connection(query,record)
    result = con.fetchAllQuerySQL()
    temp = [r[0] for r in result]
    res = [r.strftime('%Y-%m-%d') for r in temp]
    res = res + ["","","","",""]
    return res

def returnDateLogin(user_id):
    query = "SELECT DISTINCT dateCreated FROM lift WHERE user_id = %s"
    record = (user_id,)
    #result = list(fetchAllQuerySQL(query,record))
    con = Connection(query,record)
    result = con.fetchAllQuerySQL()
    date = [d[0] for d in result]
    dateString = [dt.strftime("%Y-%m-%d") for dt in date]
    return dateString

def returnDatePlan(user_id):
    query = "SELECT DISTINCT dateCreated FROM plan WHERE user_id = %s"
    record = (user_id,)
    #result = list(fetchAllQuerySQL(query,record))
    con = Connection(query,record)
    result = con.fetchAllQuerySQL()
    date = [d[0] for d in result]
    dateString = [dt.strftime("%Y-%m-%d") for dt in date]
    return dateString

def fromExcToAbr(exc):
    query = "SELECT abbreviation FROM excercise WHERE name = %s"
    record = (exc,)
    con = Connection(query,record)
    result = con.fetchOneQuerySQL()
    return result[0]

def returnMinDate(user):
    query = "SELECT MIN(dateCreated) FROM lift WHERE user_id = %s"
    record = (user,)
    con = Connection(query,record)
    result = con.fetchOneQuerySQL()
    try:
        return result[0].strftime("%Y-%m-%d")
    except:
        return datetime.now().strftime('%Y-%m-%d')

def excRowFromDB(result): #Retrieve query from SQL then make it list of App ready
    compList = []
    for i in range(0,7):
        row = [data for data in result if data[3] == i+1]
        try:
            base = [i+1, row[0][0]]
            for j in range(0,6):
                try:
                    base.append(row[j][1])
                    base.append(row[j][2])
                    base.append(row[j][4])
                except: 
                    continue
            compList.append(base)
        except Exception as ex:
            msg = f'Error : {type(ex).__name__} ,arg = {ex.args}'
            continue
    print(compList)    
    return compList

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

def powerliftingWeight(height,gender):
    if gender == "Male":
        if height >= 186 :
            mf = "140 kg"
            ipf = "120 kg+"
        elif height >= 177.5 :
            mf = "125 kg"
            ipf = "120 kg"
        elif height >= 174.5 :
            mf = "100 kg"
            ipf = "105 kg"
        elif height >= 171 :
            mf = "90 kg"
            ipf = "93 kg"
        elif height >= 168 :
            mf = "82.5 kg"
            ipf = "83 kg"
        elif height >= 164 :
            mf = "75 kg"
            ipf = "74 kg"
        elif height >= 160 :
            mf = "67.5 kg"
            ipf = "66 kg"
        elif height >= 155 :
            mf = "60 kg"
            ipf = "59 kg"
    else:
        if height >= 186 :
            mf = "90 kg"
            ipf = "84 kg+"
        elif height >= 177.5 :
            mf = "82.5 kg"
            ipf = "84 kg"
        elif height >= 174.5 :
            mf = "75 kg"
            ipf = "76 kg"
        elif height >= 171 :
            mf = "67.5 kg"
            ipf = "69 kg"
        elif height >= 168 :
            mf = "60 kg"
            ipf = "63 kg"
        elif height >= 164 :
            mf = "56 kg"
            ipf = "57 kg"
        elif height >= 160 :
            mf = "52 kg"
            ipf = "52 kg"
        elif height >= 155 :
            mf = "48 kg"
            ipf = "47 kg"

    return [mf,ipf]

def olyWeight(height,gender):
    if gender == "Male":
        if height >= 190:
            oly = "109 kg+"
            iwf = "109 kg+"
        elif height >= 178:
            oly = "109 kg"
            iwf = "109 kg"
        elif height >= 175:
            oly = "109 kg"
            iwf = "102 kg"
        elif height >= 173:
            oly = "96 kg"
            iwf = "96 kg"
        elif height >= 170:
            oly = "96 kg"
            iwf = "89 kg"
        elif height >= 167:
            oly = "81 kg"
            iwf = "81 kg"
        elif height >= 163:
            oly = "73 kg"
            iwf = "73 kg"
        elif height >= 160:
            oly = "67 kg"
            iwf = "67 kg"
        elif height >= 155:
            oly = "61 kg"
            iwf = "61 kg"
        elif height >= 150:
            oly = "61 kg"
            iwf = "55 kg"
    else:
        if height >= 190:
            oly = "87 kg+"
            iwf = "87 kg+"
        elif height >= 178:
            oly = "87 kg"
            iwf = "87 kg"
        elif height >= 175:
            oly = "87 kg"
            iwf = "81 kg"
        elif height >= 173:
            oly = "76 kg"
            iwf = "76 kg"
        elif height >= 170:
            oly = "76 kg"
            iwf = "71 kg"
        elif height >= 167:
            oly = "64 kg"
            iwf = "64 kg"
        elif height >= 163:
            oly = "59 kg"
            iwf = "59 kg"
        elif height >= 160:
            oly = "55 kg"
            iwf = "55 kg"
        elif height >= 155:
            oly = "49 kg"
            iwf = "49 kg"
        elif height >= 150:
            oly = "49 kg"
            iwf = "45 kg"
    return[oly,iwf]

def bodybuildingWeight(height):
    if height > 198:
        cbd = (height - 100) + 10
        cph = (height - 100) + 17
    elif height > 190:
        cbd = (height - 100) + 9
        cph = (height - 100) + 15
    elif height > 180:
        cbd = (height - 100) + 8
        cph = (height - 100) + 13
    elif height > 175:
        cbd = (height - 100) + 6
        cph = (height - 100) + 11
    elif height > 171:
        cbd = (height - 100) + 4
        cph = (height - 100) + 8
    elif height > 168:
        cbd = (height - 100) + 2
        cph = (height - 100) + 6
    else:
        cbd = (height - 100)
        cph = (height - 100) + 4
    return [cbd,cph]

def oneRepMax(w,r):
    r1 = round((100*w/(48.8 + (53.8*exp(-0.075*r)))))
    r2 = round(0.95*r1)
    r3 = round(0.92*r1)
    return r1

def oneRepMaxBW(bw,w,r):
    r1 = round((100*(bw + w)/(48.8 + (53.8*exp(-0.075*r))))) - bw
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

def findBestLiftOf(lift,id):
    sqlEngine = create_engine('mysql+pymysql://root:@127.0.0.1', pool_recycle=3600)
    dbConnection = sqlEngine.connect()
    df = pd.read_sql("select * from journfit.lift WHERE user_id =%s", dbConnection, params=(id,));
    pd.set_option('display.expand_frame_repr', False)
    try:
        df = df[df["exercise"] == lift]
        df['oneRep'] = np.vectorize(oneRepMax)(df['weights'],df['reps'])
        df = df[df.oneRep == df.oneRep.max()]
        #print(df['oneRep'].values[0])
        return [df['dateCreated'].values[0],df['oneRep'].values[0],df['weights'].values[0],df['reps'].values[0]]
    except:
        return ["N/A",0,"N/A","N/A"]

def findBestLiftBWOf(lift,bw,id):
    sqlEngine = create_engine('mysql+pymysql://root:@127.0.0.1', pool_recycle=3600)
    dbConnection = sqlEngine.connect()
    df = pd.read_sql("select * from journfit.lift WHERE user_id =%s", dbConnection, params=(id,));
    pd.set_option('display.expand_frame_repr', False)
    try:
        df = df[df["exercise"] == lift]
        df['oneRep'] = np.vectorize(oneRepMaxBW)(bw,df['weights'],df['reps'])
        df = df[df.oneRep == df.oneRep.max()]
        #print(df['oneRep'].values[0])
        return [df['dateCreated'].values[0],df['oneRep'].values[0]]
    except:
        return ["N/A",0]

    

def estimatedPLTotal():
    bp = findBestLiftOf("BP")[1]
    bs = findBestLiftOf("BS")[1]
    dl = findBestLiftOf("DL")[1]
    #print(bp+bs+dl)
    return bp+bs+dl

def wilksScore(w):
    return wilksFactor(w)[0]*estimatedPLTotal()

def repMaxHistoryOf(lift,id):
    sqlEngine = create_engine('mysql+pymysql://root:@127.0.0.1', pool_recycle=3600)
    dbConnection = sqlEngine.connect()
    query = "select * from journfit.lift where user_id = %s"
    df = pd.read_sql_query(query, dbConnection, params=[id]);
    pd.set_option('display.expand_frame_repr', False)

    df = df[df["exercise"] == lift]
    df['oneRep'] = np.vectorize(oneRepMax)(df['weights'],df['reps'])
    df = df.groupby(['dateCreated'])
    df = df['oneRep'].max()
    df = df.reset_index()

    bl = findBestLiftOf(lift,id)

    ax = plt.gca()
    df.plot(kind='line',x='dateCreated',y='oneRep',ax=ax)
    ymax = bl[1]
    xmax = bl[0]
    
    ax.annotate("Best Lift", xy = (xmax,ymax), xytext=(xmax,ymax+5,),
        arrowprops=dict(facecolor='black', shrink=1))
    #arrowprops=dict(arrowstyle="-",connectionstyle="arc3,rad=0.1")
    #size = (1071,401)
    #plt.figure(figsize=size)
    plt.title(getLiftName(lift))
    plt.rcParams["figure.figsize"] = (11,4)
    return plt
    #plt.show()

def plotToImage(plt):
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    im = Image.open(buf)
    #im.show()
    return im
    #buf.close()

def returnDictFromCSV(weight):
    file = f'csv\\{weight}.csv'
    with open(file, newline="") as f:
        reader = csv.reader(f)
        data = list(reader)

    result = []
    for d in data:
        result.append(d[0].split(";"))
    
    resultDict = {}
    for r in result:
        resultDict[r[0]] = r[1:]

    #print(resultDict)
    return resultDict

def getStatusOfLift(lift,weight,bw):
    liftDict = returnDictFromCSV(bw)
    liftList = liftDict[lift]
    scoreList = [30,45,60,75,87.5,100,110,125]
    try:
        if weight >= int(liftList[7].strip(" kg")) :
            status = "World Class"
            upperBound = ""
            percentage = 0
            score = 125
        elif weight >= int(liftList[6].strip(" kg")) :
            status = "Elite"
            upperBound = "World Class"
            percentage = round(((weight-int(liftList[6].strip(" kg")))/(int(liftList[7].strip(" kg"))-int(liftList[6].strip(" kg"))))*100,2)
            score = scoreList[6] + (percentage*0.01*(scoreList[7]-scoreList[6]))
        elif weight >= int(liftList[5].strip(" kg")) :
            status = "Exceptional"
            upperBound = "Elite"
            percentage = round(((weight-int(liftList[5].strip(" kg")))/(int(liftList[6].strip(" kg"))-int(liftList[5].strip(" kg"))))*100,2)
            score = scoreList[5] + (percentage*0.01*(scoreList[6]-scoreList[5]))
        elif weight >= int(liftList[4].strip(" kg")) :
            status = "Advanced"
            upperBound = "Exceptional"
            percentage = round(((weight-int(liftList[4].strip(" kg")))/(int(liftList[5].strip(" kg"))-int(liftList[4].strip(" kg"))))*100,2)
            score = scoreList[4] + (percentage*0.01*(scoreList[5]-scoreList[4]))
        elif weight >= int(liftList[3].strip(" kg")) :
            status = "Proficient"
            upperBound = "Advanced"
            percentage = round(((weight-int(liftList[3].strip(" kg")))/(int(liftList[4].strip(" kg"))-int(liftList[3].strip(" kg"))))*100,2)
            score = scoreList[3] + (percentage*0.01*(scoreList[4]-scoreList[3]))
        elif weight >= int(liftList[2].strip(" kg")) :
            status = "Intermediate"
            upperBound = "Proficient"
            percentage = round(((weight-int(liftList[2].strip(" kg")))/(int(liftList[3].strip(" kg"))-int(liftList[2].strip(" kg"))))*100,2)
            score = scoreList[2] + (percentage*0.01*(scoreList[3]-scoreList[2]))
        elif weight >= int(liftList[1].strip(" kg")) :
            status = "Novice"
            upperBound = "Intermediate"
            percentage = round(((weight-int(liftList[1].strip(" kg")))/(int(liftList[2].strip(" kg"))-int(liftList[1].strip(" kg"))))*100,2)
            score = scoreList[1] + (percentage*0.01*(scoreList[2]-scoreList[1]))
        elif weight >= int(liftList[0].strip(" kg")) :
            status = "Untrained"
            upperBound = "Novice"
            percentage = round(((weight-int(liftList[0].strip(" kg")))/(int(liftList[1].strip(" kg"))-int(liftList[0].strip(" kg"))))*100,2)
            score = scoreList[0] + (percentage*0.01*(scoreList[1]-scoreList[0]))
        else :
            status = "Subpar"
            upperBound = "Untrained"
            percentage = round(((weight-0)/(int(liftList[0].strip(" kg"))-0))*100,2)
            score = 0 + (percentage*0.01*(scoreList[1]-0))
        
        
        return [status,upperBound,percentage,score]
    except:
        return ["N/A","N/A",0,0]

def getStatusOfLiftBW(lift,weight,bw):
    liftDict = returnDictFromCSV(bw)
    liftList = liftDict[lift]
    scoreList = [30,45,60,75,87.5,100,110,125]
    try:
        if weight >= int(liftList[7].strip(" kg").strip("+")) :
            status = "World Class"
            upperBound = ""
            percentage = 0
            score = 125
        elif weight >= int(liftList[6].strip(" kg").strip("+")) :
            status = "Elite"
            upperBound = "World Class"
            percentage = round(((weight-int(liftList[6].strip(" kg").strip("+")))/(int(liftList[7].strip(" kg").strip("+"))-int(liftList[6].strip(" kg").strip("+"))))*100,2)
            score = scoreList[6] + (percentage*0.01*(scoreList[7]-scoreList[6]))
        elif weight >= int(liftList[5].strip(" kg").strip("+")) :
            status = "Exceptional"
            upperBound = "Elite"
            percentage = round(((weight-int(liftList[5].strip(" kg").strip("+")))/(int(liftList[6].strip(" kg").strip("+"))-int(liftList[5].strip(" kg").strip("+"))))*100,2)
            score = scoreList[5] + (percentage*0.01*(scoreList[6]-scoreList[5]))
        elif weight >= int(liftList[4].strip(" kg").strip("+")) :
            status = "Advanced"
            upperBound = "Exceptional"
            percentage = round(((weight-int(liftList[4].strip(" kg").strip("+")))/(int(liftList[5].strip(" kg").strip("+"))-int(liftList[4].strip(" kg").strip("+"))))*100,2)
            score = scoreList[4] + (percentage*0.01*(scoreList[5]-scoreList[4]))
        elif weight >= int(liftList[3].strip(" kg").strip("+")) :
            status = "Proficient"
            upperBound = "Advanced"
            percentage = round(((weight-int(liftList[3].strip(" kg").strip("+")))/(int(liftList[4].strip(" kg").strip("+"))-int(liftList[3].strip(" kg").strip("+"))))*100,2)
            score = scoreList[3] + (percentage*0.01*(scoreList[4]-scoreList[3]))
        elif weight >= int(liftList[2].strip(" kg").strip("+")) :
            status = "Intermediate"
            upperBound = "Proficient"
            percentage = round(((weight-int(liftList[2].strip(" kg").strip("+")))/(int(liftList[3].strip(" kg").strip("+"))-int(liftList[2].strip(" kg").strip("+"))))*100,2)
            score = scoreList[2] + (percentage*0.01*(scoreList[3]-scoreList[2]))
        elif weight >= int(liftList[1].strip(" kg").strip("+")) :
            status = "Novice"
            upperBound = "Intermediate"
            percentage = round(((weight-int(liftList[1].strip(" kg").strip("+")))/(int(liftList[2].strip(" kg").strip("+"))-int(liftList[1].strip(" kg").strip("+"))))*100,2)
            score = scoreList[1] + (percentage*0.01*(scoreList[2]-scoreList[1]))
        elif weight >= int(liftList[0].strip(" kg").strip("+")) :
            status = "Untrained"
            upperBound = "Novice"
            percentage = round(((weight-int(liftList[0].strip(" kg").strip("+")))/(int(liftList[1].strip(" kg").strip("+"))-int(liftList[0].strip(" kg").strip("+"))))*100,2)
            score = scoreList[0] + (percentage*0.01*(scoreList[1]-scoreList[0]))
        else :
            status = "Subpar"
            upperBound = "Untrained"
            percentage = round(((weight-0)/(int(liftList[0].strip(" kg").strip("+"))-0))*100,2)
            score = 0 + (percentage*0.01*(scoreList[1]-0))

        return [status,upperBound,percentage,score]
    except:
        return ["N/A","N/A",0,0]

if __name__ == '__main__':
    
    #print(oneRepMaxBW(85,8,10))
    #print(findBestLiftOf("FS"))
    #print(findBestLiftBWOf("CU",85))
    #repMaxHistoryOf("BP")
    #getLiftName("SDL")
    #estimatedPLTotal()
    #print(wilksScore(85))
    #print(idFromUser("Andi Fathul"))
    #print(listOfExcercise())
    #returnDictFromCSV(85)
    #getStatusOfLift("Front Squat",107.5,85)
    #getStatusOfLiftBW("Dip",40,85)
    #getStatusOfLift("Bench Press",110,85)
    #getStatusOfLift("Overhead Press",75,85)
    print(findBestLiftOf("BS",1))
    #r = repMaxHistoryOf("BS",1)
    #r.show()
    #plotToImage(r)