import sys
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QDesktopWidget, QLabel, QHBoxLayout, QCalendarWidget, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon, QTextCharFormat, QFont, QColor, QBrush
from numpy import mean
from formula import *
from model import User, Lift


#make non-Clickable object on Qt clickable 
def clickable(widget):
    class Filter(QObject):
        clicked = pyqtSignal()
        def eventFilter(self, obj, event):
            if obj == widget:
                if event.type() == QEvent.MouseButtonRelease:
                    if obj.rect().contains(event.pos()):
                        self.clicked.emit()
                        return True
            return False
    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked

class loginPage(QMainWindow):
    def __init__(self):
        super(loginPage, self).__init__()
        loadUi("Login2.ui", self)

        self.initUI()
        self.initConnection()

        print("Login")

    def initUI(self):
        pixmap = QPixmap("img/LogoAfterColored&Crop2.png")
        self.Logo.setPixmap(pixmap)

    def initConnection(self):
        self.btnLogin.clicked.connect(self.onClickBtnLogin)
        clickable(self.txtSignUp).connect(self.gotoSignUp)
        clickable(self.txtForget).connect(self.gotoChangePsw)

    def onClickBtnLogin(self):
        user = self.txtUsername.text()
        psw = self.txtPassword.text()
        #print(checkLoginValid(user,psw))

        if checkLoginValid(user,psw) == 1:
            self.txtMessage.setText("Success")
            user = User(idFromUser(user))
            user.addSession()
            self.gotoLiftLog() #change later
        elif checkLoginValid(user,psw) == 0:
            self.txtMessage.setText("Username not found")
        else:
            self.txtMessage.setText("Wrong Password")

    def gotoSignUp(self):
        signUp = signUpPage()
        widget.addWidget(signUp)
        widget.setCurrentWidget(signUp)

    def gotoLiftLog(self):
        liftLog = liftLogPage()
        widget.addWidget(liftLog)
        widget.setCurrentWidget(liftLog)

    def gotoChangePsw(self):
        changePsw = changePswPage()
        widget.addWidget(changePsw)
        widget.setCurrentWidget(changePsw)

class changePswPage(QMainWindow):
    def __init__(self):
        super(changePswPage, self).__init__()
        loadUi("changePass.ui", self)

        self.initUI()
        self.initConnection()
        
        print("Change Password")

    def initUI(self):
        pixmap = QPixmap("img/LogoAfterColored&Crop2.png")
        self.Logo.setPixmap(pixmap)

    def initConnection(self):
        self.btnLogin.clicked.connect(self.onClickBtnLogin)
        clickable(self.txtSignUp).connect(self.gotoSignUp)
        clickable(self.txtLogin).connect(self.gotoLogin)

    def onClickBtnLogin(self): #onClickBtnChangePassword
        user = self.txtUsername.text()
        psw = self.txtPassword.text() 
        rePsw = self.txtRPassword.text()
        msg = self.isValid(user,psw,rePsw)[1]
        if self.isValid(user,psw,rePsw)[0] :
            user = User(idFromUser(user))
            user.changePassword(psw)
            self.gotoLogin()
        else:
            self.txtMessage.setText(msg)

    def isValid(self,user,psw,rePsw):
        flag = False
        msg = ""
        if user == "":
            msg = "Please fill username field!"
        elif psw == "":
            msg = "Please fill password field!"
        elif psw != rePsw:
            msg = "Password field doesnt match!"
        elif ifUser(user) == 0:
            msg = "User not found!"
        else:
            flag = True

        return [flag,msg]

    def gotoSignUp(self):
        signUp = signUpPage()
        widget.addWidget(signUp)
        widget.setCurrentWidget(signUp)

    def gotoLogin(self):
        login = loginPage()
        widget.addWidget(login)
        widget.setCurrentWidget(login)

class signUpPage(QMainWindow):
    def __init__(self):
        super(signUpPage, self).__init__()
        loadUi("SignUp2.ui", self)
        
        self.initUI()
        self.initConnection()

        print("SignUp")

    def initUI(self):
        pixmap = QPixmap("img/LogoAfterColored&Crop2.png")
        self.Logo.setPixmap(pixmap)

    def initConnection(self):
        self.btnSignUp.clicked.connect(self.addUser)
        clickable(self.txtLogin).connect(self.gotoLogin)

    def addUser(self):
        fullname = self.txtFullname.text()
        name = self.txtUsername.text()
        email = self.txtEmail.text()
        password = self.txtPassword.text()
        rePassword = self.txtRPassword.text()

        if self.radioMale.isChecked() == True : gender = "Male"
        elif self.radioFemale.isChecked() == True : gender = "Female"
        else: gender = ""

        date = f'{self.spinYear.text()}-{self.spinMonth.text()}-{self.spinDay.text()}'

        weight = self.txtWeight.text()
        height = self.txtHeight.text()
        bodyfat = self.txtBodyFat.text()
        fitExp = self.cmbFitExp.currentIndex()
        activity = self.cmbActivity.currentIndex()
        isValid = self.validSignUp(fullname,name,email,password,rePassword,gender,date,height,weight,bodyfat,fitExp,activity)
        self.txtMessage.setText(isValid[1])
        #print(isValid)
        if isValid[0]: 
            user = User(fullname,name,email,password,gender,date,height,weight,bodyfat,fitExp,activity)
            user.insertUser()
            user.addSession()
            self.gotoLiftLog()

    def validSignUp(self, fullname,name,email,password,rePassword,gender,date,height,weight,bodyfat,fitExp,activity):
        flag = False
        msg = ""
        if fullname == "":
            msg = "Please fill Fullname field!"
        elif name == "":
            msg = "Please fill Username field!"
        elif email == "":
            msg = "Please fill Email field!"
        elif password == "":
            msg = "Please fill Password field!"
        elif password != rePassword:
            msg = "Password field doesnt match!"
        elif gender == "":
            msg = "Choose one of gender field"
        elif len(date) < 8 :
            msg = "Fill the correct Date of Birth"
        elif height == "":
            msg = "Please fill Height field!"
        elif weight == "":
            msg = "Please fill Weight field!"
        elif bodyfat == "":
            msg = "Please fill BodyFat field!"
        elif fitExp < 1:
            msg = "Choose one of Experience field!"
        elif activity < 1:
            msg = "Choose one of Activity field"
        elif ifUser(name) > 0:
            msg = "This user already have an account"
        else:
            flag = True
        return [flag,msg]

    def gotoLogin(self):
        login = loginPage()
        widget.addWidget(login)
        widget.setCurrentWidget(login)

    def gotoLiftLog(self):
        liftLog = liftLogPage()
        widget.addWidget(liftLog)
        widget.setCurrentWidget(liftLog)

