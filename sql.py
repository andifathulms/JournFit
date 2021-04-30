from datetime import datetime
import mysql.connector

def querySQL(query, record):
    try:
        #open connection
        connection = mysql.connector.connect(host = "localhost",
                                             database = "journfit",
                                             user = "root",
                                             password = "")
        cursor = connection.cursor()
        cursor.execute(query, record)
        connection.commit()
        print("Finish execute query")
    except mysql.connector.Error as error:
        print(f"Failed to execute : {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed")

def fetchOneQuerySQL(query,record):
    try:
        #open connection
        connection = mysql.connector.connect(host = "localhost",
                                             database = "journfit",
                                             user = "root",
                                             password = "")
        cursor = connection.cursor(buffered=True)
        cursor.execute(query, record)
        connection.commit()
        data = cursor.fetchone()
        print("Finish execute query")
        return data
    except mysql.connector.Error as error:
        print(f"Failed to execute : {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed")


def fetchAllQuerySQL(query,record):
    try:
        #open connection
        connection = mysql.connector.connect(host = "localhost",
                                             database = "journfit",
                                             user = "root",
                                             password = "")
        cursor = connection.cursor(buffered=True)
        cursor.execute(query, record)
        connection.commit()
        data = cursor.fetchall()
        print("Finish execute query")
        return data
    except mysql.connector.Error as error:
        print(f"Failed to execute : {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed")



