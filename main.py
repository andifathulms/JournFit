import sys
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QDesktopWidget, QLabel, QHBoxLayout, QCalendarWidget, QMessageBox
from sql import *
from PyQt5.QtGui import QPixmap, QIcon, QTextCharFormat, QFont, QColor

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
        self.btnLogin.clicked.connect(self.onClickBtnLogin)
        clickable(self.txtSignUp).connect(self.gotoSignUp)
        clickable(self.txtForget).connect(self.gotoChangePsw)
        pixmap = QPixmap("img/LogoAfterColored&Crop2.png")
        self.Logo.setPixmap(pixmap)
        print("Login")

    def onClickBtnLogin(self):
        user = self.txtUsername.text()
        psw = self.txtPassword.text()
        print(checkLoginValid(user,psw))
        curUser = ifUser(user)
        if checkLoginValid(user,psw) == 1:
            self.txtMessage.setText("Success")
            addSession(idFromUser(user))
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

    def showData(self):
        print("Forget Passsword")

class changePswPage(QMainWindow):
    def __init__(self):
        super(changePswPage, self).__init__()
        loadUi("changePass.ui", self)
        self.btnLogin.clicked.connect(self.onClickBtnLogin)
        clickable(self.txtSignUp).connect(self.gotoSignUp)
        clickable(self.txtLogin).connect(self.gotoLogin)
        pixmap = QPixmap("img/LogoAfterColored&Crop2.png")
        self.Logo.setPixmap(pixmap)

    def gotoSignUp(self):
        signUp = signUpPage()
        widget.addWidget(signUp)
        widget.setCurrentWidget(signUp)

    def gotoLogin(self):
        login = loginPage()
        widget.addWidget(login)
        widget.setCurrentWidget(login)

    def onClickBtnLogin(self):
        user = self.txtUsername.text()
        psw = self.txtPassword.text() 
        rePsw = self.txtRPassword.text()
        msg = self.isValid(user,psw,rePsw)[1]
        if self.isValid(user,psw,rePsw)[0] :
            changePassword(user,psw)
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