class liftLogPage(QMainWindow):
    def __init__(self):
        super(liftLogPage, self).__init__()
        loadUi("LiftLog.ui", self)

        self.initUI()
        self.initNav()
        self.initCalendar()
        self.initConnection()

        self.toggleEdit = 0
        
        print("Lift Log")

    def initUI(self):
        self.cmbExcercise1.clear()
        exc = listOfExcercise()
        self.cmbExcercise1.addItems(exc)
        self.cmbExcercise2.addItems(exc)
        self.cmbExcercise3.addItems(exc)
        self.cmbExcercise4.addItems(exc)
        self.cmbExcercise5.addItems(exc)
        self.cmbExcercise6.addItems(exc)
        self.clearView()

    def initConnection(self):
        self.btnSubmitE1.clicked.connect(self.onClickBtnE1)
        self.btnSubmitE2.clicked.connect(self.onClickBtnE2)
        self.btnSubmitE3.clicked.connect(self.onClickBtnE3)
        self.btnSubmitE4.clicked.connect(self.onClickBtnE4)
        self.btnSubmitE5.clicked.connect(self.onClickBtnE5)
        self.btnSubmitE6.clicked.connect(self.onClickBtnE6)
        self.btnToggle.clicked.connect(self.slideToRight)
        self.btnToggleEdit.clicked.connect(self.onClickToggleEdit)

    def initCalendar(self):
        format1 = QTextCharFormat()
        format2 = QTextCharFormat()
        format1.setBackground(QColor.fromRgb(0,0,255))
        format2.setForeground(QBrush(QColor("Black"),Qt.SolidPattern))
        self.calendarWidget.setMinimumDate(QDate.fromString(returnMinDate(getLastSession()), "yyyy-MM-dd"))
        #self.calendarWidget.setGridVisible(True)
        self.calendarWidget.setFirstDayOfWeek(Qt.Sunday)
        self.calendarWidget.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendarWidget.setHorizontalHeaderFormat(QCalendarWidget.ShortDayNames)
        self.calendarWidget.clicked.connect(self.onClickCalendar)
        #self.calendarWidget.setHeaderTextFormat(format1)
        self.calendarWidget.setWeekdayTextFormat(Qt.Saturday,format2)
        self.calendarWidget.setWeekdayTextFormat(Qt.Sunday,format2)
        for date in self.qtDateFromString():
            #date = QDate(2021,4,1)
            format = QTextCharFormat()
            #format.setFont(QFont('Times',8))
            format.setFontUnderline(True)
            format.setFontWeight(10)
            format.setUnderlineColor(QColor.fromRgb(0,0,0,50))
            format.setBackground(QColor.fromRgb(136,216,199))
            self.calendarWidget.setDateTextFormat(date,format)
            #print(self.qtDateFromString())

    def initNav(self):
        pxm0 = QPixmap("img/menuWhiteColor24Px.png")
        icon0 = QIcon(pxm0)
        self.btnToggle.setIcon(icon0)
        pxm1 = QPixmap("img/homeWhiteColor24Px.png")
        icon1 = QIcon(pxm1)
        self.btnHome.setIcon(icon1)
        pxm2 = QPixmap("img/userWhiteColor24Px.png")
        icon2 = QIcon(pxm2)
        self.btnLiftLog.setIcon(icon2)
        pxm3 = QPixmap("img/settingsWhiteColor24Px.png")
        icon3 = QIcon(pxm3)
        self.btnTDEE.setIcon(icon3)
        self.btnLiftStats.setIcon(icon3)
        self.btnLiftRecord.setIcon(icon3)
        self.btnMuscleStats.setIcon(icon3)
        self.btnStrengthStandard.setIcon(icon3)
        self.btnAccount.setIcon(icon3)
        pxm4 = QPixmap("img/Tulisan JournFit-01.png")
        self.appLogo.setPixmap(pxm4)

        self.btnToggle.setStyleSheet('*{text-align: center}')
        self.btnHome.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftLog.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnTDEE.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftStats.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftRecord.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnMuscleStats.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnStrengthStandard.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnAccount.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')

        self.btnHome.setText("")
        self.btnLiftLog.setText("")
        self.btnTDEE.setText("")
        self.btnLiftStats.setText("")
        self.btnLiftRecord.setText("")
        self.btnMuscleStats.setText("")
        self.btnStrengthStandard.setText("")
        self.btnAccount.setText("")

        #connection
        self.btnTDEE.clicked.connect(self.gotoTDEE)
        self.btnLiftStats.clicked.connect(self.gotoLiftStats)
        self.btnLiftRecord.clicked.connect(self.gotoLiftRecord)
        self.btnStrengthStandard.clicked.connect(self.gotoStrengthStandard)
        self.btnAccount.clicked.connect(self.gotoLogin)

    def slideToRight(self):
        width = self.LeftSideMenu.width()
        if width <= 100 :
            self.btnHome.setText("Home")
            self.btnLiftLog.setText("Lift Log")
            self.btnTDEE.setText("TDEE Stats")
            self.btnLiftStats.setText("Lift Stats")
            self.btnLiftRecord.setText("Lift Record")
            self.btnMuscleStats.setText("Muscle Stats")
            self.btnStrengthStandard.setText("Strength Standard")
            self.btnAccount.setText("Account")
            newWidth = 225
        else:
            self.btnHome.setText("")
            self.btnLiftLog.setText("")
            self.btnTDEE.setText("")
            self.btnLiftStats.setText("")
            self.btnLiftRecord.setText("")
            self.btnMuscleStats.setText("")
            self.btnStrengthStandard.setText("")
            self.btnAccount.setText("")
            newWidth = 50

        self.animation = QPropertyAnimation(self.LeftSideMenu, b"minimumWidth")
        self.animation.setDuration(500)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()

    def qtDateFromString(self):
        dateList = returnDateLogin(getLastSession())
        qtDate = [QDate.fromString(d, "yyyy-MM-dd") for d in dateList]
        return qtDate

    def onClickCalendar(self):
        btnList = [self.btnSubmitE1,self.btnSubmitE2,self.btnSubmitE3,self.btnSubmitE4,self.btnSubmitE5,self.btnSubmitE6]
        date = self.calendarWidget.selectedDate()
        user = User(getLastSession())
        result = user.showRecordOn(f'{date.year()}-{date.month()}-{date.day()}')
        #result = showRecordOn(f'{date.year()}-{date.month()}-{date.day()}',getLastSession())
        self.clearView()
        self.writeToTable(result)
        self.btnToggleEdit.setStyleSheet('QPushButton {background-color: rgb(255, 201, 66);}')
        self.btnToggleEdit.setText("Toggle Edit Mode")
        self.toggleEdit = 0
        for btn in btnList:
            btn.setStyleSheet('QPushButton {background-color: rgb(85, 170, 0);}')
            btn.setText("Submit")
        if QDate.currentDate().daysTo(date) < 0:
            self.disableData()
            self.btnToggleEdit.setEnabled(True)
        else:   
            self.enableData()
            self.btnToggleEdit.setEnabled(False)

        if QDate.currentDate().daysTo(date) == 0 : 
            self.btnToggleEdit.setEnabled(True)

    def onClickToggleEdit(self):
        btnList = [self.btnSubmitE1,self.btnSubmitE2,self.btnSubmitE3,self.btnSubmitE4,self.btnSubmitE5,self.btnSubmitE6]
        if self.toggleEdit % 3 == 0:
            self.btnToggleEdit.setText("Toggle Delete Mode")
            self.btnToggleEdit.setStyleSheet('QPushButton {background-color: rgb(255, 38, 42);}')
            for btn in btnList:
                btn.setStyleSheet('QPushButton {background-color: rgb(255, 201, 66);}')
                btn.setText("Edit")
                self.enableData()
        elif self.toggleEdit % 3 == 1:
            self.btnToggleEdit.setText("Toggle Submit Mode")
            self.btnToggleEdit.setStyleSheet('QPushButton {background-color: rgb(85, 170, 0);}')
            for btn in btnList:
                btn.setStyleSheet('QPushButton {background-color: rgb(255, 38, 42);}')
                btn.setText("Delete")
                self.enableData()
        else:
            self.btnToggleEdit.setText("Toggle Edit Mode")
            self.btnToggleEdit.setStyleSheet('QPushButton {background-color: rgb(255, 201, 66);}')
            for btn in btnList:
                btn.setStyleSheet('QPushButton {background-color: rgb(85, 170, 0);}')
                btn.setText("Submit")
                self.disableData()

        self.toggleEdit += 1
        print(self.toggleEdit)

    def onClickBtnE1(self):
        firstRow = [self.txtWeightE1S1, self.txtWeightE1S2, self.txtWeightE1S3, self.txtWeightE1S4, self.txtWeightE1S5, self.txtWeightE1S6]
        firstSp = [self.spinBoxE1S1,self.spinBoxE1S2,self.spinBoxE1S3,self.spinBoxE1S4,self.spinBoxE1S5,self.spinBoxE1S6]
        text = self.btnSubmitE1.text()
        print(text)
        if text == "Submit":
            try:
                self.submitRow(1,getLastSession())
                if(firstRow[0].text() != " "):
                    self.cmbExcercise1.setEnabled(False)
                    for obj in firstRow + firstSp:
                        obj.setReadOnly(True)
            except: pass
        if text == "Edit":
            if(self.hiddenE1S1.text() == "-"):
                self.submitDateRow(1,getLastSession())
                self.showPopUp("Success insert data on row 1")
            else:
                try:
                    self.editRow(1,getLastSession())
                    self.showPopUp("Success update data on row 1")
                except: pass
        if text == "Delete":
            if(len(self.hiddenE1S1.text()) != 0):
                try:
                    self.deleteRow(1,getLastSession())
                    self.showPopUp("Success delete data on row 1")
                except: pass
    
    def onClickBtnE2(self):
        secondRow = [self.txtWeightE2S1, self.txtWeightE2S2, self.txtWeightE2S3,self.txtWeightE2S4, self.txtWeightE2S5, self.txtWeightE2S6]
        secondSp = [self.spinBoxE2S1,self.spinBoxE2S2,self.spinBoxE2S3,self.spinBoxE2S4,self.spinBoxE2S5,self.spinBoxE2S6]
        text = self.btnSubmitE2.text()
        print(text)
        if text == "Submit":
            try:
                self.submitRow(2,getLastSession())
                if(secondRow[0].text() != " "):
                    self.cmbExcercise2.setEnabled(False)
                    for obj in secondRow + secondSp:
                        obj.setReadOnly(True)
            except: pass
        if text == "Edit":
            if(self.hiddenE2S1.text() == "-"):
                self.submitDateRow(2,getLastSession())
                self.showPopUp("Success insert data on row 2")
            else: 
                try:
                    self.editRow(2,getLastSession())
                    self.showPopUp("Success update data on row 1")
                except: pass
        if text == "Delete":
            if(len(self.hiddenE2S1.text()) != 0):
                try:
                    self.deleteRow(2,getLastSession())
                    self.showPopUp("Success delete data on row 2")
                except: pass

    def onClickBtnE3(self):
        thirdRow = [self.txtWeightE3S1, self.txtWeightE3S2, self.txtWeightE3S3,self.txtWeightE3S4, self.txtWeightE3S5, self.txtWeightE3S6]
        thirdSp = [self.spinBoxE3S1,self.spinBoxE3S2,self.spinBoxE3S3,self.spinBoxE3S4,self.spinBoxE3S5,self.spinBoxE3S6]
        text = self.btnSubmitE3.text()
        print(text)
        if text == "Submit":
            try:
                self.submitRow(3,getLastSession())
                if(thirdRow[0].text() != " "):
                    self.cmbExcercise3.setEnabled(False)
                    for obj in thirdRow + thirdSp:
                        obj.setReadOnly(True)
            except: pass
        if text == "Edit":
            if(self.hiddenE3S1.text() == "-"):
                self.submitDateRow(3,getLastSession())
                self.showPopUp("Success insert data on row 3")
            else: 
                try:
                    self.editRow(3,getLastSession())
                    self.showPopUp("Success update data on row 3")
                except: pass
        if text == "Delete":
            if(len(self.hiddenE3S1.text()) != 0):
                try:
                    self.deleteRow(3,getLastSession())
                    self.showPopUp("Success delete data on row 3")
                except: pass

    def onClickBtnE4(self):
        fourthRow = [self.txtWeightE4S1, self.txtWeightE4S2, self.txtWeightE4S3,self.txtWeightE4S4, self.txtWeightE4S5, self.txtWeightE4S6]
        fourthSp = [self.spinBoxE4S1,self.spinBoxE4S2,self.spinBoxE4S3,self.spinBoxE4S4,self.spinBoxE4S5,self.spinBoxE4S6]
        text = self.btnSubmitE4.text()
        print(text)
        if text == "Submit":
            try:
                self.submitRow(4,getLastSession())
                if(fourthRow[0].text() != " "):
                    self.cmbExcercise4.setEnabled(False)
                    for obj in fourthRow + fourthSp:
                        obj.setReadOnly(True)
            except: pass
        if text == "Edit":
            if(self.hiddenE4S1.text() == "-"):
                self.submitDateRow(4,getLastSession())
                self.showPopUp("Success insert data on row 4")
            else: 
                try:
                    self.editRow(4,getLastSession())
                    self.showPopUp("Success update data on row 4")
                except: pass
        if text == "Delete":
            if(len(self.hiddenE4S1.text()) != 0):
                try:
                    self.deleteRow(4,getLastSession())
                    self.showPopUp("Success delete data on row 4")
                except: pass

    def onClickBtnE5(self):
        fifthRow = [self.txtWeightE5S1, self.txtWeightE5S2, self.txtWeightE5S3,self.txtWeightE5S4, self.txtWeightE5S5, self.txtWeightE5S6]
        fifthSp = [self.spinBoxE5S1,self.spinBoxE5S2,self.spinBoxE5S3,self.spinBoxE5S4,self.spinBoxE5S5,self.spinBoxE5S6]
        text = self.btnSubmitE5.text()
        print(text)
        if text == "Submit":
            try:
                self.submitRow(5,getLastSession())
                if(fifthRow[0].text() != " "):
                    self.cmbExcercise5.setEnabled(False)
                    for obj in fifthRow + fifthSp:
                        obj.setReadOnly(True)
            except: pass
        if text == "Edit":
            if(len(self.hiddenE5S1.text()) == 0):
                self.submitDateRow(5,getLastSession())
                self.showPopUp("Success insert data on row 5")
            else: 
                try:
                    self.editRow(5,getLastSession())
                    self.showPopUp("Success update data on row 5")
                except: pass
        if text == "Delete":
            if(self.hiddenE5S1.text() == "-"):
                try:
                    self.deleteRow(5,getLastSession())
                    self.showPopUp("Success delete data on row 5")
                except: pass
    
    def onClickBtnE6(self):
        sixthRow = [self.txtWeightE6S1, self.txtWeightE6S2, self.txtWeightE6S3,self.txtWeightE6S4, self.txtWeightE6S5, self.txtWeightE6S6]
        sixthSp = [self.spinBoxE6S1,self.spinBoxE6S2,self.spinBoxE6S3,self.spinBoxE6S4,self.spinBoxE6S5,self.spinBoxE6S6]
        text = self.btnSubmitE6.text()
        print(text)
        if text == "Submit":
            try:
                self.submitRow(6,getLastSession())
                if(sixthRow[0].text() != " "):
                    self.cmbExcercise6.setEnabled(False)
                    for obj in sixthRow + sixthSp:
                        obj.setReadOnly(True)
            except: pass
        if text == "Edit":
            if(self.hiddenE6S1.text() == "-"):
                self.submitDateRow(6,getLastSession())
                self.showPopUp("Success insert data on row 6")
            else: 
                try:
                    self.editRow(6,getLastSession())
                    self.showPopUp("Success update data on row 6")
                except: pass
        if text == "Delete":
            if(len(self.hiddenE6S1.text()) != 0):
                try:
                    self.deleteRow(6,getLastSession())
                    self.showPopUp("Success delete data on row 6")
                except: pass

    def showPopUp(self,message):
        msg = QMessageBox()
        msg.setWindowTitle("JournFit")
        msg.setText(message)
        msg.Icon(QMessageBox.Information)
        msg.StandardButton(QMessageBox.Ok|QMessageBox.Open)
        msg.setStyleSheet("QLabel{font-size: 20px; text-align: center;} QPushButton{ width:75px; font-size: 10px; }");
        x = msg.exec_()

    def returnRowData(self, row, user_id):
        row1 = [self.cmbExcercise1, self.txtWeightE1S1, self.spinBoxE1S1, self.hiddenE1S1, self.txtWeightE1S2, self.spinBoxE1S2, self.hiddenE1S2,
                self.txtWeightE1S3, self.spinBoxE1S3, self.hiddenE1S3, self.txtWeightE1S4, self.spinBoxE1S4, self.hiddenE1S4,
                self.txtWeightE1S5, self.spinBoxE1S5, self.hiddenE1S5, self.txtWeightE1S6, self.spinBoxE1S6, self.hiddenE1S6]
        row2 = [self.cmbExcercise2, self.txtWeightE2S1, self.spinBoxE2S1, self.hiddenE2S1, self.txtWeightE2S2, self.spinBoxE2S2, self.hiddenE2S2,
                self.txtWeightE2S3, self.spinBoxE2S3, self.hiddenE2S3, self.txtWeightE2S4, self.spinBoxE2S4, self.hiddenE2S4,
                self.txtWeightE2S5, self.spinBoxE2S5, self.hiddenE2S5, self.txtWeightE2S6, self.spinBoxE2S6, self.hiddenE2S6]
        row3 = [self.cmbExcercise3, self.txtWeightE3S1, self.spinBoxE3S1, self.hiddenE3S1, self.txtWeightE3S2, self.spinBoxE3S2, self.hiddenE3S2,
                self.txtWeightE3S3, self.spinBoxE3S3, self.hiddenE3S3, self.txtWeightE3S4, self.spinBoxE3S4, self.hiddenE3S4, 
                self.txtWeightE3S5, self.spinBoxE3S5, self.hiddenE3S5, self.txtWeightE3S6, self.spinBoxE3S6, self.hiddenE3S6]
        row4 = [self.cmbExcercise4, self.txtWeightE4S1, self.spinBoxE4S1, self.hiddenE4S1, self.txtWeightE4S2, self.spinBoxE4S2, self.hiddenE4S2,
                self.txtWeightE4S3, self.spinBoxE4S3, self.hiddenE4S3, self.txtWeightE4S4, self.spinBoxE4S4, self.hiddenE4S4,
                self.txtWeightE4S5, self.spinBoxE4S5, self.hiddenE4S5, self.txtWeightE4S6, self.spinBoxE4S6, self.hiddenE4S6]
        row5 = [self.cmbExcercise5, self.txtWeightE5S1, self.hiddenE5S1, self.spinBoxE5S1, self.txtWeightE5S2, self.spinBoxE5S2, self.hiddenE5S2,
                self.txtWeightE5S3, self.spinBoxE5S3, self.hiddenE5S3, self.txtWeightE5S4, self.spinBoxE5S4, self.hiddenE5S4, 
                self.txtWeightE5S5, self.spinBoxE5S5, self.hiddenE5S5, self.txtWeightE5S6, self.spinBoxE5S6, self.hiddenE5S6]
        row6 = [self.cmbExcercise6, self.txtWeightE6S1, self.spinBoxE6S1, self.hiddenE6S1, self.txtWeightE6S2, self.spinBoxE6S2, self.hiddenE6S2,
                self.txtWeightE6S3, self.spinBoxE6S3, self.hiddenE6S3, self.txtWeightE6S4, self.spinBoxE6S4, self.hiddenE6S4, 
                self.txtWeightE6S5, self.spinBoxE6S5, self.hiddenE6S5, self.txtWeightE6S6, self.spinBoxE6S6, self.hiddenE6S6]
        rows = [row1,row2,row3,row4,row5,row6]
        rowsTxt = [rows[row-1][0].currentText()] + [r.text() for r in rows[row-1][1:]]
        print(rowsTxt)
        try:
            blankIndex = rowsTxt.index(" ")
            print(blankIndex)
            del rowsTxt[blankIndex:]
        except: pass
        numOfRecords = (len(rowsTxt) - 1)/3
        print(numOfRecords)
        rowMaster = []
        for i in range(1,int(numOfRecords+1)) :
            rowTemp = []
            rowTemp.append(user_id)
            rowTemp.append(fromExcToAbr(rowsTxt[0]))
            rowTemp.append(rowsTxt[(i-1)*3 + 1])
            rowTemp.append(rowsTxt[(i-1)*3 + 2])
            rowTemp.append(row)
            rowTemp.append("") #For media
            rowTemp.append(rowsTxt[i*3])
            rowMaster.append(rowTemp)
        print(rowMaster)
        return rowMaster

    def submitRow(self, row, user_id):
        rowMaster = self.returnRowData(row, user_id)
        for row in rowMaster:
            lift = Lift(row[0], row[1], row[2], row[3], row[4], row[5])
            lift.addLift()
        print(rowMaster)

    def submitDateRow(self, row, user_id):
        rowMaster = self.returnRowData(row, user_id)
        date = self.calendarWidget.selectedDate()
        selDate = f'{date.year()}-{date.month()}-{date.day()}'
        print(selDate)
        for row in rowMaster:
            print(row)
            try:
                lift = Lift(row[0], row[1], selDate, row[2], row[3], row[4], row[5])
                lift.addLift()
            except Exception as ex:
                msg = f'Error : {type(ex).__name__} ,arg = {ex.args}'
                print(msg)
        print(rowMaster)

    def editRow(self, row, user_id):
        rowMaster = self.returnRowData(row, user_id)
        for row in rowMaster:
            try:
                lift = Lift(row[6])
                lift.updateLift(row[1], row[2], row[3], row[4], row[5])
            except Exception as ex:
                msg = f'Error : {type(ex).__name__} ,arg = {ex.args}'
                print(msg)

        date = self.calendarWidget.selectedDate()        
        user = User(getLastSession())
        result = user.showRecordOn(f'{date.year()}-{date.month()}-{date.day()}')
        #result = showRecordOf(f'{date.year()}-{date.month()}-{date.day()}',getLastSession())
        self.clearView()
        self.writeToTable(result)

    def deleteRow(self, row, user_id):
        rowMaster = self.returnRowData(row, user_id)
        for row in rowMaster:
            try:
                lift = Lift(row[6])
                lift.deleteLift()
                #deleteLift(row[6])
                #print(row[6])
            except Exception as ex:
                msg = f'Error : {type(ex).__name__} ,arg = {ex.args}'
                print(msg)
        
        date = self.calendarWidget.selectedDate()
        user = User(getLastSession())
        result = user.showRecordOn(f'{date.year()}-{date.month()}-{date.day()}')        
        #result = showRecordOf(f'{date.year()}-{date.month()}-{date.day()}',getLastSession())
        self.clearView()
        self.writeToTable(result)
        #print(rowMaster)

    def clearView(self):
        cmbExcList = [self.cmbExcercise1,self.cmbExcercise2,self.cmbExcercise3,self.cmbExcercise4,self.cmbExcercise5,self.cmbExcercise6]
        firstRow = [self.txtWeightE1S1, self.txtWeightE1S2, self.txtWeightE1S3, self.txtWeightE1S4, self.txtWeightE1S5, self.txtWeightE1S6]
        secondRow = [self.txtWeightE2S1, self.txtWeightE2S2, self.txtWeightE2S3,self.txtWeightE2S4, self.txtWeightE2S5, self.txtWeightE2S6]
        thirdRow = [self.txtWeightE3S1, self.txtWeightE3S2, self.txtWeightE3S3,self.txtWeightE3S4, self.txtWeightE3S5, self.txtWeightE3S6]
        fourthRow = [self.txtWeightE4S1, self.txtWeightE4S2, self.txtWeightE4S3,self.txtWeightE4S4, self.txtWeightE4S5, self.txtWeightE4S6]
        fifthRow = [self.txtWeightE5S1, self.txtWeightE5S2, self.txtWeightE5S3,self.txtWeightE5S4, self.txtWeightE5S5, self.txtWeightE5S6]
        sixthRow = [self.txtWeightE6S1, self.txtWeightE6S2, self.txtWeightE6S3,self.txtWeightE6S4, self.txtWeightE6S5, self.txtWeightE6S6]
        firstSp = [self.spinBoxE1S1,self.spinBoxE1S2,self.spinBoxE1S3,self.spinBoxE1S4,self.spinBoxE1S5,self.spinBoxE1S6]
        secondSp = [self.spinBoxE2S1,self.spinBoxE2S2,self.spinBoxE2S3,self.spinBoxE2S4,self.spinBoxE2S5,self.spinBoxE2S6]
        thirdSp = [self.spinBoxE3S1,self.spinBoxE3S2,self.spinBoxE3S3,self.spinBoxE3S4,self.spinBoxE3S5,self.spinBoxE3S6]
        fourthSp = [self.spinBoxE4S1,self.spinBoxE4S2,self.spinBoxE4S3,self.spinBoxE4S4,self.spinBoxE4S5,self.spinBoxE4S6]
        fifthSp = [self.spinBoxE5S1,self.spinBoxE5S2,self.spinBoxE5S3,self.spinBoxE5S4,self.spinBoxE5S5,self.spinBoxE5S6]
        sixthSp = [self.spinBoxE6S1,self.spinBoxE6S2,self.spinBoxE6S3,self.spinBoxE6S4,self.spinBoxE6S5,self.spinBoxE6S6]
        firstHidden = [self.hiddenE1S1,self.hiddenE1S2,self.hiddenE1S3,self.hiddenE1S4,self.hiddenE1S5,self.hiddenE1S6]
        secondHidden = [self.hiddenE2S1,self.hiddenE2S2,self.hiddenE2S3,self.hiddenE2S4,self.hiddenE2S5,self.hiddenE2S6]
        thirdHidden = [self.hiddenE3S1,self.hiddenE3S2,self.hiddenE3S3,self.hiddenE3S4,self.hiddenE3S5,self.hiddenE3S6]
        fourthHidden = [self.hiddenE4S1,self.hiddenE4S2,self.hiddenE4S3,self.hiddenE4S4,self.hiddenE4S5,self.hiddenE4S6]
        fifthHidden = [self.hiddenE5S1,self.hiddenE5S2,self.hiddenE5S3,self.hiddenE5S4,self.hiddenE5S5,self.hiddenE5S6]
        sixthHidden = [self.hiddenE6S1,self.hiddenE6S2,self.hiddenE6S3,self.hiddenE6S4,self.hiddenE6S5,self.hiddenE6S6]
        for cmb in cmbExcList:
            cmb.setCurrentIndex(-1)
        for r in firstRow + secondRow + thirdRow + fourthRow + fifthRow + sixthRow:
            r.setText(" ")
        for sp in firstSp + secondSp + thirdSp + fourthSp + fifthSp + sixthSp:
            sp.setValue(0)
        for hd in firstHidden + secondHidden + thirdHidden + fourthHidden + fifthHidden + sixthHidden:
            hd.setText("-")

    def gotoTDEE(self):
        tdee = tdeePage()
        widget.addWidget(tdee)
        widget.setCurrentWidget(tdee)

    def gotoLiftStats(self):
        liftstats = liftStatsPage()
        widget.addWidget(liftstats)
        widget.setCurrentWidget(liftstats)

    def gotoLiftRecord(self):
        liftrecord = liftRecordPage()
        widget.addWidget(liftrecord)
        widget.setCurrentWidget(liftrecord)

    def gotoStrengthStandard(self):
        strengthSt = strengthStandardPage()
        widget.addWidget(strengthSt)
        widget.setCurrentWidget(strengthSt)

    def gotoLogin(self):
        login = loginPage()
        widget.addWidget(login)
        widget.setCurrentWidget(login) 
    
    def writeToTable(self, result):
        cmbExcList = [self.cmbExcercise1,self.cmbExcercise2,self.cmbExcercise3,self.cmbExcercise4,self.cmbExcercise5,self.cmbExcercise6]
        firstRow = [self.txtWeightE1S1, self.txtWeightE1S2, self.txtWeightE1S3, self.txtWeightE1S4, self.txtWeightE1S5, self.txtWeightE1S6]
        secondRow = [self.txtWeightE2S1, self.txtWeightE2S2, self.txtWeightE2S3,self.txtWeightE2S4, self.txtWeightE2S5, self.txtWeightE2S6]
        thirdRow = [self.txtWeightE3S1, self.txtWeightE3S2, self.txtWeightE3S3,self.txtWeightE3S4, self.txtWeightE3S5, self.txtWeightE3S6]
        fourthRow = [self.txtWeightE4S1, self.txtWeightE4S2, self.txtWeightE4S3,self.txtWeightE4S4, self.txtWeightE4S5, self.txtWeightE4S6]
        fifthRow = [self.txtWeightE5S1, self.txtWeightE5S2, self.txtWeightE5S3,self.txtWeightE5S4, self.txtWeightE5S5, self.txtWeightE5S6]
        sixthRow = [self.txtWeightE6S1, self.txtWeightE6S2, self.txtWeightE6S3,self.txtWeightE6S4, self.txtWeightE6S5, self.txtWeightE6S6]
        firstSp = [self.spinBoxE1S1,self.spinBoxE1S2,self.spinBoxE1S3,self.spinBoxE1S4,self.spinBoxE1S5,self.spinBoxE1S6]
        secondSp = [self.spinBoxE2S1,self.spinBoxE2S2,self.spinBoxE2S3,self.spinBoxE2S4,self.spinBoxE2S5,self.spinBoxE2S6]
        thirdSp = [self.spinBoxE3S1,self.spinBoxE3S2,self.spinBoxE3S3,self.spinBoxE3S4,self.spinBoxE3S5,self.spinBoxE3S6]
        fourthSp = [self.spinBoxE4S1,self.spinBoxE4S2,self.spinBoxE4S3,self.spinBoxE4S4,self.spinBoxE4S5,self.spinBoxE4S6]
        fifthSp = [self.spinBoxE5S1,self.spinBoxE5S2,self.spinBoxE5S3,self.spinBoxE5S4,self.spinBoxE5S5,self.spinBoxE5S6]
        sixthSp = [self.spinBoxE6S1,self.spinBoxE6S2,self.spinBoxE6S3,self.spinBoxE6S4,self.spinBoxE6S5,self.spinBoxE6S6]
        firstHidden = [self.hiddenE1S1,self.hiddenE1S2,self.hiddenE1S3,self.hiddenE1S4,self.hiddenE1S5,self.hiddenE1S6]
        secondHidden = [self.hiddenE2S1,self.hiddenE2S2,self.hiddenE2S3,self.hiddenE2S4,self.hiddenE2S5,self.hiddenE2S6]
        thirdHidden = [self.hiddenE3S1,self.hiddenE3S2,self.hiddenE3S3,self.hiddenE3S4,self.hiddenE3S5,self.hiddenE3S6]
        fourthHidden = [self.hiddenE4S1,self.hiddenE4S2,self.hiddenE4S3,self.hiddenE4S4,self.hiddenE4S5,self.hiddenE4S6]
        fifthHidden = [self.hiddenE5S1,self.hiddenE5S2,self.hiddenE5S3,self.hiddenE5S4,self.hiddenE5S5,self.hiddenE5S6]
        sixthHidden = [self.hiddenE6S1,self.hiddenE6S2,self.hiddenE6S3,self.hiddenE6S4,self.hiddenE6S5,self.hiddenE6S6]
        rows = excRowFromDB(result)
        rowsLen = len(rows)
        firstRowLen = int((len(rows[0])-2)/3) if len(rows) > 0 else 0
        secondRowLen = int((len(rows[1])-2)/3) if len(rows) > 1 else 0
        thirdRowLen = int((len(rows[2])-2)/3) if len(rows) > 2 else 0
        fourthRowLen = int((len(rows[3])-2)/3) if len(rows) > 3 else 0
        fifthRowLen = int((len(rows[4])-2)/3) if len(rows) > 4 else 0
        sixthRowLen = int((len(rows[5])-2)/3) if len(rows) > 5 else 0
        print(firstRowLen)
        for i in range(0, rowsLen):
            try:
                cmbExcList[i].setCurrentText(rows[i][1])
            except: continue

        for i in range(0, firstRowLen):
            firstRow[i].setText(str(rows[0][(i+1)*3 - 1]))
            firstSp[i].setValue(rows[0][(i+1)*3])
            firstHidden[i].setText(str(rows[0][(i+1)*3 + 1]))
        for i in range(0, secondRowLen):
            secondRow[i].setText(str(rows[1][(i+1)*3 - 1]))
            secondSp[i].setValue(rows[1][(i+1)*3])
            secondHidden[i].setText(str(rows[1][(i+1)*3 + 1]))
        for i in range(0, thirdRowLen):
            thirdRow[i].setText(str(rows[2][(i+1)*3 - 1]))
            thirdSp[i].setValue(rows[2][(i+1)*3])
            thirdHidden[i].setText(str(rows[2][(i+1)*3 + 1]))
        for i in range(0, fourthRowLen):
            fourthRow[i].setText(str(rows[3][(i+1)*3 - 1]))
            fourthSp[i].setValue(rows[3][(i+1)*3])
            fourthHidden[i].setText(str(rows[3][(i+1)*3 + 1]))
        for i in range(0, fifthRowLen):
            fifthRow[i].setText(str(rows[4][(i+1)*3 - 1]))
            fifthSp[i].setValue(rows[4][(i+1)*3])
            fifthHidden[i].setText(str(rows[4][(i+1)*3 + 1]))
        for i in range(0, sixthRowLen):
            sixthRow[i].setText(str(rows[5][(i+1)*3 - 1]))
            sixthSp[i].setValue(rows[5][(i+1)*3])
            sixthHidden[i].setText(str(rows[5][(i+1)*3 + 1]))
        for hd in firstHidden + secondHidden + thirdHidden + fourthHidden + fifthHidden + sixthHidden:
            hd.setVisible(False)
        print(rows)

    def disableData(self):
        cmbExcList = [self.cmbExcercise1,self.cmbExcercise2,self.cmbExcercise3,self.cmbExcercise4,self.cmbExcercise5,self.cmbExcercise6]
        firstRow = [self.txtWeightE1S1, self.txtWeightE1S2, self.txtWeightE1S3, self.txtWeightE1S4, self.txtWeightE1S5, self.txtWeightE1S6]
        secondRow = [self.txtWeightE2S1, self.txtWeightE2S2, self.txtWeightE2S3,self.txtWeightE2S4, self.txtWeightE2S5, self.txtWeightE2S6]
        thirdRow = [self.txtWeightE3S1, self.txtWeightE3S2, self.txtWeightE3S3,self.txtWeightE3S4, self.txtWeightE3S5, self.txtWeightE3S6]
        fourthRow = [self.txtWeightE4S1, self.txtWeightE4S2, self.txtWeightE4S3,self.txtWeightE4S4, self.txtWeightE4S5, self.txtWeightE4S6]
        fifthRow = [self.txtWeightE5S1, self.txtWeightE5S2, self.txtWeightE5S3,self.txtWeightE5S4, self.txtWeightE5S5, self.txtWeightE5S6]
        sixthRow = [self.txtWeightE6S1, self.txtWeightE6S2, self.txtWeightE6S3,self.txtWeightE6S4, self.txtWeightE6S5, self.txtWeightE6S6]
        firstSp = [self.spinBoxE1S1,self.spinBoxE1S2,self.spinBoxE1S3,self.spinBoxE1S4,self.spinBoxE1S5,self.spinBoxE1S6]
        secondSp = [self.spinBoxE2S1,self.spinBoxE2S2,self.spinBoxE2S3,self.spinBoxE2S4,self.spinBoxE2S5,self.spinBoxE2S6]
        thirdSp = [self.spinBoxE3S1,self.spinBoxE3S2,self.spinBoxE3S3,self.spinBoxE3S4,self.spinBoxE3S5,self.spinBoxE3S6]
        fourthSp = [self.spinBoxE4S1,self.spinBoxE4S2,self.spinBoxE4S3,self.spinBoxE4S4,self.spinBoxE4S5,self.spinBoxE4S6]
        fifthSp = [self.spinBoxE5S1,self.spinBoxE5S2,self.spinBoxE5S3,self.spinBoxE5S4,self.spinBoxE5S5,self.spinBoxE5S6]
        sixthSp = [self.spinBoxE6S1,self.spinBoxE6S2,self.spinBoxE6S3,self.spinBoxE6S4,self.spinBoxE6S5,self.spinBoxE6S6]
        btnList = [self.btnSubmitE1,self.btnSubmitE2,self.btnSubmitE3,self.btnSubmitE4,self.btnSubmitE5,self.btnSubmitE6]

        for cmb in cmbExcList:
            cmb.setEnabled(False)
        for r in firstRow + secondRow + thirdRow + fourthRow + fifthRow + sixthRow:
            r.setReadOnly(True)
        for sp in firstSp + secondSp + thirdSp + fourthSp + fifthSp + sixthSp:
            sp.setReadOnly(True)
        for btn in btnList:
            btn.setEnabled(False)

    def enableData(self):
        cmbExcList = [self.cmbExcercise1,self.cmbExcercise2,self.cmbExcercise3,self.cmbExcercise4,self.cmbExcercise5,self.cmbExcercise6]
        firstRow = [self.txtWeightE1S1, self.txtWeightE1S2, self.txtWeightE1S3, self.txtWeightE1S4, self.txtWeightE1S5, self.txtWeightE1S6]
        secondRow = [self.txtWeightE2S1, self.txtWeightE2S2, self.txtWeightE2S3,self.txtWeightE2S4, self.txtWeightE2S5, self.txtWeightE2S6]
        thirdRow = [self.txtWeightE3S1, self.txtWeightE3S2, self.txtWeightE3S3,self.txtWeightE3S4, self.txtWeightE3S5, self.txtWeightE3S6]
        fourthRow = [self.txtWeightE4S1, self.txtWeightE4S2, self.txtWeightE4S3,self.txtWeightE4S4, self.txtWeightE4S5, self.txtWeightE4S6]
        fifthRow = [self.txtWeightE5S1, self.txtWeightE5S2, self.txtWeightE5S3,self.txtWeightE5S4, self.txtWeightE5S5, self.txtWeightE5S6]
        sixthRow = [self.txtWeightE6S1, self.txtWeightE6S2, self.txtWeightE6S3,self.txtWeightE6S4, self.txtWeightE6S5, self.txtWeightE6S6]
        firstSp = [self.spinBoxE1S1,self.spinBoxE1S2,self.spinBoxE1S3,self.spinBoxE1S4,self.spinBoxE1S5,self.spinBoxE1S6]
        secondSp = [self.spinBoxE2S1,self.spinBoxE2S2,self.spinBoxE2S3,self.spinBoxE2S4,self.spinBoxE2S5,self.spinBoxE2S6]
        thirdSp = [self.spinBoxE3S1,self.spinBoxE3S2,self.spinBoxE3S3,self.spinBoxE3S4,self.spinBoxE3S5,self.spinBoxE3S6]
        fourthSp = [self.spinBoxE4S1,self.spinBoxE4S2,self.spinBoxE4S3,self.spinBoxE4S4,self.spinBoxE4S5,self.spinBoxE4S6]
        fifthSp = [self.spinBoxE5S1,self.spinBoxE5S2,self.spinBoxE5S3,self.spinBoxE5S4,self.spinBoxE5S5,self.spinBoxE5S6]
        sixthSp = [self.spinBoxE6S1,self.spinBoxE6S2,self.spinBoxE6S3,self.spinBoxE6S4,self.spinBoxE6S5,self.spinBoxE6S6]
        btnList = [self.btnSubmitE1,self.btnSubmitE2,self.btnSubmitE3,self.btnSubmitE4,self.btnSubmitE5,self.btnSubmitE6]

        for cmb in cmbExcList:
            cmb.setEnabled(True)
        for r in firstRow + secondRow + thirdRow + fourthRow + fifthRow + sixthRow:
            r.setReadOnly(False)
        for sp in firstSp + secondSp + thirdSp + fourthSp + fifthSp + sixthSp:
            sp.setReadOnly(False)
        for btn in btnList:
            btn.setEnabled(True)