def insertUser(fullname, name, email, password, gender, datebirth, height, weight, bodyfat, experience,activityLevel):
    #Add to user table
    query = """
            INSERT INTO user(dateCreated, fullname, name, email, password, gender, datebirth, height, weight, bodyfat, experience,activityLevel)
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
    now = datetime.now()
    date = now.strftime('%Y-%m-%d %H:%M:%S')
    record = (date,fullname, name, email, password, gender, datebirth, height, weight, bodyfat, experience, activityLevel)
    querySQL(query,record)
    
    #Add to weightchanges table
    user_id = ifUser(name)
    query = """
            INSERT INTO weightchanges(user_id, dateCreated, weight, bodyfat) 
            VALUES
            (%s, %s, %s, %s)
            """
    record = (user_id, date, weight, bodyfat)
    querySQL(query,record)

def deleteUser(id):
    query = "DELETE FROM user WHERE user_id = %s"
    record = (id,)
    querySQL(query,record)

def idFromUser(user):
    query = "SELECT user_id FROM user WHERE name = %s"
    record = (user,)
    result = fetchOneQuerySQL(query,record)
    return result[0]

def addSession(user):
    query = "INSERT INTO session(user,dateLogin) VALUES(%s,%s)"
    now = datetime.now()
    dateLogin = now.strftime('%Y-%m-%d %H:%M:%S')
    record = (user,dateLogin)
    querySQL(query,record)

def getLastSession():
    query = "SELECT MAX(id) FROM session"
    record = ""
    user = fetchOneQuerySQL(query,record)

    query = """
            SELECT user FROM session 
            WHERE id = %s
            """
    record = (user[0],)
    result = fetchOneQuerySQL(query,record)
    return result[0]

def addWeightChanges(user_id, weight, bodyfat):
    #Add to weightchanges table
    query = """
            INSERT INTO weightchanges(user_id, dateCreated, weight, bodyfat) 
            VALUES
            (%s, %s, %s, %s)
            """

    now = datetime.now()
    date = now.strftime('%Y-%m-%d %H:%M:%S')
    record = (user_id, date, weight, bodyfat)
    querySQL(query,record)

    #Update weight at user table
    query = "UPDATE user SET weight = %s, bodyfat = %s WHERE user_id = %s"
    record = (weight, bodyfat, user_id)
    querySQL(query,record)


def addLift(user_id, exercise, weights, reps, row, media):
    query = """
            INSERT INTO lift(user_id, exercise, dateCreated, weights, reps, row, media) 
            VALUES
            (%s, %s, %s, %s, %s, %s, %s)
            """

    now = datetime.now()
    date = now.strftime('%Y-%m-%d %H:%M:%S')
    record = (user_id, exercise, date, weights, reps, row, media)
    querySQL(query,record)

def updateLift(id, exercise, weights, reps, row, media):
    query = """
            UPDATE lift SET exercise = %s, weights = %s, reps = %s, media = %s
            WHERE id = %s
            """
    record = (exercise,weights,reps,media,id)
    print(f'Update id-{id}')
    querySQL(query,record)

def changePassword(user,psw):
    query = " UPDATE user SET password = %s WHERE name = %s"
    record = (psw, user)
    querySQL(query,record)

def addLiftWithDate(user_id, exercise, date, weights, reps, row, media):
    query = """
            INSERT INTO lift(user_id, exercise, dateCreated, weights, reps, row, media) 
            VALUES
            (%s, %s, %s, %s, %s, %s, %s)
            """
    record = (user_id, exercise, date, weights, reps, row, media)
    print(date)
    querySQL(query,record)

def addLiftWithDateCSV(excList): #For input my data from csv only
    user_id = excList[0]
    exercise = excList[1]
    date = excList[2]
    weights = excList[3]
    reps = excList[4]
    #rpe = excList[5]
    row = excList[6]
    media = excList[7]
    query = """
            INSERT INTO lift(user_id, exercise, dateCreated, weights, reps, row, media) 
            VALUES
            (%s, %s, %s, %s, %s, %s, %s)
            """
    record = (user_id, exercise, date, weights, reps, row, media)
    querySQL(query,record)

def deleteLift(id):
    query = "DELETE FROM lift WHERE id = %s"
    record = (id,)
    querySQL(query,record)
    print(f'Delete id-{id}')

def getLiftName(lift):
    query = "SELECT name FROM excercise WHERE abbreviation = %s"
    record = (lift,)
    result = fetchOneQuerySQL(query,record)
    return result[0]

def checkLoginValid(username,password):
    query = "SELECT password FROM user WHERE name = %s"
    record = (username,)
    result = fetchOneQuerySQL(query,record)
    
    if result == None:
        return 0
    elif result[0] != password:
        return -1
    else:
        return 1

def ifUser(username):
    query = "SELECT user_id FROM user WHERE name = %s"
    record = (username,)
    result = fetchOneQuerySQL(query,record)
    if result == None:
        return 0
    else:
        return result[0]

def listOfExcercise():
    query = "SELECT name FROM excercise ORDER BY type DESC, name"
    record = ""
    result = list(fetchAllQuerySQL(query,record))
    exc = [r[0] for r in result]
    #exc.append(" ")
    return exc

def showRecordOf(date, user_id):
    query = """
            SELECT name,weights,reps,row,id 
            FROM lift LEFT JOIN excercise
            ON lift.exercise = excercise.abbreviation
            WHERE dateCreated = %s AND user_id = %s
            """
    record = (date,user_id)
    result = list(fetchAllQuerySQL(query,record))
    return result

def returnDateLogin(user_id):
    query = "SELECT DISTINCT dateCreated FROM lift WHERE user_id = %s"
    record = (user_id,)
    result = list(fetchAllQuerySQL(query,record))
    date = [d[0] for d in result]
    dateString = [dt.strftime("%Y-%m-%d") for dt in date]
    return dateString

def excRowFromDB(result): #Retrieve query from SQL then make it list of App ready
    compList = []
    for i in range(0,7):
        row = [data for data in result if data[3] == i+1]
        #print(row)
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
            #print(msg)
            continue
    print(compList)    
    return compList

def fromExcToAbr(exc):
    query = "SELECT abbreviation FROM excercise WHERE name = %s"
    record = (exc,)
    result = fetchOneQuerySQL(query,record)
    #print(result[0])
    return result[0]

def returnMinDate(user):
    query = "SELECT MIN(dateCreated) FROM lift WHERE user_id = %s"
    record = (user,)
    result = fetchOneQuerySQL(query,record)
    #print(result[0])
    try:
        return result[0].strftime("%Y-%m-%d")
    except:
        return datetime.now().strftime('%Y-%m-%d')

if __name__ == '__main__':
    #getLiftName("BS")
    #print(checkLoginValid("Andi Fathul", "12345678"))
    #print(ifUser("Nanda"))
    #print(listOfExcercise())
    #print(showRecordOf("2021-04-05",1))
    #result = showRecordOf("2021-04-05",1)
    #print(returnDateLogin(1))
    #excRowFromDB(result)
    #fromExcToAbr("Back Squat")
    #print(returnMinDate(1))
    print(getLastSession())
    #print(datetime.now().strftime('%Y-%m-%d'))