class signUpPage(QMainWindow):
    def __init__(self):
        super(signUpPage, self).__init__()
        loadUi("SignUp2.ui", self)
        self.btnSignUp.clicked.connect(self.addUser)
        clickable(self.txtLogin).connect(self.gotoLogin)
        print("SignUp")

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
        print(isValid)
        if isValid[0]: 
            insertUser(fullname,name,email,password,gender,date,height,weight,bodyfat,fitExp,activity)
            addSession(idFromUser(name))
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
        self.initNav()
        self.initDate()

        self.btnSubmitE1.clicked.connect(self.onClickBtnE1)
        self.btnSubmitE2.clicked.connect(self.onClickBtnE2)
        self.btnSubmitE3.clicked.connect(self.onClickBtnE3)
        self.btnSubmitE4.clicked.connect(self.onClickBtnE4)
        self.btnSubmitE5.clicked.connect(self.onClickBtnE5)
        self.btnSubmitE6.clicked.connect(self.onClickBtnE6)
        self.btnToggle.clicked.connect(self.slideToRight)
        self.btnToggleEdit.clicked.connect(self.onClickToggleEdit)
        self.toggleEdit = 0

        self.calendarWidget.setMinimumDate(QDate.fromString(returnMinDate(getLastSession()), "yyyy-MM-dd"))
        #self.calendarWidget.setGridVisible(True)
        self.calendarWidget.setFirstDayOfWeek(Qt.Sunday)
        self.calendarWidget.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendarWidget.setHorizontalHeaderFormat(QCalendarWidget.ShortDayNames)
        self.calendarWidget.clicked.connect(self.onClickCalendar)
        self.cmbExcercise1.clear()

        exc = listOfExcercise()
        self.cmbExcercise1.addItems(exc)
        self.cmbExcercise2.addItems(exc)
        self.cmbExcercise3.addItems(exc)
        self.cmbExcercise4.addItems(exc)
        self.cmbExcercise5.addItems(exc)
        self.cmbExcercise6.addItems(exc)
        self.clearView()
        
        print("Lift Log")

    def initDate(self):
        for date in self.qtDateFromString():
            #date = QDate(2021,4,1)
            format = QTextCharFormat()
            format.setFont(QFont('Times', 12))
            format.setFontUnderline(True)
            format.setFontWeight(10)
            format.setUnderlineColor(QColor.fromRgb(0,0,0,50))
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

        self.btnHome.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftLog.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnTDEE.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftStats.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftRecord.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnMuscleStats.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnStrengthStandard.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnAccount.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')

        #connection
        self.btnTDEE.clicked.connect(self.gotoTDEE)
        self.btnLiftStats.clicked.connect(self.gotoLiftStats)
        self.btnLiftRecord.clicked.connect(self.gotoLiftRecord)
        self.btnStrengthStandard.clicked.connect(self.gotoStrengthStandard)
        self.btnAccount.clicked.connect(self.gotoLogin)

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

    def qtDateFromString(self):
        dateList = returnDateLogin(getLastSession())
        qtDate = [QDate.fromString(d, "yyyy-MM-dd") for d in dateList]
        return qtDate

    def slideToRight(self):
        width = self.LeftSideMenu.width()
        if width <= 100 :
            newWidth = 225
        else:
            newWidth = 50

        self.animation = QPropertyAnimation(self.LeftSideMenu, b"minimumWidth")
        self.animation.setDuration(500)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()

    def onClickCalendar(self):
        btnList = [self.btnSubmitE1,self.btnSubmitE2,self.btnSubmitE3,self.btnSubmitE4,self.btnSubmitE5,self.btnSubmitE6]
        date = self.calendarWidget.selectedDate()
        result = showRecordOf(f'{date.year()}-{date.month()}-{date.day()}',getLastSession())
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

    def showPopUp(self,message):
        msg = QMessageBox()
        msg.setWindowTitle("JournFit")
        msg.setText(message)
        msg.Icon(QMessageBox.Information)
        msg.StandardButton(QMessageBox.Ok|QMessageBox.Open)
        msg.setStyleSheet("QLabel{font-size: 20px; text-align: center;} QPushButton{ width:75px; font-size: 10px; }");
        x = msg.exec_()

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
        self.initDate()
    
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
            addLift(row[0], row[1], row[2], row[3], row[4], row[5])
        print(rowMaster)

    def submitDateRow(self, row, user_id):
        rowMaster = self.returnRowData(row, user_id)
        date = self.calendarWidget.selectedDate()
        selDate = f'{date.year()}-{date.month()}-{date.day()}'
        print(selDate)
        for row in rowMaster:
            print(row)
            try:
                print("Try")
                addLiftWithDate(row[0], row[1], selDate, row[2], row[3], row[4], row[5])
                print("Func")
            except Exception as ex:
                msg = f'Error : {type(ex).__name__} ,arg = {ex.args}'
                print(msg)
        print(rowMaster)

    def editRow(self, row, user_id):
        rowMaster = self.returnRowData(row, user_id)
        for row in rowMaster:
            try:
                updateLift(row[6], row[1], row[2], row[3], row[4], row[5])
            except Exception as ex:
                msg = f'Error : {type(ex).__name__} ,arg = {ex.args}'
                print(msg)

        date = self.calendarWidget.selectedDate()        
        result = showRecordOf(f'{date.year()}-{date.month()}-{date.day()}',getLastSession())
        self.clearView()
        self.writeToTable(result)
        #print(rowMaster)

    def deleteRow(self, row, user_id):
        rowMaster = self.returnRowData(row, user_id)
        for row in rowMaster:
            try:
                deleteLift(row[6])
                #print(row[6])
            except Exception as ex:
                msg = f'Error : {type(ex).__name__} ,arg = {ex.args}'
                print(msg)
        
        date = self.calendarWidget.selectedDate()        
        result = showRecordOf(f'{date.year()}-{date.month()}-{date.day()}',getLastSession())
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

        self.btnHome.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftLog.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnTDEE.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftStats.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftRecord.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnMuscleStats.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnStrengthStandard.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnAccount.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')

        #connection
        self.btnLiftLog.clicked.connect(self.gotoLiftLog)
        self.btnLiftStats.clicked.connect(self.gotoLiftStats)
        self.btnLiftRecord.clicked.connect(self.gotoLiftRecord)
        self.btnStrengthStandard.clicked.connect(self.gotoStrengthStandard)

    def slideToRight(self):
        width = self.LeftSideMenu.width()
        if width <= 100 :
            newWidth = 225
        else:
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

        self.btnHome.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftLog.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnTDEE.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftStats.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftRecord.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnMuscleStats.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnStrengthStandard.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnAccount.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')

        #connection
        self.btnLiftLog.clicked.connect(self.gotoLiftLog)
        self.btnTDEE.clicked.connect(self.gotoTDEE)
        self.btnLiftRecord.clicked.connect(self.gotoLiftRecord)
        self.btnStrengthStandard.clicked.connect(self.gotoStrengthStandard)

    def slideToRight(self):
        width = self.LeftSideMenu.width()
        if width <= 100 :
            newWidth = 225
        else:
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

        self.btnHome.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftLog.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnTDEE.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftStats.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftRecord.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnMuscleStats.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnStrengthStandard.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnAccount.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')

        #connection
        self.btnLiftLog.clicked.connect(self.gotoLiftLog)
        self.btnTDEE.clicked.connect(self.gotoTDEE)
        self.btnLiftStats.clicked.connect(self.gotoLiftStats)
        self.btnStrengthStandard.clicked.connect(self.gotoStrengthStandard)

    def slideToRight(self):
        width = self.LeftSideMenu.width()
        if width <= 100 :
            newWidth = 225
        else:
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

        self.btnHome.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftLog.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnTDEE.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftStats.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftRecord.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnMuscleStats.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnStrengthStandard.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnAccount.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')

        #connection
        self.btnLiftLog.clicked.connect(self.gotoLiftLog)
        self.btnTDEE.clicked.connect(self.gotoTDEE)
        self.btnLiftStats.clicked.connect(self.gotoLiftStats)
        self.btnLiftRecord.clicked.connect(self.gotoLiftRecord)

    def slideToRight(self):
        width = self.LeftSideMenu.width()
        if width <= 100 :
            newWidth = 225
        else:
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