class tdeePage(QMainWindow):
    def __init__(self):
        super(tdeePage, self).__init__()
        loadUi("TDEE.ui", self)
        
        self.initNav()
        self.initConnection()
        self.initHeader()
        self.initTDEE()

    def initConnection(self):
        self.btnToggle.clicked.connect(self.slideToRight)
        self.btnRecalculate.clicked.connect(self.initTDEE)

    def initHeader(self):
        user = User(getLastSession())
        self.labelInitial.setText(f'{user.name}, {user.age}y/o {user.gender} who is ')
        self.txtHeight.setText(str(user.height))
        self.txtWeight.setText(str(user.weight))
        self.cmbActivity.setCurrentIndex(user.activity-1)
        self.txtBF.setText(str(user.bodyfat))

    def initTDEE(self):
        user = User(getLastSession())
        tdee = tdeeCalc(user.gender, int(self.txtHeight.text()), int(self.txtWeight.text()), 
            int(self.txtBF.text()), int(self.cmbActivity.currentIndex())+1)
        self.txtCalpday.setText(str(tdee[0]))
        self.txtCalpwk.setText(str(tdee[0]*7))

        text = f"Based on your stats, the best estimate for your maintenance calories is {str(tdee[0])} calories per day based on the Katch-McArdle Formula, which is widely known to be the most accurate when body fat is provided. The table below shows the difference if you were to have selected a different activity level."
        self.tdeeExp.setText(text)

        txtTdee = [self.txtBMRCal, self.txtSedCal, self.txtLexCal, self.txtMexCal, self.txtHexCal, self.txtAthCal]
        txtText = [self.txt1, self.txt2, self.txt3, self.txt4, self.txt5, self.txt6]
        txtCpd = [self.cpd1, self.cpd2, self.cpd3, self.cpd4, self.cpd5, self.cpd6]
        bmiLabel = [self.bmi1, self.bmi2, self.bmi3, self.bmi4, self.bmi5, self.bmi6, self.bmi7, self.bmi8]
        font = QFont()
        font.setBold(False)
        for idx,txt in enumerate(txtTdee):
            txt.setText(str(tdee[1][idx]))
            txt.setFont(font)
        for txt in txtText + txtCpd:
            txt.setFont(font)
        for bmi in bmiLabel:
            bmi.setFont(font)

        font.setBold(True)
        txtTdee[self.cmbActivity.currentIndex()+1].setFont(font)
        txtText[self.cmbActivity.currentIndex()+1].setFont(font)
        txtCpd[self.cmbActivity.currentIndex()+1].setFont(font)

        self.widgetMacros.setStyleSheet('QTabBar{background-color: rgb(3, 114, 188); color: rgb(0, 0, 0)}')

        maintenance = [self.txtMainModP, self.txtMainModF, self.txtMainModC, self.txtMainLowP, self.txtMainLowF, self.txtMainLowC, 
                       self.txtMainHigP, self.txtMainHigF, self.txtMainHigC]
        cutting = [self.txtCutModP, self.txtCutModF, self.txtCutModC, self.txtCutLowP, self.txtCutLowF, self.txtCutLowC, 
                   self.txtCutHigP, self.txtCutHigF, self.txtCutHigC]
        bulking = [self.txtBulkModP, self.txtBulkModF, self.txtBulkModC, self.txtBulkLowP, self.txtBulkLowF, self.txtBulkLowC, 
                   self.txtBulkHigP, self.txtBulkHigF, self.txtBulkHigC]

        maint = macrosMaintenance(int(self.txtCalpday.text()))
        cut = macrosCutting(int(self.txtCalpday.text()))
        bulk = macrosBulking(int(self.txtCalpday.text()))
        maintList = maint[0] + maint[1] + maint[2]
        cutList = cut[0] + cut[1] + cut[2]
        bulkList = bulk[0] + bulk[1] + bulk[2]

        for idx,m in enumerate(maintenance):
            m.setText(f'{maintList[idx]}g')

        for idx,c in enumerate(cutting):
            c.setText(f'{cutList[idx]}g')

        for idx,b in enumerate(bulking):
            b.setText(f'{bulkList[idx]}g')

        #bmi

        bmi = bmiScore(int(self.txtWeight.text()),int(self.txtHeight.text()))
        self.txtBMI.setText(f'BMI Score : {bmi[0]}')
        text = f"Your BMI is {bmi[0]}, which means you are classified as {bmi[1]}. <b>The BMI Index did not account the bodyfat so you maybe muscular enough to be listed as overweight...</b>"
        self.txtBMILabel.setText(text)

        if bmi[0] <= 18.5 :
            self.bmi1.setFont(font)
            self.bmi5.setFont(font)
        elif bmi[0] <= 24.99 :
            self.bmi2.setFont(font)
            self.bmi6.setFont(font)
        elif bmi[0] <= 29.99 :
            self.bmi3.setFont(font)
            self.bmi7.setFont(font)
        else :
            self.bmi4.setFont(font)
            self.bmi8.setFont(font)

        #ideal bodyweight

        mmp = maxMP(int(self.txtHeight.text()))
        self.txtMMP5.setText(f'{mmp[0]} kg at 5.5% bodyfat')
        self.txtMMP8.setText(f'{mmp[1]} kg at 8% bodyfat')
        self.txtMMP10.setText(f'{mmp[2]} kg at 10% bodyfat')
        self.txtMMP12.setText(f'{mmp[3]} kg at 12% bodyfat')
        self.txtMMP15.setText(f'{mmp[4]} kg at 15% bodyfat')

        pw = powerliftingWeight(int(self.txtHeight.text()), user.gender)
        self.txtPL1.setText(f'{pw[0]} (Most Federation)')
        self.txtPL2.setText(f'{pw[1]} (IPF)')

        oly = olyWeight(int(self.txtHeight.text()), user.gender)
        self.txtOLY.setText(f'{oly[0]} (Olympic Standard)')
        self.txtIWF.setText(f'{oly[1]} (IWF)')

        bb = bodybuildingWeight(int(self.txtHeight.text()))
        if(user.gender == "Male"):
            self.txtCBD.setText(f'{bb[0]} (Classic Bodybuilding Division)')
            self.txtCPH.setText(f'{bb[1]} (Classic Physic Division)')
        else:
            self.txtCBD.setText(f'{bb[0]-20} (Classic Bodybuilding Division)')
            self.txtCPH.setText(f'{bb[1]-20} (Classic Physic Division)')

    def initNav(self):
        pxm0 = QPixmap("img/menuWhiteColor24Px.png")
        icon0 = QIcon(pxm0)
        self.btnToggle.setIcon(icon0)
        pxm1 = QPixmap("img/homeWhiteColor24Px.png")
        icon1 = QIcon(pxm1)
        self.btnHome.setIcon(icon1)
        pxm2 = QPixmap("img/userWhiteColor24Px.png")
        icon2 = QIcon(pxm2)
        self.btnLiftLog.setIcon(icon2)
        pxm3 = QPixmap("img/settingsWhiteColor24Px.png")
        icon3 = QIcon(pxm3)
        self.btnTDEE.setIcon(icon3)
        self.btnLiftStats.setIcon(icon3)
        self.btnLiftRecord.setIcon(icon3)
        self.btnMuscleStats.setIcon(icon3)
        self.btnStrengthStandard.setIcon(icon3)
        self.btnAccount.setIcon(icon3)
        pxm4 = QPixmap("img/Tulisan JournFit-01.png")
        self.appLogo.setPixmap(pxm4)

        self.btnToggle.setStyleSheet('*{text-align: center}')
        self.btnHome.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftLog.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnTDEE.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftStats.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftRecord.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnMuscleStats.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnStrengthStandard.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnAccount.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')

        self.btnHome.setText("")
        self.btnLiftLog.setText("")
        self.btnTDEE.setText("")
        self.btnLiftStats.setText("")
        self.btnLiftRecord.setText("")
        self.btnMuscleStats.setText("")
        self.btnStrengthStandard.setText("")
        self.btnAccount.setText("")

        #connection
        self.btnLiftLog.clicked.connect(self.gotoLiftLog)
        self.btnLiftStats.clicked.connect(self.gotoLiftStats)
        self.btnLiftRecord.clicked.connect(self.gotoLiftRecord)
        self.btnStrengthStandard.clicked.connect(self.gotoStrengthStandard)

    def slideToRight(self):
        width = self.LeftSideMenu.width()
        if width <= 100 :
            self.btnHome.setText("Home")
            self.btnLiftLog.setText("Lift Log")
            self.btnTDEE.setText("TDEE Stats")
            self.btnLiftStats.setText("Lift Stats")
            self.btnLiftRecord.setText("Lift Record")
            self.btnMuscleStats.setText("Muscle Stats")
            self.btnStrengthStandard.setText("Strength Standard")
            self.btnAccount.setText("Account")
            newWidth = 225
        else:
            self.btnHome.setText("")
            self.btnLiftLog.setText("")
            self.btnTDEE.setText("")
            self.btnLiftStats.setText("")
            self.btnLiftRecord.setText("")
            self.btnMuscleStats.setText("")
            self.btnStrengthStandard.setText("")
            self.btnAccount.setText("")
            newWidth = 50

        self.animation = QPropertyAnimation(self.LeftSideMenu, b"minimumWidth")
        self.animation.setDuration(500)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()

    def gotoLiftLog(self):
        liftLog = liftLogPage()
        widget.addWidget(liftLog)
        widget.setCurrentWidget(liftLog)

    def gotoLiftStats(self):
        liftstats = liftStatsPage()
        widget.addWidget(liftstats)
        widget.setCurrentWidget(liftstats)

    def gotoLiftRecord(self):
        liftrecord = liftRecordPage()
        widget.addWidget(liftrecord)
        widget.setCurrentWidget(liftrecord)

    def gotoStrengthStandard(self):
        strengthSt = strengthStandardPage()
        widget.addWidget(strengthSt)
        widget.setCurrentWidget(strengthSt)

