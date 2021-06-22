from datetime import datetime
import mysql.connector

class Connection():
    def __init__(self, query, record):
        self.query = query
        self.record = record

    def querySQL(self):
        try:
            #open connection
            connection = mysql.connector.connect(host = "localhost",
                                                 database = "journfit",
                                                 user = "root",
                                                 password = "")
            cursor = connection.cursor()
            cursor.execute(self.query, self.record)
            connection.commit()
            print("Finish execute query")
        except mysql.connector.Error as error:
            print(f"Failed to execute : {error}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("Connection closed")

    def fetchAllQuerySQL(self):
        try:
            #open connection
            connection = mysql.connector.connect(host = "localhost",
                                                 database = "journfit",
                                                 user = "root",
                                                 password = "")
            cursor = connection.cursor(buffered=True)
            cursor.execute(self.query, self.record)
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

    def fetchOneQuerySQL(self):
        try:
            #open connection
            connection = mysql.connector.connect(host = "localhost",
                                                 database = "journfit",
                                                 user = "root",
                                                 password = "")
            cursor = connection.cursor(buffered=True)
            cursor.execute(self.query, self.record)
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

class User():
    def __init__(self, *args):
        if len(args) == 1 :
            user = self.getUser(args[0])[0]
            self.userID = user[0]
            self.fullname = user[2] 
            self.name = user[3]
            self.email = user[4]
            self.password = user[5]
            self.gender = user[6]
            self.dateOfBirth = user[7]
            self.height = user[8]
            self.weight = user[9]
            self.bodyfat = user[10]
            self.experience = user[11]
            self.activity = user[12]
            self.image = user[13]
            self.age = self.calculateAge()
            self.type = 0
            #print(user)
        else :
            self.fullname = args[0] 
            self.name = args[1]
            self.email = args[2]
            self.password = args[3]
            self.gender = args[4]
            dob = args[5]
            self.dateOfBirth = datetime.strptime(dob, '%Y-%m-%d')
            self.height = args[6]
            self.weight = args[7]
            self.bodyfat = args[8]
            self.experience = args[9]
            self.activity = args[10]
            self.age = self.calculateAge()
            self.type = 1
        
    def getUser(self, id):
        query = "SELECT * FROM user WHERE user_id = %s"
        record = (id,)
        con = Connection(query,record)
        result = con.fetchAllQuerySQL()
        return result

    def insertUser(self):
        if self.type == 1:
            query = """
                    INSERT INTO user(dateCreated, fullname, name, email, password, gender, datebirth, height, weight, bodyfat, experience,activityLevel)
                    VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
            now = datetime.now()
            date = now.strftime('%Y-%m-%d %H:%M:%S')
            record = (date,self.fullname, self.name, self.email, self.password, self.gender, self.dateOfBirth, 
                self.height, self.weight, self.bodyfat, self.experience, self.activity)
            con = Connection(query,record)
            con.querySQL()
            
            #Add to weightchanges table
            user_id = self.getID()
            query = """
                    INSERT INTO weightchanges(user_id, dateCreated, weight, bodyfat) 
                    VALUES
                    (%s, %s, %s, %s)
                    """
            record = (user_id, date, self.weight, self.bodyfat)
            con = Connection(query,record)
            con.querySQL()

    def insertImage(self, image):
        query = " UPDATE user SET image = %s WHERE user_id = %s "
        record = (image,self.userID)
        con = Connection(query,record)
        con.querySQL()

    def getID(self):
        query = "SELECT user_id FROM user WHERE name = %s"
        record = (self.name,)
        con = Connection(query,record)
        result = con.fetchOneQuerySQL()
        self.userID = result[0]
        return result[0]

    def changePassword(self, psw):
        query = " UPDATE user SET password = %s WHERE user_id = %s"
        record = (psw, self.userID)
        con = Connection(query,record)
        con.querySQL()

        now = datetime.now()
        date = now.strftime('%Y-%m-%d %H:%M:%S')
        query = """
                INSERT INTO passwordchanges(user_id,oldPassword,newPassword,dateChange)
                VALUES
                (%s, %s, %s, %s)
                """
        record = (self.userID, self.password, psw, date)
        con = Connection(query,record)
        con.querySQL()

    def updateWeight(self, weight):
        query = " UPDATE user SET weight = %s WHERE user_id = %s"
        record = (weight, self.userID)
        con = Connection(query,record)
        con.querySQL()
        self.addToWeightChanges(weight)

    def updateBodyfat(self, bf):
        query = " UPDATE user SET bodyfat = %s WHERE user_id = %s"
        record = (bf, self.userID)
        con = Connection(query,record)
        con.querySQL()

    def addToWeightChanges(self, weight):
        query = """
                INSERT INTO weightchanges(user_id, dateCreated, weight, bodyfat) 
                VALUES
                (%s, %s, %s, %s)
                """

        now = datetime.now()
        date = now.strftime('%Y-%m-%d %H:%M:%S')
        record = (self.userID, date, weight, self.bodyfat)
        con = Connection(query,record)
        con.querySQL()

    def updateUser(self, fullname, name, email, dobDay, dobMonth, dobYear, weight, height, bf, exp, activity):
        query = """
                UPDATE user 
                SET Fullname = %s, name = %s, email = %s, dateBirth = %s, weight = %s, height = %s,bodyfat = %s,experience = %s, activityLevel = %s
                WHERE user_id = %s
                """
        record = (fullname,name,email,f'{dobYear}-{dobMonth}-{dobDay}',weight,height,bf,exp,activity,self.userID)
        con = Connection(query,record)
        con.querySQL()
        self.addToWeightChanges(weight)

    def calculateAge(self):
        today = datetime.now()
        born = self.dateOfBirth
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    def addSession(self):
        query = "INSERT INTO session(user,dateLogin) VALUES(%s,%s)"
        now = datetime.now()
        dateLogin = now.strftime('%Y-%m-%d %H:%M:%S')
        record = (self.userID,dateLogin)
        con = Connection(query,record)
        con.querySQL()

    def showRecordOn(self, date):
        query = """
                SELECT name,weights,reps,row,id 
                FROM lift LEFT JOIN excercise
                ON lift.exercise = excercise.abbreviation
                WHERE dateCreated = %s AND user_id = %s
                """
        record = (date,self.userID)
        con = Connection(query,record)
        #result = list(fetchAllQuerySQL(query,record))
        result = con.fetchAllQuerySQL()
        return result

    def showPlanOn(self, date):
        query = """
                SELECT name,weights,reps,row,id 
                FROM plan LEFT JOIN excercise
                ON plan.exercise = excercise.abbreviation
                WHERE dateCreated = %s AND user_id = %s
                """
        record = (date,self.userID)
        con = Connection(query,record)
        #result = list(fetchAllQuerySQL(query,record))
        result = con.fetchAllQuerySQL()
        return result

class Lift():
    def __init__(self, *args):
        if len(args) == 1 :
            lift = self.getLift(args[0])[0]
            self.liftID = lift[0]
            self.userID = lift[1]
            self.exercise = lift[2]
            self.dateCreated = lift[3]
            self.weights = lift[4]
            self.reps = lift[5]
            self.row = lift[6]
            self.media = lift[7]
        elif len(args) == 6 :
            self.userID = args[0]
            self.exercise = args[1]
            self.weights = args[2]
            self.reps = args[3]
            self.row = args[4]
            self.media = args[5]
            self.dateCreated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(666)
        elif len(args) == 7 :
            self.userID = args[0]
            self.exercise = args[1]
            self.dateCreated = args[2]
            self.weights = args[3]
            self.reps = args[4]
            self.row = args[5]
            self.media = args[6]
            print(777)

    def getLift(self, id):
        query = "SELECT * FROM lift WHERE id = %s"
        record = (id,)
        con = Connection(query,record)
        result = con.fetchAllQuerySQL()
        return result

    def addLift(self):
        try:
            query = """
                    INSERT INTO lift(user_id, exercise, dateCreated, weights, reps, row, media) 
                    VALUES
                    (%s, %s, %s, %s, %s, %s, %s)
                    """

            record = (self.userID, self.exercise, self.dateCreated, self.weights, self.reps, self.row, self.media)
            con = Connection(query,record)
            con.querySQL()
        except Exception as ex:
            msg = f'Error : {type(ex).__name__} ,arg = {ex.args}'
            print(msg)

    def insertMedia(self, media):
        query = " UPDATE lift SET media = %s WHERE id = %s "
        record = (media,self.liftID)
        con = Connection(query,record)
        con.querySQL()

    def updateLift(self, exercise, weights, reps, row, media):
        query = """
                UPDATE lift SET exercise = %s, weights = %s, reps = %s, media = %s
                WHERE id = %s
                """
        record = (exercise,weights,reps,media,self.liftID)
        print(f'Update id- {self.liftID}')
        con = Connection(query,record)
        con.querySQL()

    def deleteLift(self):
        query = "DELETE FROM lift WHERE id = %s"
        record = (self.liftID,)
        print(f'Delete id-{self.liftID}')
        con = Connection(query,record)
        con.querySQL()

class Plan(Lift):
    def __init__(self, *args):
        if len(args) == 1 :
            lift = self.getPlan(args[0])[0]
            self.liftID = lift[0]
            self.userID = lift[1]
            self.exercise = lift[2]
            self.dateCreated = lift[3]
            self.weights = lift[4]
            self.reps = lift[5]
            self.row = lift[6]
            self.media = lift[7]
        else:
            super(Plan, self).__init__(*args)
        

    def getPlan(self, id):
        query = "SELECT * FROM plan WHERE id = %s"
        record = (id,)
        con = Connection(query,record)
        result = con.fetchAllQuerySQL()
        return result

    def addPlan(self):
        try:
            query = """
                    INSERT INTO plan(user_id, exercise, dateCreated, weights, reps, row, media) 
                    VALUES
                    (%s, %s, %s, %s, %s, %s, %s)
                    """

            record = (self.userID, self.exercise, self.dateCreated, self.weights, self.reps, self.row, self.media)
            con = Connection(query,record)
            con.querySQL()
        except Exception as ex:
            msg = f'Error : {type(ex).__name__} ,arg = {ex.args}'
            print(msg)

    def updatePlan(self, exercise, weights, reps, row, media):
        query = """
                UPDATE plan SET exercise = %s, weights = %s, reps = %s, media = %s
                WHERE id = %s
                """
        record = (exercise,weights,reps,media,self.liftID)
        print(f'Update id- {self.liftID}')
        con = Connection(query,record)
        con.querySQL()

    def deletePlan(self):
        query = "DELETE FROM plan WHERE id = %s"
        record = (self.liftID,)
        print(f'Delete id-{self.liftID}')
        con = Connection(query,record)
        con.querySQL()

if __name__ == '__main__':
    #u1 = User(1)
    #u2 = User("Fikri","Fikri","123","123","Male","1999-01-01","180","85","20","1","1")
    #print(u1.age)
    #print(u2.age)
    #print(u1.getUser(1))
    #u1.changePassword("12345")
    #l = Lift(10)
    #p = Plan(1,"BP","2021-05-16",100,4,1,"")
    #print(p.weights)
    l = Lift(2740)
    print(l.getLift(2740))
    #print(l.weights)