class liftStatsPage(QMainWindow):
    def __init__(self):
        super(liftStatsPage, self).__init__()
        loadUi("liftStats.ui", self)

        self.btnToggle.clicked.connect(self.slideToRight)
        self.initNav()
        self.writeData()
        #clear view and try except the func

        print("Lift Stats")

    def initNav(self):
        pxm0 = QPixmap("img/menuWhiteColor24Px.png")
        icon0 = QIcon(pxm0)
        self.btnToggle.setIcon(icon0)
        pxm1 = QPixmap("img/homeWhiteColor24Px.png")
        icon1 = QIcon(pxm1)
        self.btnHome.setIcon(icon1)
        pxm2 = QPixmap("img/userWhiteColor24Px.png")
        icon2 = QIcon(pxm2)
        self.btnLiftLog.setIcon(icon2)
        pxm3 = QPixmap("img/settingsWhiteColor24Px.png")
        icon3 = QIcon(pxm3)
        self.btnTDEE.setIcon(icon3)
        self.btnLiftStats.setIcon(icon3)
        self.btnLiftRecord.setIcon(icon3)
        self.btnMuscleStats.setIcon(icon3)
        self.btnStrengthStandard.setIcon(icon3)
        self.btnAccount.setIcon(icon3)
        pxm4 = QPixmap("img/Tulisan JournFit-01.png")
        self.appLogo.setPixmap(pxm4)

        self.btnToggle.setStyleSheet('*{text-align: center}')
        self.btnHome.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftLog.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnTDEE.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftStats.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftRecord.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnMuscleStats.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnStrengthStandard.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnAccount.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')

        self.btnHome.setText("")
        self.btnLiftLog.setText("")
        self.btnTDEE.setText("")
        self.btnLiftStats.setText("")
        self.btnLiftRecord.setText("")
        self.btnMuscleStats.setText("")
        self.btnStrengthStandard.setText("")
        self.btnAccount.setText("")

        #connection
        self.btnLiftLog.clicked.connect(self.gotoLiftLog)
        self.btnTDEE.clicked.connect(self.gotoTDEE)
        self.btnLiftRecord.clicked.connect(self.gotoLiftRecord)
        self.btnStrengthStandard.clicked.connect(self.gotoStrengthStandard)

    def writeData(self): #update the func query later
        user = User(getLastSession())
        id = user.userID
        bsERP = findBestLiftOf("BS",id)
        fsERP = findBestLiftOf("FS",id) 
        dlERP = findBestLiftOf("DL",id) 
        sdlERP = findBestLiftOf("SDL",id) 
        bpERP = findBestLiftOf("BP",id) 
        ibpERP = findBestLiftOf("IBP",id) 
        dipERP = findBestLiftBWOf("DIP",user.weight,id) 
        ohpERP = findBestLiftOf("OHP",id) 
        cuERP = findBestLiftBWOf("CU",user.weight,id) 
        puERP = findBestLiftBWOf("PU",user.weight,id) 
        prERP = findBestLiftOf("PR",id)
        plTotal = bsERP[1] + dlERP[1] + bpERP[1]
        wilks = wilksFactor(user.weight)
        try:
            wilkScore = wilks[0]*plTotal #change later to gender based
        except:
            wilkScore = ""

        bs = getStatusOfLift("Back Squat",bsERP[1],user.weight)
        fs = getStatusOfLift("Front Squat",fsERP[1],user.weight)
        dl = getStatusOfLift("Deadlift",dlERP[1],user.weight)
        sdl = getStatusOfLift("Sumo Deadlift",sdlERP[1],user.weight)
        bp = getStatusOfLift("Bench Press",bpERP[1],user.weight)
        ibp = getStatusOfLift("Incline Bench Press",ibpERP[1],user.weight)
        dip = getStatusOfLiftBW("Dip",dipERP[1],user.weight)
        ohp = getStatusOfLift("Overhead Press",ohpERP[1],user.weight)
        cu = getStatusOfLiftBW("Chin-up",cuERP[1],user.weight)
        pu = getStatusOfLiftBW("Pull-up",puERP[1],user.weight)
        pr = getStatusOfLift("Pendlay Row",prERP[1],user.weight)

        self.txtBS_ERP.setText(str(bsERP[1]) + " kg")
        self.txtFS_ERP.setText(str(fsERP[1]) + " kg")
        self.txtDL_ERP.setText(str(dlERP[1]) + " kg")
        self.txtSDL_ERP.setText(str(sdlERP[1]) + " kg")
        self.txtBP_ERP.setText(str(bpERP[1]) + " kg")
        self.txtIBP_ERP.setText(str(ibpERP[1]) + " kg")
        self.txtDIP_ERP.setText("+" + str(dipERP[1]) + " kg")
        self.txtOHP_ERP.setText(str(ohpERP[1]) + " kg")
        self.txtCU_ERP.setText("+" + str(cuERP[1]) + " kg")
        self.txtPU_ERP.setText("+" + str(puERP[1]) + " kg")
        self.txtPR_ERP.setText(str(prERP[1]) + " kg")

        self.txtBS_Score.setText(str(round(bs[3],1)))
        self.txtFS_Score.setText(str(round(fs[3],1)))
        self.txtDL_Score.setText(str(round(dl[3],1)))
        self.txtSDL_Score.setText(str(round(sdl[3],1)))
        self.txtBP_Score.setText(str(round(bp[3],1)))
        self.txtIBP_Score.setText(str(round(ibp[3],1)))
        self.txtDIP_Score.setText(str(round(dip[3],1)))
        self.txtOHP_Score.setText(str(round(ohp[3],1)))
        self.txtCU_Score.setText(str(round(cu[3],1)))
        self.txtPU_Score.setText(str(round(pu[3],1)))
        self.txtPR_Score.setText(str(round(pr[3],1)))

        self.txtBS_Status.setText(str(bs[0]))
        self.txtFS_Status.setText(str(fs[0]))
        self.txtDL_Status.setText(str(dl[0]))
        self.txtSDL_Status.setText(str(sdl[0]))
        self.txtBP_Status.setText(str(bp[0]))
        self.txtIBP_Status.setText(str(ibp[0]))
        self.txtDIP_Status.setText(str(dip[0]))
        self.txtOHP_Status.setText(str(ohp[0]))
        self.txtCU_Status.setText(str(cu[0]))
        self.txtPU_Status.setText(str(pu[0]))
        self.txtPR_Status.setText(str(pr[0]))

        self.txtBS_Current.setText(str(bs[0]))
        self.txtFS_Current.setText(str(fs[0]))
        self.txtDL_Current.setText(str(dl[0]))
        self.txtSDL_Current.setText(str(sdl[0]))
        self.txtBP_Current.setText(str(bp[0]))
        self.txtIBP_Current.setText(str(ibp[0]))
        self.txtDIP_Current.setText(str(dip[0]))
        self.txtOHP_Current.setText(str(ohp[0]))
        self.txtCU_Current.setText(str(cu[0]))
        self.txtPU_Current.setText(str(pu[0]))
        self.txtPR_Current.setText(str(pr[0]))

        self.txtBS_Next.setText(str(bs[1]))
        self.txtFS_Next.setText(str(fs[1]))
        self.txtDL_Next.setText(str(dl[1]))
        self.txtSDL_Next.setText(str(sdl[1]))
        self.txtBP_Next.setText(str(bp[1]))
        self.txtIBP_Next.setText(str(ibp[1]))
        self.txtDIP_Next.setText(str(dip[1]))
        self.txtOHP_Next.setText(str(ohp[1]))
        self.txtCU_Next.setText(str(cu[1]))
        self.txtPU_Next.setText(str(pu[1]))
        self.txtPR_Next.setText(str(pr[1]))

        self.progressBarBS.setValue(bs[2])
        self.progressBarFS.setValue(fs[2])
        self.progressBarDL.setValue(dl[2])
        self.progressBarSDL.setValue(sdl[2])
        self.progressBarBP.setValue(bp[2])
        self.progressBarIBP.setValue(ibp[2])
        self.progressBarDIP.setValue(dip[2])
        self.progressBarOHP.setValue(ohp[2])
        self.progressBarCU.setValue(cu[2])
        self.progressBarPU.setValue(pu[2])
        self.progressBarPR.setValue(pr[2])

        if bs[3] == 0 or fs[3] == 0 :
            squatScore = bs[3] + fs[3]
        else :
            squatScore = mean([bs[3],fs[3]])

        horprsScore = mean([bp[3],ibp[3],dip[3]])
        verprsScore = ohp[3]
        floorplScore = mean([dl[3],sdl[3]])
        purowScore = mean([cu[3],pu[3],pr[3]])

        squatStatus = self.getStatus(squatScore)
        floorplStatus = self.getStatus(floorplScore)
        horprsStatus = self.getStatus(horprsScore)
        verprsStatus = self.getStatus(verprsScore)
        purowStatus = self.getStatus(purowScore)

        self.txtSquatScore.setText(str(round(squatScore,1)))
        self.txtHorizontalPressScore.setText(str(round(horprsScore,1)))
        self.txtVerticalPressScore.setText(str(round(verprsScore,1)))
        self.txtFloorPullScore.setText(str(round(floorplScore,1)))
        self.txtPullUpRowScore.setText(str(round(purowScore,1)))

        self.txtSquatStatus.setText(squatStatus)
        self.txtHorizontalPressStatus.setText(horprsStatus)
        self.txtVerticalPressStatus.setText(verprsStatus)
        self.txtFloorPullStatus.setText(floorplStatus)
        self.txtPullUpRowStatus.setText(purowStatus)

        overallScore = mean([squatScore,horprsScore,verprsScore,floorplScore,purowScore])
        overallStatus = self.getStatus(overallScore)

        self.txtOverallScore.setText(str(round(overallScore,1)))
        self.txtOverallStatus.setText(overallStatus)
        try:
            self.txtEstimatedPLTotal.setText(str(round(plTotal,1)))
        except:
            self.txtEstimatedPLTotal.setText(str(0))
        try:
            self.txtWilksScore.setText(str(int(wilkScore)))
        except:
            self.txtWilksScore.setText(str(0))

        #scoreList = [bsERP[1],fsERP[1],dlERP[1],sdlERP[1],bpERP[1],ibpERP[1],dipERP[1],ohpERP[1],cuERP[1],puERP[1],prERP[1]]
        scoreList = [bs[3],fs[3],dl[3],sdl[3],bp[3],ibp[3],dip[3],ohp[3],cu[3],pu[3],pr[3]]
        excList = ["Back Squat", "Front Squat", "Deadlift", "Sumo Deadlift", "Bench Press", "Incline Bench Press", "Dip", 
                   "Overhead Press", "Chin Up", "Pull Up", "Pendlay Row"]

        minIndex = min(range(len(scoreList)), key=scoreList.__getitem__)
        maxIndex = max(range(len(scoreList)), key=scoreList.__getitem__)
        minExc = excList[minIndex]
        maxExc = excList[maxIndex]

        if overallScore != 0:
            self.txtStrongestLift.setText(maxExc)
            self.txtWeakestLift.setText(minExc)
        else:
            self.txtStrongestLift.setText("")
            self.txtWeakestLift.setText("")


    def getStatus(self,score):
        if score >= 125 : return "World Class"
        elif score >= 110 : return "Elite"
        elif score >= 100 : return "Exceptional"
        elif score >= 87.5 : return "Advanced"
        elif score >= 75 : return "Proficient"
        elif score >= 60 : return "Intermediate"
        elif score >= 45 : return "Novice"
        elif score >= 30 : return "Untrained"
        return "Subpar"

    def slideToRight(self):
        width = self.LeftSideMenu.width()
        if width <= 100 :
            self.btnHome.setText("Home")
            self.btnLiftLog.setText("Lift Log")
            self.btnTDEE.setText("TDEE Stats")
            self.btnLiftStats.setText("Lift Stats")
            self.btnLiftRecord.setText("Lift Record")
            self.btnMuscleStats.setText("Muscle Stats")
            self.btnStrengthStandard.setText("Strength Standard")
            self.btnAccount.setText("Account")
            newWidth = 225
        else:
            self.btnHome.setText("")
            self.btnLiftLog.setText("")
            self.btnTDEE.setText("")
            self.btnLiftStats.setText("")
            self.btnLiftRecord.setText("")
            self.btnMuscleStats.setText("")
            self.btnStrengthStandard.setText("")
            self.btnAccount.setText("")
            newWidth = 50

        self.animation = QPropertyAnimation(self.LeftSideMenu, b"minimumWidth")
        self.animation.setDuration(500)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()

    def gotoLiftLog(self):
        liftLog = liftLogPage()
        widget.addWidget(liftLog)
        widget.setCurrentWidget(liftLog)

    def gotoTDEE(self):
        tdee = tdeePage()
        widget.addWidget(tdee)
        widget.setCurrentWidget(tdee)

    def gotoLiftRecord(self):
        liftrecord = liftRecordPage()
        widget.addWidget(liftrecord)
        widget.setCurrentWidget(liftrecord)

    def gotoStrengthStandard(self):
        strengthSt = strengthStandardPage()
        widget.addWidget(strengthSt)
        widget.setCurrentWidget(strengthSt)

class liftRecordPage(QMainWindow):
    def __init__(self):
        super(liftRecordPage, self).__init__()
        loadUi("liftRecord.ui", self)
        self.btnToggle.clicked.connect(self.slideToRight)
        self.initNav()
        self.writeData()

    def initNav(self):
        pxm0 = QPixmap("img/menuWhiteColor24Px.png")
        icon0 = QIcon(pxm0)
        self.btnToggle.setIcon(icon0)
        pxm1 = QPixmap("img/homeWhiteColor24Px.png")
        icon1 = QIcon(pxm1)
        self.btnHome.setIcon(icon1)
        pxm2 = QPixmap("img/userWhiteColor24Px.png")
        icon2 = QIcon(pxm2)
        self.btnLiftLog.setIcon(icon2)
        pxm3 = QPixmap("img/settingsWhiteColor24Px.png")
        icon3 = QIcon(pxm3)
        self.btnTDEE.setIcon(icon3)
        self.btnLiftStats.setIcon(icon3)
        self.btnLiftRecord.setIcon(icon3)
        self.btnMuscleStats.setIcon(icon3)
        self.btnStrengthStandard.setIcon(icon3)
        self.btnAccount.setIcon(icon3)
        pxm4 = QPixmap("img/Tulisan JournFit-01.png")
        self.appLogo.setPixmap(pxm4)

        self.btnToggle.setStyleSheet('*{text-align: center}')
        self.btnHome.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftLog.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnTDEE.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftStats.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftRecord.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnMuscleStats.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnStrengthStandard.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnAccount.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')

        self.btnHome.setText("")
        self.btnLiftLog.setText("")
        self.btnTDEE.setText("")
        self.btnLiftStats.setText("")
        self.btnLiftRecord.setText("")
        self.btnMuscleStats.setText("")
        self.btnStrengthStandard.setText("")
        self.btnAccount.setText("")

        #connection
        self.btnLiftLog.clicked.connect(self.gotoLiftLog)
        self.btnTDEE.clicked.connect(self.gotoTDEE)
        self.btnLiftStats.clicked.connect(self.gotoLiftStats)
        self.btnStrengthStandard.clicked.connect(self.gotoStrengthStandard)

    def writeData(self):
        user = User(getLastSession())
        id = user.userID
        bsERP = findBestLiftOf("BS",id)
        fsERP = findBestLiftOf("FS",id) 
        dlERP = findBestLiftOf("DL",id) 
        sdlERP = findBestLiftOf("SDL",id) 
        bpERP = findBestLiftOf("BP",id) 
        ibpERP = findBestLiftOf("IBP",id) 
        ohpERP = findBestLiftOf("OHP",id) 

        bs = getStatusOfLift("Back Squat",bsERP[1],user.weight)
        fs = getStatusOfLift("Front Squat",fsERP[1],user.weight)
        dl = getStatusOfLift("Deadlift",dlERP[1],user.weight)
        sdl = getStatusOfLift("Sumo Deadlift",sdlERP[1],user.weight)
        bp = getStatusOfLift("Bench Press",bpERP[1],user.weight)
        ibp = getStatusOfLift("Incline Bench Press",ibpERP[1],user.weight)
        ohp = getStatusOfLift("Overhead Press",ohpERP[1],user.weight)

        self.txtBS_Status.setText(str(bs[0]))
        self.txtFS_Status.setText(str(fs[0]))
        self.txtDL_Status.setText(str(dl[0]))
        self.txtSDL_Status.setText(str(sdl[0]))
        self.txtBP_Status.setText(str(bp[0]))
        self.txtIBP_Status.setText(str(ibp[0]))
        self.txtOHP_Status.setText(str(ohp[0]))

        self.txtBS_ERP.setText(str(bsERP[1]) + " kg")
        self.txtFS_ERP.setText(str(fsERP[1]) + " kg")
        self.txtDL_ERP.setText(str(dlERP[1]) + " kg")
        self.txtSDL_ERP.setText(str(sdlERP[1]) + " kg")
        self.txtBP_ERP.setText(str(bpERP[1]) + " kg")
        self.txtIBP_ERP.setText(str(ibpERP[1]) + " kg")
        self.txtOHP_ERP.setText(str(ohpERP[1]) + " kg")

        try: 
            self.txtBS_WR.setText(f'{int(bsERP[2])} x {bsERP[3]}')
            self.txtBS_Date.setText(bsERP[0].strftime('%Y-%m-%d'))
            self.txtBS_Days.setText(f'{QDate.fromString(bsERP[0].strftime("%Y-%m-%d"), "yyyy-MM-dd").daysTo(QDate.currentDate())} days ago')
        except:
            self.txtBS_WR.setText(f'{bsERP[2]} x {bsERP[3]}')
            self.txtBS_Date.setText(bsERP[0])
            self.txtBS_Days.setText(bsERP[0])
        try:
            self.txtFS_WR.setText(f'{int(fsERP[2])} x {fsERP[3]}')
            self.txtFS_Date.setText(fsERP[0].strftime('%Y-%m-%d'))
            self.txtFS_Days.setText(f'{QDate.fromString(fsERP[0].strftime("%Y-%m-%d"), "yyyy-MM-dd").daysTo(QDate.currentDate())} days ago')
        except:
            self.txtFS_WR.setText(f'{fsERP[2]} x {fsERP[3]}')
            self.txtFS_Date.setText(fsERP[0])
            self.txtFS_Days.setText(fsERP[0])
        try:
            self.txtDL_WR.setText(f'{int(dlERP[2])} x {dlERP[3]}')
            self.txtDL_Date.setText(dlERP[0].strftime('%Y-%m-%d'))
            self.txtDL_Days.setText(f'{QDate.fromString(dlERP[0].strftime("%Y-%m-%d"), "yyyy-MM-dd").daysTo(QDate.currentDate())} days ago')
        except:
            self.txtDL_WR.setText(f'{dlERP[2]} x {dlERP[3]}')
            self.txtDL_Date.setText(dlERP[0])
            self.txtDL_Days.setText(dlERP[0])
        try:
            self.txtSDL_WR.setText(f'{int(sdlERP[2])} x {sdlERP[3]}')
            self.txtSDL_Date.setText(sdlERP[0].strftime('%Y-%m-%d'))
            self.txtSDL_Days.setText(f'{QDate.fromString(sdlERP[0].strftime("%Y-%m-%d"), "yyyy-MM-dd").daysTo(QDate.currentDate())} days ago')
        except:
            self.txtSDL_WR.setText(f'{sdlERP[2]} x {sdlERP[3]}')
            self.txtSDL_Date.setText(sdlERP[0])
            self.txtSDL_Days.setText(sdlERP[0])
        try:
            self.txtBP_WR.setText(f'{int(bpERP[2])} x {bpERP[3]}')
            self.txtBP_Date.setText(bpERP[0].strftime('%Y-%m-%d'))
            self.txtBP_Days.setText(f'{QDate.fromString(bpERP[0].strftime("%Y-%m-%d"), "yyyy-MM-dd").daysTo(QDate.currentDate())} days ago')
        except:
            self.txtBP_WR.setText(f'{bpERP[2]} x {bpERP[3]}')
            self.txtBP_Date.setText(bpERP[0])
            self.txtBP_Days.setText(bpERP[0])
        try:
            self.txtIBP_WR.setText(f'{int(ibpERP[2])} x {ibpERP[3]}')
            self.txtIBP_Date.setText(ibpERP[0].strftime('%Y-%m-%d'))
            self.txtIBP_Days.setText(f'{QDate.fromString(ibpERP[0].strftime("%Y-%m-%d"), "yyyy-MM-dd").daysTo(QDate.currentDate())} days ago')
        except:
            self.txtIBP_WR.setText(f'{ibpERP[2]} x {ibpERP[3]}')
            self.txtIBP_Date.setText(ibpERP[0])
            self.txtIBP_Days.setText(ibpERP[0])
        try:
            self.txtOHP_WR.setText(f'{int(ohpERP[2])} x {ohpERP[3]}')
            self.txtOHP_Date.setText(ohpERP[0].strftime('%Y-%m-%d'))
            self.txtOHP_Days.setText(f'{QDate.fromString(ohpERP[0].strftime("%Y-%m-%d"), "yyyy-MM-dd").daysTo(QDate.currentDate())} days ago')
        except:
            self.txtOHP_WR.setText(f'{ohpERP[2]} x {ohpERP[3]}')
            self.txtOHP_Date.setText(ohpERP[0])
            self.txtOHP_Days.setText(ohpERP[0])

    def slideToRight(self):
        width = self.LeftSideMenu.width()
        if width <= 100 :
            self.btnHome.setText("Home")
            self.btnLiftLog.setText("Lift Log")
            self.btnTDEE.setText("TDEE Stats")
            self.btnLiftStats.setText("Lift Stats")
            self.btnLiftRecord.setText("Lift Record")
            self.btnMuscleStats.setText("Muscle Stats")
            self.btnStrengthStandard.setText("Strength Standard")
            self.btnAccount.setText("Account")
            newWidth = 225
        else:
            self.btnHome.setText("")
            self.btnLiftLog.setText("")
            self.btnTDEE.setText("")
            self.btnLiftStats.setText("")
            self.btnLiftRecord.setText("")
            self.btnMuscleStats.setText("")
            self.btnStrengthStandard.setText("")
            self.btnAccount.setText("")
            newWidth = 50

        self.animation = QPropertyAnimation(self.LeftSideMenu, b"minimumWidth")
        self.animation.setDuration(500)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()

    def gotoLiftLog(self):
        liftLog = liftLogPage()
        widget.addWidget(liftLog)
        widget.setCurrentWidget(liftLog)

    def gotoTDEE(self):
        tdee = tdeePage()
        widget.addWidget(tdee)
        widget.setCurrentWidget(tdee)

    def gotoLiftStats(self):
        liftstats = liftStatsPage()
        widget.addWidget(liftstats)
        widget.setCurrentWidget(liftstats)

    def gotoStrengthStandard(self):
        strengthSt = strengthStandardPage()
        widget.addWidget(strengthSt)
        widget.setCurrentWidget(strengthSt)

class strengthStandardPage(QMainWindow):
    def __init__(self):
        super(strengthStandardPage, self).__init__()
        loadUi("strengthStandard.ui", self)
        self.btnToggle.clicked.connect(self.slideToRight)
        self.initNav()

    def initNav(self):
        pxm0 = QPixmap("img/menuWhiteColor24Px.png")
        icon0 = QIcon(pxm0)
        self.btnToggle.setIcon(icon0)
        pxm1 = QPixmap("img/homeWhiteColor24Px.png")
        icon1 = QIcon(pxm1)
        self.btnHome.setIcon(icon1)
        pxm2 = QPixmap("img/userWhiteColor24Px.png")
        icon2 = QIcon(pxm2)
        self.btnLiftLog.setIcon(icon2)
        pxm3 = QPixmap("img/settingsWhiteColor24Px.png")
        icon3 = QIcon(pxm3)
        self.btnTDEE.setIcon(icon3)
        self.btnLiftStats.setIcon(icon3)
        self.btnLiftRecord.setIcon(icon3)
        self.btnMuscleStats.setIcon(icon3)
        self.btnStrengthStandard.setIcon(icon3)
        self.btnAccount.setIcon(icon3)
        pxm4 = QPixmap("img/Tulisan JournFit-01.png")
        self.appLogo.setPixmap(pxm4)

        self.btnToggle.setStyleSheet('*{text-align: center}')
        self.btnHome.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftLog.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnTDEE.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftStats.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftRecord.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnMuscleStats.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnStrengthStandard.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnAccount.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')

        self.btnHome.setText("")
        self.btnLiftLog.setText("")
        self.btnTDEE.setText("")
        self.btnLiftStats.setText("")
        self.btnLiftRecord.setText("")
        self.btnMuscleStats.setText("")
        self.btnStrengthStandard.setText("")
        self.btnAccount.setText("")

        #connection
        self.btnLiftLog.clicked.connect(self.gotoLiftLog)
        self.btnTDEE.clicked.connect(self.gotoTDEE)
        self.btnLiftStats.clicked.connect(self.gotoLiftStats)
        self.btnLiftRecord.clicked.connect(self.gotoLiftRecord)

    def slideToRight(self):
        width = self.LeftSideMenu.width()
        if width <= 100 :
            self.btnHome.setText("Home")
            self.btnLiftLog.setText("Lift Log")
            self.btnTDEE.setText("TDEE Stats")
            self.btnLiftStats.setText("Lift Stats")
            self.btnLiftRecord.setText("Lift Record")
            self.btnMuscleStats.setText("Muscle Stats")
            self.btnStrengthStandard.setText("Strength Standard")
            self.btnAccount.setText("Account")
            newWidth = 225
        else:
            self.btnHome.setText("")
            self.btnLiftLog.setText("")
            self.btnTDEE.setText("")
            self.btnLiftStats.setText("")
            self.btnLiftRecord.setText("")
            self.btnMuscleStats.setText("")
            self.btnStrengthStandard.setText("")
            self.btnAccount.setText("")
            newWidth = 50

        self.animation = QPropertyAnimation(self.LeftSideMenu, b"minimumWidth")
        self.animation.setDuration(500)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()

    def gotoLiftLog(self):
        liftLog = liftLogPage()
        widget.addWidget(liftLog)
        widget.setCurrentWidget(liftLog)

    def gotoTDEE(self):
        tdee = tdeePage()
        widget.addWidget(tdee)
        widget.setCurrentWidget(tdee)

    def gotoLiftStats(self):
        liftstats = liftStatsPage()
        widget.addWidget(liftstats)
        widget.setCurrentWidget(liftstats)

    def gotoLiftRecord(self):
        liftrecord = liftRecordPage()
        widget.addWidget(liftrecord)
        widget.setCurrentWidget(liftrecord)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    screen1 = loginPage()
    screen2 = signUpPage()
    screen3 = liftLogPage()
    widget.addWidget(screen1)
    widget.addWidget(screen2)
    widget.addWidget(screen3)
    widget.show()

    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")