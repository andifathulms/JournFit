import sys
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QDesktopWidget, QLabel, QHBoxLayout, QCalendarWidget, QLineEdit, QMessageBox, QInputDialog, QFileDialog, QWidget, QProgressDialog, QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QAction
from PyQt5.QtGui import QPixmap, QIcon, QTextCharFormat, QFont, QColor, QBrush, QFontMetrics
from PyQt5.QtWebEngineWidgets import *
from formula import *
from statistics import mean
from model import User, Lift, Plan
from PIL.ImageQt import ImageQt
from PIL import Image
import smtplib, ssl
import os
from email.message import EmailMessage
from win10toast import ToastNotifier
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import threading
import random
from password_strength import PasswordPolicy, PasswordStats
from newsScrapper import scrapingContent
from web import showWeb

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

def exportToPDF(self):
    progress = QProgressDialog("Copying files...","Cancel",0,100)
    progress.setWindowModality(Qt.WindowModal)
    progress.setAutoClose(False)
    progress.setMinimumDuration(0)
    progress.resize(progress.size()+QSize(70,70))
    tdee = tdeePage()
    liftstats = liftStatsPage()
    liftrecord = liftRecordPage()
    acc = accountPage()
    tdee.snapImg()
    liftstats.snapImg()
    liftrecord.snapImg()
    acc.snapImg()
    progress.setLabelText("Process Image 1")
    progress.setValue(5)
    time.sleep(0.1)
    try:
        img0 = Image.open("img/LogoAfterColored&Crop2.png")
        img = Image.new('RGB', img0.size, (255,255,255))
        img.paste(img0, mask=img0.split()[3])
    except:
        img0 = Image.open("img/LogoAfterColored&Crop2.png")

    progress.setLabelText("Process Image 2")
    progress.setValue(20)
    time.sleep(0.1)
    try:
        img1 = Image.open("screenshot/account.png")
        img1 = Image.new('RGB', img1.size, (255,255,255))
        img1.paste(img0, mask=img1.split()[3])
    except:
        img1 = Image.open("screenshot/account.png")

    progress.setLabelText("Process Image 3")
    progress.setValue(40)
    time.sleep(0.1)
    try:
        img2 = Image.open("screenshot/tdee.png")
        img2 = Image.new('RGB', img2.size, (255,255,255))
        img2.paste(img0, mask=img2.split()[3])
    except:
        img2 = Image.open("screenshot/tdee.png")

    progress.setLabelText("Process Image 4")
    progress.setValue(60)
    time.sleep(0.1)
    try:
        img3 = Image.open("screenshot/liftrecord.png")
        img3 = Image.new('RGB', img3.size, (255,255,255))
        img3.paste(img3, mask=img3.split()[3])
    except:
        img3 = Image.open("screenshot/liftrecord.png")

    progress.setLabelText("Process Image 5")
    progress.setValue(80)
    time.sleep(0.1)
    try:
        img4 = Image.open("screenshot/liftstats.png")  
        img4 = Image.new('RGB', img4.size, (255,255,255))
        img4.paste(img4, mask=img4.split()[3])
    except:
        img4 = Image.open("screenshot/liftstats.png")


    img_list = [img1,img2,img3,img4]
    progress.setLabelText("Complete")
    progress.setValue(99)
    time.sleep(0.1)
    file = "screenshot/PDF/Record.pdf"
    img.save(file, "PDF" ,resolution=100.0, save_all=True, append_images=img_list)
    win10Notif()

def sentToEmail(self):
    progress = QProgressDialog("Copying files...","Cancel",0,100)
    progress.setWindowModality(Qt.WindowModal)
    progress.setAutoClose(False)
    progress.setMinimumDuration(0)
    progress.resize(progress.size()+QSize(70,70))
    #progress.setMinimumWidth(200)


    msg = EmailMessage()
    progress.setLabelText("Authentification")
    msg['Subject'] = 'Journfit'
    msg['From'] = 'JournFit Notification'
    msg['To'] = 'officialandifathul@gmail.com'
    msg.set_content('Your training stats')
    progress.setValue(20)
    time.sleep(0.2)
    progress.setLabelText("Load HTML content")
    with open('html/msg.html', 'r') as file:
        html = file.read().rstrip('\n')

    msg.add_alternative(html, subtype='html')
    progress.setValue(40)
    time.sleep(0.2)
    progress.setLabelText("Attach PDF File")
    progress.setValue(60)
    with open("screenshot/record.pdf","rb") as f:
        content = f.read()
        msg.add_attachment(content, maintype='application', subtype='pdf', filename='record.pdf')
    time.sleep(0.1)
    progress.setLabelText("Send Email...")
    progress.setValue(80)
    with smtplib.SMTP('smtp.gmail.com',587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login("notifications-journfit@haloloyase.net", "RiemannConjecture")
        smtp.send_message(msg)
    time.sleep(0.1)
    progress.setLabelText("Complete")
    progress.setValue(99)
    time.sleep(0.1)
    progress.cancel()

    win10NotifEmail()

def sentOTPEmail(otp):
    msg = EmailMessage()
    msg['Subject'] = 'Journfit'
    msg['From'] = 'JournFit Notification'
    msg['To'] = 'officialandifathul@gmail.com'
    msg.set_content('Password Change')
    #with open('html/LETTER_OTP.html', 'r') as file:
    #    html = file.read().rstrip('\n')
    html = """\
            <!DOCTYPE html>
            <html>
            <head>
                <title>JournFit</title>
            </head>
            <body>
            <table style="margin-left: auto; margin-right: auto; height: 421px;" width="462">
            <tbody>
            <tr style="height: 424.4px;">
            <td style="width: 452.8px; height: 424.4px;">
            <table style="margin-left: auto; margin-right: auto; height: 26px;" width="434">
            <tbody>
            <tr>
            <td style="width: 424.8px;">&nbsp;<img src="img/LogoAfterColored&Crop2.png" alt="" width="444" height="175" /></td>
            </tr>
            </tbody>
            </table>
            <table style="margin-left: auto; margin-right: auto; height: 68px;" width="451">
            <tbody>
            <tr>
            <td style="width: 441.6px; text-align: center;"><strong><strong><br />[OTP] Password recovery</strong></strong><hr /><strong><br /></strong></td>
            </tr>
            </tbody>
            </table>
            <table style="margin-left: auto; margin-right: auto; height: 35px;" width="449">
            <tbody>
            <tr>
            <td style="width: 440px;">&nbsp;OTP : {otp}<br />&nbsp;is your JournFit Verivication code.<br /><hr /></td>
            </tr>
            </tbody>
            </table>
            <table style="margin-left: auto; margin-right: auto; height: 26px;" width="450">
            <tbody>
            <tr>
            <td style="width: 440.8px; text-align: center;"><span style="color: #999999;"><strong>&copy;2021 JournFit</strong></span></td>
            </tr>
            </tbody>
            </table>
            </td>
            </tr>
            </tbody>
            </table>
            </body>
            </html>
            """.format(otp=otp)
    msg.add_alternative(html, subtype='html')
    with smtplib.SMTP('smtp.gmail.com',587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login("notifications-journfit@haloloyase.net", "RiemannConjecture")
        smtp.send_message(msg)

    print("Sent")

def openInbox():
    url = "https://mail.google.com/mail/u/0/#inbox"
    options = Options()
    options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    options.headless = False
    print("Open Driver..")
    driver = webdriver.Chrome("C:\\Users\\LENOVO\\chromedriver.exe", options = options)
    print("Request URL..")
    driver.get(url)

def openFolder():
    path = "D:\\Project\\Journfit\\screenshot\\PDF"
    path = os.path.realpath(path)
    os.startfile(path)

def win10Notif():
    toaster = ToastNotifier()
    toaster.show_toast("JournFit","Your report has been made. Click to open!",duration=60, threaded=True, callback_on_click=openFolder)

def win10NotifEmail():
    toaster = ToastNotifier()
    toaster.show_toast("JournFit","You're email has been sent!",duration=15, threaded=True, callback_on_click=openInbox)
 
def checkPasswordPolicy(password):
    policy = PasswordPolicy.from_names(length=6,uppercase=1,numbers=1)
    return policy.test(password)

def checkPasswordStrength(password):
    try:
        stats = PasswordStats(password)
        return stats.strength()
    except:
        return 0

class openWeb(QWebEngineView):
    def __init__(self):
        super(openWeb, self).__init__()
        global news
        web = QWebEngineView()
        web.load(QUrl("www.google.com"))
        #web.load(QUrl("https://www.health.com/fitness/this-50-push-up-challenge-will-transform-your-body-in-30-days"))
        web.show()

class dialog(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Choose a file'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.file = ""
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        #self.openFileNameDialog()
        self.show()
    
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
            self.file = fileName
            #return fileName

class loginPage(QMainWindow):

    def __init__(self):
        super(loginPage, self).__init__()
        loadUi("Login2.ui", self)

        self.eyeClick = 0

        self.initUI()
        self.initConnection()

        print("Login")

    def initUI(self):
        pixmap = QPixmap("img/LogoAfterColored&Crop2.png")
        self.Logo.setPixmap(pixmap)
        pixmap = QPixmap("img/view.png")
        self.txtShowPass.setPixmap(pixmap)
        self.center()

    def center(self):
        """
        qtRectangle = self.frameGeometry()
        print(qtRectangle)
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        print(centerPoint)
        """
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2)) 
        #self.move(0,0)

    def initConnection(self):
        self.btnLogin.clicked.connect(self.onClickBtnLogin)
        clickable(self.txtSignUp).connect(self.gotoSignUp)
        clickable(self.txtForget).connect(self.gotoChangePsw)
        clickable(self.txtShowPass).connect(self.showHidePsw)

    def showHidePsw(self):
        if self.eyeClick%2 == 0:
            self.txtPassword.setEchoMode(QLineEdit.Normal)
        else:
            self.txtPassword.setEchoMode(QLineEdit.Password)
        self.eyeClick += 1

    def onClickBtnLogin(self):
        user = self.txtUsername.text()
        psw = self.txtPassword.text()
        #print(checkLoginValid(user,psw))

        if checkLoginValid(user,psw) == 1:
            self.txtMessage.setText("Success")
            user = User(idFromUser(user))
            user.addSession()
            self.gotoHome() #change later
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

    def gotoHome(self):
        home = homePage()
        widget.addWidget(home)
        widget.setCurrentWidget(home)

class changePswPage(QMainWindow):
    def __init__(self):
        super(changePswPage, self).__init__()
        loadUi("changePass.ui", self)

        self.eyeClick = 0
        self.eyeClick2 = 0
        self.initUI()
        self.initConnection()
        #self.otp = self.generateOTP()
        self.otp = "000000"

        self.count = 0
        self.start = False
        self.time = 60
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTimer)
        self.timer.start(100)

        print("Change Password")

    def initUI(self):
        pixmap = QPixmap("img/LogoAfterColored&Crop2.png")
        self.Logo.setPixmap(pixmap)
        pixmap = QPixmap("img/view.png")
        self.txtShowPass.setPixmap(pixmap)
        self.txtShowPass_2.setPixmap(pixmap)
        self.txtOTP.setPlaceholderText("Enter OTP Code")
        self.txtOTP.setVisible(False)
        self.txtTimer.setVisible(False)

    def initConnection(self):
        self.btnLogin.clicked.connect(self.onClickBtnLogin)
        clickable(self.txtSignUp).connect(lambda : self.gotoSignUp(self.timer))
        clickable(self.txtLogin).connect(lambda : self.gotoLogin(self.timer))
        self.txtPassword.cursorPositionChanged.connect(self.checkPassword)
        self.txtRPassword.cursorPositionChanged.connect(self.checkRPassword)
        clickable(self.txtShowPass).connect(self.showHidePsw)
        clickable(self.txtShowPass_2).connect(self.showHidePsw2)

    def showHidePsw(self):
        if self.eyeClick%2 == 0:
            self.txtPassword.setEchoMode(QLineEdit.Normal)
        else:
            self.txtPassword.setEchoMode(QLineEdit.Password)
        self.eyeClick += 1

    def showHidePsw2(self):
        if self.eyeClick2%2 == 0:
            self.txtRPassword.setEchoMode(QLineEdit.Normal)
        else:
            self.txtRPassword.setEchoMode(QLineEdit.Password)
        self.eyeClick2 += 1

    def onClickBtnLogin(self): #onClickBtnChangePassword
        user = self.txtUsername.text()
        psw = self.txtPassword.text() 
        rePsw = self.txtRPassword.text()
        msg = self.isValid(user,psw,rePsw)[1]
        if self.isValid(user,psw,rePsw)[0] and checkPasswordPolicy(psw) == [] :
            self.txtOTP.setVisible(True)
            self.txtTimer.setVisible(True)
            self.txtTimer.setText(str(self.time))
            self.count = self.time * 10
            self.start_action()
            self.otp = self.generateOTP()
            print(self.otp)
            #self.showTimer()
            self.txtMessage.setText("OTP has been sent to your email")
            self.txtOTP.cursorPositionChanged.connect(self.verifyOTP)
            loop = QEventLoop()
            sentOTPEmail(self.otp)
            loop.exec()
            #user = User(idFromUser(user))
            #user.changePassword(psw)
            #self.gotoLogin()
        else:
            self.txtMessage.setText(msg)
        
    def checkPassword(self):
        psw = self.txtPassword.text()
        result = [str(a) for a in checkPasswordPolicy(psw)]
        if("Length(6)" in result):
            self.txtMessage.setText("Password at least have 6 characters")
        elif("Uppercase(1)" in result):
            self.txtMessage.setText("Password at least have 1 uppercase")
        elif("Numbers(1)" in result):
            self.txtMessage.setText("Password at least have 1 numbers")
        else:
            self.txtMessage.setText("")

        score = checkPasswordStrength(psw)
        self.txtPswScore.setText(f'Score: {round(score,3)}')
        if score >= 0.8:
            self.txtPswStrength.setText("Very Strong")
            self.txtPswScore.setStyleSheet('*{color: rgb(237, 41, 57); background-color: rgb(255,255,255); border-style: none;}')
            self.txtPswStrength.setStyleSheet('*{color: rgb(237, 41, 57); background-color: rgb(255,255,255); border-style: none;}')
        elif score >= 0.6:
            self.txtPswStrength.setText("Strong")
            self.txtPswScore.setStyleSheet('*{color: rgb(255, 102, 0); background-color: rgb(255,255,255); border-style: none;}')
            self.txtPswStrength.setStyleSheet('*{color: rgb(255, 102, 0); background-color: rgb(255,255,255); border-style: none;}')
        elif score >= 0.5:
            self.txtPswStrength.setText("Good")
            self.txtPswScore.setStyleSheet('*{color: rgb(11, 102, 35); background-color: rgb(255,255,255); border-style: none;}')
            self.txtPswStrength.setStyleSheet('*{color: rgb(11, 102, 35); background-color: rgb(255,255,255); border-style: none;}')
        elif score >= 0.3:
            self.txtPswStrength.setText("Weak")
            self.txtPswScore.setStyleSheet('*{color: rgb(252, 226, 5); background-color: rgb(255,255,255); border-style: none;}')
            self.txtPswStrength.setStyleSheet('*{color: rgb(252, 226, 5); background-color: rgb(255,255,255); border-style: none;}')
        else:
            self.txtPswStrength.setText("Vulnerable")
            self.txtPswScore.setStyleSheet('*{color: rgb(100, 0, 100); background-color: rgb(255,255,255); border-style: none;}')
            self.txtPswStrength.setStyleSheet('*{color: rgb(100, 0, 100); background-color: rgb(255,255,255); border-style: none;}')

    def checkRPassword(self):
        psw = self.txtPassword.text()
        rpsw = self.txtRPassword.text()
        if psw != rpsw:
            self.txtMessage.setText("Password not matched")
        else:
            self.txtMessage.setText("")

    def verifyOTP(self):
        print("This")
        if len(self.txtOTP.text()) == 6:
            if self.txtOTP.text() == self.otp:
                user = User(idFromUser(self.txtUsername.text()))
                user.changePassword(self.txtPassword.text())
                self.gotoHome(self.timer)
            else:
                self.txtMessage.setText("Incorrect OTP. Try Again")
                self.txtOTP.setText("")

    def showTimer(self):
        #print("This")
        if self.start:
            self.count -= 1

            if self.count <= 100:
                self.txtTimer.setStyleSheet('*{color: rgb(255, 0, 68); background-color: rgb(255,255,255); border-style: none;}')
            elif self.count <= 200:
                self.txtTimer.setStyleSheet('*{color: rgb(255, 170, 0); background-color: rgb(255,255,255); border-style: none;}')
            else:
                self.txtTimer.setStyleSheet('*{color: rgb(0, 0, 0); background-color: rgb(255,255,255); border-style: none;}')

            if self.count == 0:
                self.start = False
                self.txtMessage.setText("Timeout. New OTP has been sent")
                self.otp = self.generateOTP()
                print(self.otp)
                self.txtTimer.setText(str(self.time))
                self.count = self.time * 10
                self.start_action()
                sentOTPEmail(self.otp)
        if self.start:
            text = str(self.count / 10) + " s"
            self.txtTimer.setText(text)

    def start_action(self):
        # making flag true
        self.start = True
  
        # count = 0
        if self.count == 0:
            self.start = False

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
        elif checkPasswordStrength(psw) < 0.5:
            msg = "Try better password"
        else:
            flag = True

        return [flag,msg]

    def generateOTP(self):
        pool = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R",
                "S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9"]
        
        otp = ""
        for i in range(0,6):
            otp += pool[random.randint(0,35)]
        print(otp)
        return otp

    def gotoSignUp(self,timer):
        timer.stop()
        signUp = signUpPage()
        widget.addWidget(signUp)
        widget.setCurrentWidget(signUp)

    def gotoLogin(self,timer):
        timer.stop()
        login = loginPage()
        widget.addWidget(login)
        widget.setCurrentWidget(login)

    def gotoLiftLog(self,timer):
        timer.stop()
        liftLog = liftLogPage()
        widget.addWidget(liftLog)
        widget.setCurrentWidget(liftLog)

    def gotoHome(self,timer):
        timer.stop()
        home = homePage()
        widget.addWidget(home)
        widget.setCurrentWidget(home)

class changePswPageFromInside(QMainWindow):
    def __init__(self):
        super(changePswPageFromInside, self).__init__()
        loadUi("changePass.ui", self)
        self.eyeClick = 0
        self.eyeClick2 = 0
        self.user = User(getLastSession()) 

        self.initUI()
        self.initConnection()
        self.txtPassword.setPlaceholderText("Enter your old password")
        self.txtRPassword.setPlaceholderText("Enter your new password")
        self.txtOTP.setVisible(False)
        print("Change Password")

    def initUI(self):
        pixmap = QPixmap("img/LogoAfterColored&Crop2.png")
        self.Logo.setPixmap(pixmap)
        self.txtUsername.setText(self.user.name)
        self.txtUsername.setReadOnly(True)
        pixmap = QPixmap("img/view.png")
        self.txtShowPass.setPixmap(pixmap)
        self.txtShowPass_2.setPixmap(pixmap)

    def initConnection(self):
        self.btnLogin.clicked.connect(self.onClickBtnLogin)
        clickable(self.txtSignUp).connect(self.gotoSignUp)
        clickable(self.txtLogin).connect(self.gotoAccount)
        self.txtRPassword.cursorPositionChanged.connect(self.checkPassword)
        clickable(self.txtShowPass).connect(self.showHidePsw)
        clickable(self.txtShowPass_2).connect(self.showHidePsw2)

    def showHidePsw(self):
        if self.eyeClick%2 == 0:
            self.txtPassword.setEchoMode(QLineEdit.Normal)
        else:
            self.txtPassword.setEchoMode(QLineEdit.Password)
        self.eyeClick += 1

    def showHidePsw2(self):
        if self.eyeClick2%2 == 0:
            self.txtRPassword.setEchoMode(QLineEdit.Normal)
        else:
            self.txtRPassword.setEchoMode(QLineEdit.Password)
        self.eyeClick2 += 1

    def onClickBtnLogin(self): #onClickBtnChangePassword
        user = self.txtUsername.text()
        oldpsw = self.txtPassword.text() 
        newpsw = self.txtRPassword.text()
        msg = self.isValid(user,oldpsw,newpsw)[1]
        if self.isValid(user,oldpsw,newpsw)[0] and checkPasswordPolicy(newpsw) == []:
            user = User(idFromUser(user))
            realpsw = user.password
            if oldpsw == realpsw:
                user.changePassword(newpsw)
                self.gotoAccount()
                print("==")
            else:
                self.txtMessage.setText("Password incorrect!")
                #self.txtPassword.setText("")
                #self.txtRPassword.setText("")
                print("!=")
        else:
            self.txtMessage.setText(msg)

    def isValid(self,user,old,new):
        flag = False
        msg = ""
        if user == "":
            msg = "Please fill username field!"
        elif old == "":
            msg = "Please fill old password field!"
        elif new == "":
            msg = "Please fill new password field!"
        elif ifUser(user) == 0:
            msg = "User not found!"
        elif checkPasswordStrength(new) < 0.5:
            msg = "Try better password"
        else:
            flag = True

        return [flag,msg]

    def checkPassword(self):
        psw = self.txtRPassword.text()
        result = [str(a) for a in checkPasswordPolicy(psw)]
        if("Length(6)" in result):
            self.txtMessage.setText("Password at least have 6 characters")
            print("IN")
        elif("Uppercase(1)" in result):
            self.txtMessage.setText("Password at least have 1 uppercase")
        elif("Numbers(1)" in result):
            self.txtMessage.setText("Password at least have 1 numbers")
        else:
            self.txtMessage.setText("")

        score = checkPasswordStrength(psw)
        self.txtPswScore.setText(f'Score: {round(score,3)}')
        if score >= 0.8:
            self.txtPswStrength.setText("Very Strong")
            self.txtPswScore.setStyleSheet('*{color: rgb(237, 41, 57); background-color: rgb(255,255,255); border-style: none;}')
            self.txtPswStrength.setStyleSheet('*{color: rgb(237, 41, 57); background-color: rgb(255,255,255); border-style: none;}')
        elif score >= 0.6:
            self.txtPswStrength.setText("Strong")
            self.txtPswScore.setStyleSheet('*{color: rgb(255, 102, 0); background-color: rgb(255,255,255); border-style: none;}')
            self.txtPswStrength.setStyleSheet('*{color: rgb(255, 102, 0); background-color: rgb(255,255,255); border-style: none;}')
        elif score >= 0.5:
            self.txtPswStrength.setText("Good")
            self.txtPswScore.setStyleSheet('*{color: rgb(11, 102, 35); background-color: rgb(255,255,255); border-style: none;}')
            self.txtPswStrength.setStyleSheet('*{color: rgb(11, 102, 35); background-color: rgb(255,255,255); border-style: none;}')
        elif score >= 0.3:
            self.txtPswStrength.setText("Weak")
            self.txtPswScore.setStyleSheet('*{color: rgb(252, 226, 5); background-color: rgb(255,255,255); border-style: none;}')
            self.txtPswStrength.setStyleSheet('*{color: rgb(252, 226, 5); background-color: rgb(255,255,255); border-style: none;}')
        else:
            self.txtPswStrength.setText("Vulnerable")
            self.txtPswScore.setStyleSheet('*{color: rgb(100, 0, 100); background-color: rgb(255,255,255); border-style: none;}')
            self.txtPswStrength.setStyleSheet('*{color: rgb(100, 0, 100); background-color: rgb(255,255,255); border-style: none;}')

    def gotoSignUp(self):
        signUp = signUpPage()
        widget.addWidget(signUp)
        widget.setCurrentWidget(signUp)

    def gotoAccount(self):
        acc = accountPage()
        widget.addWidget(acc)
        widget.setCurrentWidget(acc) 

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

class homePage(QMainWindow):
    def __init__(self):
        super(homePage, self).__init__()
        loadUi("Home.ui", self)

        self.user = User(getLastSession())
        self.settingClick = 0
        self.initConnection()
        self.initNav()
        self.initUI()
        self.getNews()

    def initUI(self):
        self.frame1.setStyleSheet('QFrame {image: url(img/Squat.png) no-repeat center center fixed;border : transparent;}')
        self.frame2.setStyleSheet('QFrame {image: url(img/Deadlift.png) no-repeat center center fixed;border : transparent;}')
        self.frame3.setStyleSheet('QFrame {image: url(img/BP.png) no-repeat center center fixed;border : transparent;}')
        self.frame4.setStyleSheet('QFrame {image: url(img/FrontSquat.png) no-repeat center center fixed;border : transparent;}')
        self.frame5.setStyleSheet('QFrame {image: url(img/OverheadPress.png) no-repeat center center fixed;border : transparent;}')
        self.frame6.setStyleSheet('QFrame {image: url(img/SumoDeadlift.png) no-repeat center center fixed;border : transparent;}')
        self.frame7.setStyleSheet('QFrame {image: url(img/Latpulldown.png) no-repeat center center fixed;border : transparent;}')
        self.frame8.setStyleSheet('QFrame {image: url(img/Barbellrow.png) no-repeat center center fixed;border : transparent;}')
        self.frame9.setStyleSheet('QFrame {image: url(img/Pullups.png) no-repeat center center fixed;border : transparent;}')
        self.frame10.setStyleSheet('QFrame {image: url(img/Cablerow.png) no-repeat center center fixed;border : transparent;}')
        self.frame11.setStyleSheet('QFrame {image: url(img/InclineBenchpress.png) no-repeat center center fixed;border : transparent;}')
        self.frame12.setStyleSheet('QFrame {image: url(img/Legpress.png) no-repeat center center fixed;border : transparent;}')

    def initConnection(self):
        self.btnToggle.clicked.connect(self.slideToRight)
        self.btnToPDF.clicked.connect(exportToPDF)
        self.btnToEmail.clicked.connect(sentToEmail)
        self.btnChangePsw.clicked.connect(self.gotoChangePsw)
        self.btnLogout.clicked.connect(self.gotoLogin)
        self.btnLiftLog.clicked.connect(self.gotoLiftLog)
        self.btnSettings.clicked.connect(self.onClickBtnSettings)
        self.btnBS.clicked.connect(self.gotoSquat)
        clickable(self.news1).connect(lambda : self.gotoOpenWeb(1,0))
        clickable(self.news2).connect(lambda : self.gotoOpenWeb(1,1))
        clickable(self.news3).connect(lambda : self.gotoOpenWeb(1,2))
        clickable(self.news4).connect(lambda : self.gotoOpenWeb(1,3))
        clickable(self.news5).connect(lambda : self.gotoOpenWeb(1,4))
        clickable(self.tnews1).connect(lambda : self.gotoOpenWeb(3,0))
        clickable(self.tnews2).connect(lambda : self.gotoOpenWeb(3,1))
        clickable(self.tnews3).connect(lambda : self.gotoOpenWeb(3,2))
        clickable(self.tnews4).connect(lambda : self.gotoOpenWeb(3,3))
        clickable(self.tnews5).connect(lambda : self.gotoOpenWeb(3,4))
        clickable(self.wnews1).connect(lambda : self.gotoOpenWeb(5,0))
        clickable(self.wnews2).connect(lambda : self.gotoOpenWeb(5,1))
        clickable(self.wnews3).connect(lambda : self.gotoOpenWeb(5,2))
        clickable(self.wnews4).connect(lambda : self.gotoOpenWeb(5,3))
        clickable(self.wnews5).connect(lambda : self.gotoOpenWeb(5,4))

    def initNav(self):
        pxm0 = QPixmap("img/menuWhiteColor24Px.png")
        icon0 = QIcon(pxm0)
        pxm1 = QPixmap("img/homeWhiteColor24Px.png")
        icon1 = QIcon(pxm1)
        pxm2 = QPixmap("img/userWhiteColor24Px.png")
        icon2 = QIcon(pxm2)
        pxm3 = QPixmap("img/document.png")
        icon3 = QIcon(pxm3)
        pxm4 = QPixmap("img/analytics.png")
        icon4 = QIcon(pxm4)
        pxm5 = QPixmap("img/bar-chart.png")
        icon5 = QIcon(pxm5)
        pxm6 = QPixmap("img/list.png")
        icon6 = QIcon(pxm6)
        pxm7 = QPixmap("img/meal.png")
        icon7 = QIcon(pxm7)
        self.btnToggle.setIcon(icon0)
        self.btnHome.setIcon(icon1)
        self.btnLiftLog.setIcon(icon3)
        self.btnTDEE.setIcon(icon7)
        self.btnLiftStats.setIcon(icon4)
        self.btnLiftRecord.setIcon(icon6)
        self.btnStrengthStandard.setIcon(icon5)
        self.btnAccount.setIcon(icon2)
        pxm4 = QPixmap("img/Tulisan JournFit-01.png")
        self.appLogo.setPixmap(pxm4)
        pxm7 = QPixmap("img/logout.png")
        icon7 = QIcon(pxm7)
        self.btnLogout.setIcon(icon7)
        pxm8 = QPixmap("img/padlock.png")
        icon8 = QIcon(pxm8)
        self.btnChangePsw.setIcon(icon8)
        pxm9 = QPixmap("img/settingsWhiteColor24Px.png")
        icon9 = QIcon(pxm9)
        self.btnSettings.setIcon(icon9)
        pxm10 = QPixmap("img/pdf.png")
        icon10 = QIcon(pxm10)
        self.btnToPDF.setIcon(icon10)
        pxm11 = QPixmap("img/mail.png")
        icon11 = QIcon(pxm11)
        self.btnToEmail.setIcon(icon11)
        self.btnLogout.setVisible(False)
        self.btnChangePsw.setVisible(False)
        self.btnToPDF.setVisible(False)
        self.btnToEmail.setVisible(False)
        if self.user.image == "":
            pxmFoto = QPixmap("img/user.png")
            self.profileFoto.setPixmap(pxmFoto)
        else:
            pxmFoto = QPixmap(self.user.image)
            self.profileFoto.setPixmap(pxmFoto)

        self.btnToggle.setStyleSheet('*{text-align: center}')
        self.btnHome.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(4, 155, 255); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftLog.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnTDEE.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftStats.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftRecord.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnStrengthStandard.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnAccount.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.profileName.setStyleSheet('*{border-radius : 10px; color: rgb(255, 255, 255);}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnSettings.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnToPDF.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnToEmail.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnChangePsw.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLogout.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')

        self.btnHome.setText("")
        self.btnLiftLog.setText("")
        self.btnTDEE.setText("")
        self.btnLiftStats.setText("")
        self.btnLiftRecord.setText("")
        self.btnStrengthStandard.setText("")
        self.btnAccount.setText("")
        self.profileName.setText(self.user.name)
        self.btnSettings.setText("")
        self.btnToPDF.setText("")
        self.btnToEmail.setText("")
        self.btnChangePsw.setText("")
        self.btnLogout.setText("")

        #connection
        self.btnTDEE.clicked.connect(self.gotoTDEE)
        self.btnLiftStats.clicked.connect(self.gotoLiftStats)
        self.btnLiftRecord.clicked.connect(self.gotoLiftRecord)
        self.btnStrengthStandard.clicked.connect(self.gotoStrengthStandard)
        self.btnAccount.clicked.connect(self.gotoAccount)
        clickable(self.profileName).connect(self.gotoAccount)
        clickable(self.profileFoto).connect(self.gotoAccount)

    def slideToRight(self):
        width = self.LeftSideMenu.width()
        if width <= 100 :
            self.btnHome.setText("Home")
            self.btnLiftLog.setText("Lift Log")
            self.btnTDEE.setText("TDEE Stats")
            self.btnLiftStats.setText("Lift Stats")
            self.btnLiftRecord.setText("Lift Record")
            self.btnStrengthStandard.setText("Strength Standard")
            self.btnAccount.setText("Account")
            self.btnSettings.setText("Settings")
            self.btnToPDF.setText("Export To PDF")
            self.btnToEmail.setText("Sent To Email")
            self.btnChangePsw.setText("Change Password")
            self.btnLogout.setText("Logout")
            newWidth = 225
        else:
            self.btnHome.setText("")
            self.btnLiftLog.setText("")
            self.btnTDEE.setText("")
            self.btnLiftStats.setText("")
            self.btnLiftRecord.setText("")
            self.btnStrengthStandard.setText("")
            self.btnAccount.setText("")
            self.btnSettings.setText("")
            self.btnToPDF.setText("")
            self.btnToEmail.setText("")
            self.btnChangePsw.setText("")
            self.btnLogout.setText("")
            newWidth = 50

        self.animation = QPropertyAnimation(self.LeftSideMenu, b"minimumWidth")
        self.animation.setDuration(500)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()

    def onClickBtnSettings(self):
        self.settingClick += 1
        if self.settingClick%2 == 0:
            self.btnLogout.setVisible(False)
            self.btnChangePsw.setVisible(False)
            self.btnToPDF.setVisible(False)
            self.btnToEmail.setVisible(False)
            self.slideToRight()
        else:
            self.btnLogout.setVisible(True)
            self.btnChangePsw.setVisible(True)
            self.btnToPDF.setVisible(True)
            self.btnToEmail.setVisible(True)
            self.slideToRight()

    def getNews(self):
        global news
        self.news1.setText(news[0][0])
        self.news2.setText(news[0][1])
        self.news3.setText(news[0][2])
        self.news4.setText(news[0][3])
        self.news5.setText(news[0][4])
        self.tnews1.setText(news[2][0])
        self.tnews2.setText(news[2][1])
        self.tnews3.setText(news[2][2])
        self.tnews4.setText(news[2][3])
        self.tnews5.setText(news[2][4])
        self.wnews1.setText(news[4][0])
        self.wnews2.setText(news[4][1])
        self.wnews3.setText(news[4][2])
        self.wnews4.setText(news[4][3])
        self.wnews5.setText(news[4][4])

    def gotoOpenWeb(self,url,idx):
        url = news[url][idx]
        loop = QEventLoop()
        web = QWebEngineView()
        web.load(QUrl(url))
        web.show()
        loop.exec()

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
    
    def gotoAccount(self):
        acc = accountPage()
        widget.addWidget(acc)
        widget.setCurrentWidget(acc) 

    def gotoChangePsw(self):
        changePsw = changePswPageFromInside()
        widget.addWidget(changePsw)
        widget.setCurrentWidget(changePsw)

    def gotoLogin(self):
        login = loginPage()
        widget.addWidget(login)
        widget.setCurrentWidget(login)

    def gotoLiftLog(self):
        liftLog = liftLogPage()
        widget.addWidget(liftLog)
        widget.setCurrentWidget(liftLog)

    def gotoSquat(self):
        exc = excSquat()
        widget.addWidget(exc)
        widget.setCurrentWidget(exc)


class excSquat(QMainWindow):
    def __init__(self):
        super(excSquat, self).__init__()
        loadUi("squat.ui", self)

        self.user = User(getLastSession())
        self.settingClick = 0
        self.initConnection()
        self.initNav()
        self.initUI()

    def initUI(self):
        pass

    def initConnection(self):
        self.btnToggle.clicked.connect(self.slideToRight)
        self.btnToPDF.clicked.connect(exportToPDF)
        self.btnToEmail.clicked.connect(sentToEmail)
        self.btnChangePsw.clicked.connect(self.gotoChangePsw)
        self.btnLogout.clicked.connect(self.gotoLogin)
        self.btnLiftLog.clicked.connect(self.gotoLiftLog)
        self.btnSettings.clicked.connect(self.onClickBtnSettings)
        self.btnBack.clicked.connect(self.gotoHome)
        self.btnPrev.clicked.connect(self.gotoLegPress)
        self.btnNext.clicked.connect(self.gotoDeadlift)

    def initNav(self):
        pxm0 = QPixmap("img/menuWhiteColor24Px.png")
        icon0 = QIcon(pxm0)
        pxm1 = QPixmap("img/homeWhiteColor24Px.png")
        icon1 = QIcon(pxm1)
        pxm2 = QPixmap("img/userWhiteColor24Px.png")
        icon2 = QIcon(pxm2)
        pxm3 = QPixmap("img/document.png")
        icon3 = QIcon(pxm3)
        pxm4 = QPixmap("img/analytics.png")
        icon4 = QIcon(pxm4)
        pxm5 = QPixmap("img/bar-chart.png")
        icon5 = QIcon(pxm5)
        pxm6 = QPixmap("img/list.png")
        icon6 = QIcon(pxm6)
        pxm7 = QPixmap("img/meal.png")
        icon7 = QIcon(pxm7)
        self.btnToggle.setIcon(icon0)
        self.btnHome.setIcon(icon1)
        self.btnLiftLog.setIcon(icon3)
        self.btnTDEE.setIcon(icon7)
        self.btnLiftStats.setIcon(icon4)
        self.btnLiftRecord.setIcon(icon6)
        self.btnStrengthStandard.setIcon(icon5)
        self.btnAccount.setIcon(icon2)
        pxm4 = QPixmap("img/Tulisan JournFit-01.png")
        self.appLogo.setPixmap(pxm4)
        pxm7 = QPixmap("img/logout.png")
        icon7 = QIcon(pxm7)
        self.btnLogout.setIcon(icon7)
        pxm8 = QPixmap("img/padlock.png")
        icon8 = QIcon(pxm8)
        self.btnChangePsw.setIcon(icon8)
        pxm9 = QPixmap("img/settingsWhiteColor24Px.png")
        icon9 = QIcon(pxm9)
        self.btnSettings.setIcon(icon9)
        pxm10 = QPixmap("img/pdf.png")
        icon10 = QIcon(pxm10)
        self.btnToPDF.setIcon(icon10)
        pxm11 = QPixmap("img/mail.png")
        icon11 = QIcon(pxm11)
        self.btnToEmail.setIcon(icon11)
        self.btnLogout.setVisible(False)
        self.btnChangePsw.setVisible(False)
        self.btnToPDF.setVisible(False)
        self.btnToEmail.setVisible(False)
        if self.user.image == "":
            pxmFoto = QPixmap("img/user.png")
            self.profileFoto.setPixmap(pxmFoto)
        else:
            pxmFoto = QPixmap(self.user.image)
            self.profileFoto.setPixmap(pxmFoto)

        self.btnToggle.setStyleSheet('*{text-align: center}')
        self.btnHome.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftLog.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(4, 155, 255); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnTDEE.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftStats.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftRecord.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnStrengthStandard.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnAccount.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.profileName.setStyleSheet('*{border-radius : 10px; color: rgb(255, 255, 255);}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnSettings.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnToPDF.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnToEmail.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnChangePsw.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLogout.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')

        self.btnHome.setText("")
        self.btnLiftLog.setText("")
        self.btnTDEE.setText("")
        self.btnLiftStats.setText("")
        self.btnLiftRecord.setText("")
        self.btnStrengthStandard.setText("")
        self.btnAccount.setText("")
        self.profileName.setText(self.user.name)
        self.btnSettings.setText("")
        self.btnToPDF.setText("")
        self.btnToEmail.setText("")
        self.btnChangePsw.setText("")
        self.btnLogout.setText("")

        #connection
        self.btnTDEE.clicked.connect(self.gotoTDEE)
        self.btnLiftStats.clicked.connect(self.gotoLiftStats)
        self.btnLiftRecord.clicked.connect(self.gotoLiftRecord)
        self.btnStrengthStandard.clicked.connect(self.gotoStrengthStandard)
        self.btnAccount.clicked.connect(self.gotoAccount)
        clickable(self.profileName).connect(self.gotoAccount)
        clickable(self.profileFoto).connect(self.gotoAccount)

    def slideToRight(self):
        width = self.LeftSideMenu.width()
        if width <= 100 :
            self.btnHome.setText("Home")
            self.btnLiftLog.setText("Lift Log")
            self.btnTDEE.setText("TDEE Stats")
            self.btnLiftStats.setText("Lift Stats")
            self.btnLiftRecord.setText("Lift Record")
            self.btnStrengthStandard.setText("Strength Standard")
            self.btnAccount.setText("Account")
            self.btnSettings.setText("Settings")
            self.btnToPDF.setText("Export To PDF")
            self.btnToEmail.setText("Sent To Email")
            self.btnChangePsw.setText("Change Password")
            self.btnLogout.setText("Logout")
            newWidth = 225
        else:
            self.btnHome.setText("")
            self.btnLiftLog.setText("")
            self.btnTDEE.setText("")
            self.btnLiftStats.setText("")
            self.btnLiftRecord.setText("")
            self.btnStrengthStandard.setText("")
            self.btnAccount.setText("")
            self.btnSettings.setText("")
            self.btnToPDF.setText("")
            self.btnToEmail.setText("")
            self.btnChangePsw.setText("")
            self.btnLogout.setText("")
            newWidth = 50

        self.animation = QPropertyAnimation(self.LeftSideMenu, b"minimumWidth")
        self.animation.setDuration(500)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()

    def onClickBtnSettings(self):
        self.settingClick += 1
        if self.settingClick%2 == 0:
            self.btnLogout.setVisible(False)
            self.btnChangePsw.setVisible(False)
            self.btnToPDF.setVisible(False)
            self.btnToEmail.setVisible(False)
            self.slideToRight()
        else:
            self.btnLogout.setVisible(True)
            self.btnChangePsw.setVisible(True)
            self.btnToPDF.setVisible(True)
            self.btnToEmail.setVisible(True)
            self.slideToRight()

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
    
    def gotoAccount(self):
        acc = accountPage()
        widget.addWidget(acc)
        widget.setCurrentWidget(acc) 

    def gotoChangePsw(self):
        changePsw = changePswPageFromInside()
        widget.addWidget(changePsw)
        widget.setCurrentWidget(changePsw)

    def gotoLogin(self):
        login = loginPage()
        widget.addWidget(login)
        widget.setCurrentWidget(login)

    def gotoLiftLog(self):
        liftLog = liftLogPage()
        widget.addWidget(liftLog)
        widget.setCurrentWidget(liftLog)

    def gotoHome(self):
        home = homePage()
        widget.addWidget(home)
        widget.setCurrentWidget(home)

    def gotoLegPress(self):
        legpress = excLegPress()
        widget.addWidget(legpress)
        widget.setCurrentWidget(legpress)

    def gotoDeadlift(self):
        deadlift = excDeadlift()
        widget.addWidget(deadlift)
        widget.setCurrentWidget(deadlift)

class excDeadlift(QMainWindow):
    def __init__(self):
        super(excDeadlift, self).__init__()
        loadUi("deadlift.ui", self)

        self.user = User(getLastSession())
        self.settingClick = 0
        self.initConnection()
        self.initNav()
        self.initUI()

    def initUI(self):
        pass

    def initConnection(self):
        self.btnToggle.clicked.connect(self.slideToRight)
        self.btnToPDF.clicked.connect(exportToPDF)
        self.btnToEmail.clicked.connect(sentToEmail)
        self.btnChangePsw.clicked.connect(self.gotoChangePsw)
        self.btnLogout.clicked.connect(self.gotoLogin)
        self.btnLiftLog.clicked.connect(self.gotoLiftLog)
        self.btnSettings.clicked.connect(self.onClickBtnSettings)
        self.btnBack.clicked.connect(self.gotoHome)
        self.btnPrev.clicked.connect(self.gotoSquat)
        self.btnNext.clicked.connect(self.gotoBenchPress)

    def initNav(self):
        pxm0 = QPixmap("img/menuWhiteColor24Px.png")
        icon0 = QIcon(pxm0)
        pxm1 = QPixmap("img/homeWhiteColor24Px.png")
        icon1 = QIcon(pxm1)
        pxm2 = QPixmap("img/userWhiteColor24Px.png")
        icon2 = QIcon(pxm2)
        pxm3 = QPixmap("img/document.png")
        icon3 = QIcon(pxm3)
        pxm4 = QPixmap("img/analytics.png")
        icon4 = QIcon(pxm4)
        pxm5 = QPixmap("img/bar-chart.png")
        icon5 = QIcon(pxm5)
        pxm6 = QPixmap("img/list.png")
        icon6 = QIcon(pxm6)
        pxm7 = QPixmap("img/meal.png")
        icon7 = QIcon(pxm7)
        self.btnToggle.setIcon(icon0)
        self.btnHome.setIcon(icon1)
        self.btnLiftLog.setIcon(icon3)
        self.btnTDEE.setIcon(icon7)
        self.btnLiftStats.setIcon(icon4)
        self.btnLiftRecord.setIcon(icon6)
        self.btnStrengthStandard.setIcon(icon5)
        self.btnAccount.setIcon(icon2)
        pxm4 = QPixmap("img/Tulisan JournFit-01.png")
        self.appLogo.setPixmap(pxm4)
        pxm7 = QPixmap("img/logout.png")
        icon7 = QIcon(pxm7)
        self.btnLogout.setIcon(icon7)
        pxm8 = QPixmap("img/padlock.png")
        icon8 = QIcon(pxm8)
        self.btnChangePsw.setIcon(icon8)
        pxm9 = QPixmap("img/settingsWhiteColor24Px.png")
        icon9 = QIcon(pxm9)
        self.btnSettings.setIcon(icon9)
        pxm10 = QPixmap("img/pdf.png")
        icon10 = QIcon(pxm10)
        self.btnToPDF.setIcon(icon10)
        pxm11 = QPixmap("img/mail.png")
        icon11 = QIcon(pxm11)
        self.btnToEmail.setIcon(icon11)
        self.btnLogout.setVisible(False)
        self.btnChangePsw.setVisible(False)
        self.btnToPDF.setVisible(False)
        self.btnToEmail.setVisible(False)
        if self.user.image == "":
            pxmFoto = QPixmap("img/user.png")
            self.profileFoto.setPixmap(pxmFoto)
        else:
            pxmFoto = QPixmap(self.user.image)
            self.profileFoto.setPixmap(pxmFoto)

        self.btnToggle.setStyleSheet('*{text-align: center}')
        self.btnHome.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftLog.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(4, 155, 255); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnTDEE.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftStats.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftRecord.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnStrengthStandard.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnAccount.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.profileName.setStyleSheet('*{border-radius : 10px; color: rgb(255, 255, 255);}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnSettings.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnToPDF.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnToEmail.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnChangePsw.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLogout.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')

        self.btnHome.setText("")
        self.btnLiftLog.setText("")
        self.btnTDEE.setText("")
        self.btnLiftStats.setText("")
        self.btnLiftRecord.setText("")
        self.btnStrengthStandard.setText("")
        self.btnAccount.setText("")
        self.profileName.setText(self.user.name)
        self.btnSettings.setText("")
        self.btnToPDF.setText("")
        self.btnToEmail.setText("")
        self.btnChangePsw.setText("")
        self.btnLogout.setText("")

        #connection
        self.btnTDEE.clicked.connect(self.gotoTDEE)
        self.btnLiftStats.clicked.connect(self.gotoLiftStats)
        self.btnLiftRecord.clicked.connect(self.gotoLiftRecord)
        self.btnStrengthStandard.clicked.connect(self.gotoStrengthStandard)
        self.btnAccount.clicked.connect(self.gotoAccount)
        clickable(self.profileName).connect(self.gotoAccount)
        clickable(self.profileFoto).connect(self.gotoAccount)

    def slideToRight(self):
        width = self.LeftSideMenu.width()
        if width <= 100 :
            self.btnHome.setText("Home")
            self.btnLiftLog.setText("Lift Log")
            self.btnTDEE.setText("TDEE Stats")
            self.btnLiftStats.setText("Lift Stats")
            self.btnLiftRecord.setText("Lift Record")
            self.btnStrengthStandard.setText("Strength Standard")
            self.btnAccount.setText("Account")
            self.btnSettings.setText("Settings")
            self.btnToPDF.setText("Export To PDF")
            self.btnToEmail.setText("Sent To Email")
            self.btnChangePsw.setText("Change Password")
            self.btnLogout.setText("Logout")
            newWidth = 225
        else:
            self.btnHome.setText("")
            self.btnLiftLog.setText("")
            self.btnTDEE.setText("")
            self.btnLiftStats.setText("")
            self.btnLiftRecord.setText("")
            self.btnStrengthStandard.setText("")
            self.btnAccount.setText("")
            self.btnSettings.setText("")
            self.btnToPDF.setText("")
            self.btnToEmail.setText("")
            self.btnChangePsw.setText("")
            self.btnLogout.setText("")
            newWidth = 50

        self.animation = QPropertyAnimation(self.LeftSideMenu, b"minimumWidth")
        self.animation.setDuration(500)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()

    def onClickBtnSettings(self):
        self.settingClick += 1
        if self.settingClick%2 == 0:
            self.btnLogout.setVisible(False)
            self.btnChangePsw.setVisible(False)
            self.btnToPDF.setVisible(False)
            self.btnToEmail.setVisible(False)
            self.slideToRight()
        else:
            self.btnLogout.setVisible(True)
            self.btnChangePsw.setVisible(True)
            self.btnToPDF.setVisible(True)
            self.btnToEmail.setVisible(True)
            self.slideToRight()

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
    
    def gotoAccount(self):
        acc = accountPage()
        widget.addWidget(acc)
        widget.setCurrentWidget(acc) 

    def gotoChangePsw(self):
        changePsw = changePswPageFromInside()
        widget.addWidget(changePsw)
        widget.setCurrentWidget(changePsw)

    def gotoLogin(self):
        login = loginPage()
        widget.addWidget(login)
        widget.setCurrentWidget(login)

    def gotoLiftLog(self):
        liftLog = liftLogPage()
        widget.addWidget(liftLog)
        widget.setCurrentWidget(liftLog)

    def gotoHome(self):
        home = homePage()
        widget.addWidget(home)
        widget.setCurrentWidget(home)

    def gotoSquat(self):
        squat = excSquat()
        widget.addWidget(squat)
        widget.setCurrentWidget(squat)

    def gotoBenchPress(self):
        benchpress = excBenchPress()
        widget.addWidget(benchpress)
        widget.setCurrentWidget(benchpress)

class excBenchPress(QMainWindow):
    def __init__(self):
        super(excBenchPress, self).__init__()
        loadUi("benchpress.ui", self)

        self.user = User(getLastSession())
        self.settingClick = 0
        self.initConnection()
        self.initNav()
        self.initUI()

    def initUI(self):
        pass

    def initConnection(self):
        self.btnToggle.clicked.connect(self.slideToRight)
        self.btnToPDF.clicked.connect(exportToPDF)
        self.btnToEmail.clicked.connect(sentToEmail)
        self.btnChangePsw.clicked.connect(self.gotoChangePsw)
        self.btnLogout.clicked.connect(self.gotoLogin)
        self.btnLiftLog.clicked.connect(self.gotoLiftLog)
        self.btnSettings.clicked.connect(self.onClickBtnSettings)
        self.btnBack.clicked.connect(self.gotoHome)
        self.btnPrev.clicked.connect(self.gotoDeadlift)
        self.btnNext.clicked.connect(self.gotoFrontSquat)

    def initNav(self):
        pxm0 = QPixmap("img/menuWhiteColor24Px.png")
        icon0 = QIcon(pxm0)
        pxm1 = QPixmap("img/homeWhiteColor24Px.png")
        icon1 = QIcon(pxm1)
        pxm2 = QPixmap("img/userWhiteColor24Px.png")
        icon2 = QIcon(pxm2)
        pxm3 = QPixmap("img/document.png")
        icon3 = QIcon(pxm3)
        pxm4 = QPixmap("img/analytics.png")
        icon4 = QIcon(pxm4)
        pxm5 = QPixmap("img/bar-chart.png")
        icon5 = QIcon(pxm5)
        pxm6 = QPixmap("img/list.png")
        icon6 = QIcon(pxm6)
        pxm7 = QPixmap("img/meal.png")
        icon7 = QIcon(pxm7)
        self.btnToggle.setIcon(icon0)
        self.btnHome.setIcon(icon1)
        self.btnLiftLog.setIcon(icon3)
        self.btnTDEE.setIcon(icon7)
        self.btnLiftStats.setIcon(icon4)
        self.btnLiftRecord.setIcon(icon6)
        self.btnStrengthStandard.setIcon(icon5)
        self.btnAccount.setIcon(icon2)
        pxm4 = QPixmap("img/Tulisan JournFit-01.png")
        self.appLogo.setPixmap(pxm4)
        pxm7 = QPixmap("img/logout.png")
        icon7 = QIcon(pxm7)
        self.btnLogout.setIcon(icon7)
        pxm8 = QPixmap("img/padlock.png")
        icon8 = QIcon(pxm8)
        self.btnChangePsw.setIcon(icon8)
        pxm9 = QPixmap("img/settingsWhiteColor24Px.png")
        icon9 = QIcon(pxm9)
        self.btnSettings.setIcon(icon9)
        pxm10 = QPixmap("img/pdf.png")
        icon10 = QIcon(pxm10)
        self.btnToPDF.setIcon(icon10)
        pxm11 = QPixmap("img/mail.png")
        icon11 = QIcon(pxm11)
        self.btnToEmail.setIcon(icon11)
        self.btnLogout.setVisible(False)
        self.btnChangePsw.setVisible(False)
        self.btnToPDF.setVisible(False)
        self.btnToEmail.setVisible(False)
        if self.user.image == "":
            pxmFoto = QPixmap("img/user.png")
            self.profileFoto.setPixmap(pxmFoto)
        else:
            pxmFoto = QPixmap(self.user.image)
            self.profileFoto.setPixmap(pxmFoto)

        self.btnToggle.setStyleSheet('*{text-align: center}')
        self.btnHome.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftLog.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(4, 155, 255); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnTDEE.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftStats.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftRecord.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnStrengthStandard.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnAccount.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.profileName.setStyleSheet('*{border-radius : 10px; color: rgb(255, 255, 255);}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnSettings.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnToPDF.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnToEmail.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnChangePsw.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLogout.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')

        self.btnHome.setText("")
        self.btnLiftLog.setText("")
        self.btnTDEE.setText("")
        self.btnLiftStats.setText("")
        self.btnLiftRecord.setText("")
        self.btnStrengthStandard.setText("")
        self.btnAccount.setText("")
        self.profileName.setText(self.user.name)
        self.btnSettings.setText("")
        self.btnToPDF.setText("")
        self.btnToEmail.setText("")
        self.btnChangePsw.setText("")
        self.btnLogout.setText("")

        #connection
        self.btnTDEE.clicked.connect(self.gotoTDEE)
        self.btnLiftStats.clicked.connect(self.gotoLiftStats)
        self.btnLiftRecord.clicked.connect(self.gotoLiftRecord)
        self.btnStrengthStandard.clicked.connect(self.gotoStrengthStandard)
        self.btnAccount.clicked.connect(self.gotoAccount)
        clickable(self.profileName).connect(self.gotoAccount)
        clickable(self.profileFoto).connect(self.gotoAccount)

    def slideToRight(self):
        width = self.LeftSideMenu.width()
        if width <= 100 :
            self.btnHome.setText("Home")
            self.btnLiftLog.setText("Lift Log")
            self.btnTDEE.setText("TDEE Stats")
            self.btnLiftStats.setText("Lift Stats")
            self.btnLiftRecord.setText("Lift Record")
            self.btnStrengthStandard.setText("Strength Standard")
            self.btnAccount.setText("Account")
            self.btnSettings.setText("Settings")
            self.btnToPDF.setText("Export To PDF")
            self.btnToEmail.setText("Sent To Email")
            self.btnChangePsw.setText("Change Password")
            self.btnLogout.setText("Logout")
            newWidth = 225
        else:
            self.btnHome.setText("")
            self.btnLiftLog.setText("")
            self.btnTDEE.setText("")
            self.btnLiftStats.setText("")
            self.btnLiftRecord.setText("")
            self.btnStrengthStandard.setText("")
            self.btnAccount.setText("")
            self.btnSettings.setText("")
            self.btnToPDF.setText("")
            self.btnToEmail.setText("")
            self.btnChangePsw.setText("")
            self.btnLogout.setText("")
            newWidth = 50

        self.animation = QPropertyAnimation(self.LeftSideMenu, b"minimumWidth")
        self.animation.setDuration(500)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()

    def onClickBtnSettings(self):
        self.settingClick += 1
        if self.settingClick%2 == 0:
            self.btnLogout.setVisible(False)
            self.btnChangePsw.setVisible(False)
            self.btnToPDF.setVisible(False)
            self.btnToEmail.setVisible(False)
            self.slideToRight()
        else:
            self.btnLogout.setVisible(True)
            self.btnChangePsw.setVisible(True)
            self.btnToPDF.setVisible(True)
            self.btnToEmail.setVisible(True)
            self.slideToRight()

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
    
    def gotoAccount(self):
        acc = accountPage()
        widget.addWidget(acc)
        widget.setCurrentWidget(acc) 

    def gotoChangePsw(self):
        changePsw = changePswPageFromInside()
        widget.addWidget(changePsw)
        widget.setCurrentWidget(changePsw)

    def gotoLogin(self):
        login = loginPage()
        widget.addWidget(login)
        widget.setCurrentWidget(login)

    def gotoLiftLog(self):
        liftLog = liftLogPage()
        widget.addWidget(liftLog)
        widget.setCurrentWidget(liftLog)

    def gotoHome(self):
        home = homePage()
        widget.addWidget(home)
        widget.setCurrentWidget(home)

    def gotoDeadlift(self):
        deadlift = excDeadlift()
        widget.addWidget(deadlift)
        widget.setCurrentWidget(deadlift)

    def gotoFrontSquat(self):
        frontsquat = excFrontSquat()
        widget.addWidget(frontsquat)
        widget.setCurrentWidget(frontsquat)

class excFrontSquat(QMainWindow):
    def __init__(self):
        super(excFrontSquat, self).__init__()
        loadUi("frontsquat.ui", self)

        self.user = User(getLastSession())
        self.settingClick = 0
        self.initConnection()
        self.initNav()
        self.initUI()

    def initUI(self):
        pass

    def initConnection(self):
        self.btnToggle.clicked.connect(self.slideToRight)
        self.btnToPDF.clicked.connect(exportToPDF)
        self.btnToEmail.clicked.connect(sentToEmail)
        self.btnChangePsw.clicked.connect(self.gotoChangePsw)
        self.btnLogout.clicked.connect(self.gotoLogin)
        self.btnLiftLog.clicked.connect(self.gotoLiftLog)
        self.btnSettings.clicked.connect(self.onClickBtnSettings)
        self.btnBack.clicked.connect(self.gotoHome)
        self.btnPrev.clicked.connect(self.gotoBenchPress)
        self.btnNext.clicked.connect(self.gotoOverheadPress)

    def initNav(self):
        pxm0 = QPixmap("img/menuWhiteColor24Px.png")
        icon0 = QIcon(pxm0)
        pxm1 = QPixmap("img/homeWhiteColor24Px.png")
        icon1 = QIcon(pxm1)
        pxm2 = QPixmap("img/userWhiteColor24Px.png")
        icon2 = QIcon(pxm2)
        pxm3 = QPixmap("img/document.png")
        icon3 = QIcon(pxm3)
        pxm4 = QPixmap("img/analytics.png")
        icon4 = QIcon(pxm4)
        pxm5 = QPixmap("img/bar-chart.png")
        icon5 = QIcon(pxm5)
        pxm6 = QPixmap("img/list.png")
        icon6 = QIcon(pxm6)
        pxm7 = QPixmap("img/meal.png")
        icon7 = QIcon(pxm7)
        self.btnToggle.setIcon(icon0)
        self.btnHome.setIcon(icon1)
        self.btnLiftLog.setIcon(icon3)
        self.btnTDEE.setIcon(icon7)
        self.btnLiftStats.setIcon(icon4)
        self.btnLiftRecord.setIcon(icon6)
        self.btnStrengthStandard.setIcon(icon5)
        self.btnAccount.setIcon(icon2)
        pxm4 = QPixmap("img/Tulisan JournFit-01.png")
        self.appLogo.setPixmap(pxm4)
        pxm7 = QPixmap("img/logout.png")
        icon7 = QIcon(pxm7)
        self.btnLogout.setIcon(icon7)
        pxm8 = QPixmap("img/padlock.png")
        icon8 = QIcon(pxm8)
        self.btnChangePsw.setIcon(icon8)
        pxm9 = QPixmap("img/settingsWhiteColor24Px.png")
        icon9 = QIcon(pxm9)
        self.btnSettings.setIcon(icon9)
        pxm10 = QPixmap("img/pdf.png")
        icon10 = QIcon(pxm10)
        self.btnToPDF.setIcon(icon10)
        pxm11 = QPixmap("img/mail.png")
        icon11 = QIcon(pxm11)
        self.btnToEmail.setIcon(icon11)
        self.btnLogout.setVisible(False)
        self.btnChangePsw.setVisible(False)
        self.btnToPDF.setVisible(False)
        self.btnToEmail.setVisible(False)
        if self.user.image == "":
            pxmFoto = QPixmap("img/user.png")
            self.profileFoto.setPixmap(pxmFoto)
        else:
            pxmFoto = QPixmap(self.user.image)
            self.profileFoto.setPixmap(pxmFoto)

        self.btnToggle.setStyleSheet('*{text-align: center}')
        self.btnHome.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftLog.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(4, 155, 255); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnTDEE.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftStats.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftRecord.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnStrengthStandard.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnAccount.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.profileName.setStyleSheet('*{border-radius : 10px; color: rgb(255, 255, 255);}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnSettings.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnToPDF.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnToEmail.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnChangePsw.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLogout.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')

        self.btnHome.setText("")
        self.btnLiftLog.setText("")
        self.btnTDEE.setText("")
        self.btnLiftStats.setText("")
        self.btnLiftRecord.setText("")
        self.btnStrengthStandard.setText("")
        self.btnAccount.setText("")
        self.profileName.setText(self.user.name)
        self.btnSettings.setText("")
        self.btnToPDF.setText("")
        self.btnToEmail.setText("")
        self.btnChangePsw.setText("")
        self.btnLogout.setText("")

        #connection
        self.btnTDEE.clicked.connect(self.gotoTDEE)
        self.btnLiftStats.clicked.connect(self.gotoLiftStats)
        self.btnLiftRecord.clicked.connect(self.gotoLiftRecord)
        self.btnStrengthStandard.clicked.connect(self.gotoStrengthStandard)
        self.btnAccount.clicked.connect(self.gotoAccount)
        clickable(self.profileName).connect(self.gotoAccount)
        clickable(self.profileFoto).connect(self.gotoAccount)

    def slideToRight(self):
        width = self.LeftSideMenu.width()
        if width <= 100 :
            self.btnHome.setText("Home")
            self.btnLiftLog.setText("Lift Log")
            self.btnTDEE.setText("TDEE Stats")
            self.btnLiftStats.setText("Lift Stats")
            self.btnLiftRecord.setText("Lift Record")
            self.btnStrengthStandard.setText("Strength Standard")
            self.btnAccount.setText("Account")
            self.btnSettings.setText("Settings")
            self.btnToPDF.setText("Export To PDF")
            self.btnToEmail.setText("Sent To Email")
            self.btnChangePsw.setText("Change Password")
            self.btnLogout.setText("Logout")
            newWidth = 225
        else:
            self.btnHome.setText("")
            self.btnLiftLog.setText("")
            self.btnTDEE.setText("")
            self.btnLiftStats.setText("")
            self.btnLiftRecord.setText("")
            self.btnStrengthStandard.setText("")
            self.btnAccount.setText("")
            self.btnSettings.setText("")
            self.btnToPDF.setText("")
            self.btnToEmail.setText("")
            self.btnChangePsw.setText("")
            self.btnLogout.setText("")
            newWidth = 50

        self.animation = QPropertyAnimation(self.LeftSideMenu, b"minimumWidth")
        self.animation.setDuration(500)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()

    def onClickBtnSettings(self):
        self.settingClick += 1
        if self.settingClick%2 == 0:
            self.btnLogout.setVisible(False)
            self.btnChangePsw.setVisible(False)
            self.btnToPDF.setVisible(False)
            self.btnToEmail.setVisible(False)
            self.slideToRight()
        else:
            self.btnLogout.setVisible(True)
            self.btnChangePsw.setVisible(True)
            self.btnToPDF.setVisible(True)
            self.btnToEmail.setVisible(True)
            self.slideToRight()

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
    
    def gotoAccount(self):
        acc = accountPage()
        widget.addWidget(acc)
        widget.setCurrentWidget(acc) 

    def gotoChangePsw(self):
        changePsw = changePswPageFromInside()
        widget.addWidget(changePsw)
        widget.setCurrentWidget(changePsw)

    def gotoLogin(self):
        login = loginPage()
        widget.addWidget(login)
        widget.setCurrentWidget(login)

    def gotoLiftLog(self):
        liftLog = liftLogPage()
        widget.addWidget(liftLog)
        widget.setCurrentWidget(liftLog)

    def gotoHome(self):
        home = homePage()
        widget.addWidget(home)
        widget.setCurrentWidget(home)

    def gotoBenchPress(self):
        bp = excBenchPress()
        widget.addWidget(bp)
        widget.setCurrentWidget(bp)

    def gotoOverheadPress(self):
        ohp = excOverheadPress()
        widget.addWidget(ohp)
        widget.setCurrentWidget(ohp)

class excOverheadPress(QMainWindow):
    def __init__(self):
        super(excOverheadPress, self).__init__()
        loadUi("ohp.ui", self)

        self.user = User(getLastSession())
        self.settingClick = 0
        self.initConnection()
        self.initNav()
        self.initUI()

    def initUI(self):
        pass

    def initConnection(self):
        self.btnToggle.clicked.connect(self.slideToRight)
        self.btnToPDF.clicked.connect(exportToPDF)
        self.btnToEmail.clicked.connect(sentToEmail)
        self.btnChangePsw.clicked.connect(self.gotoChangePsw)
        self.btnLogout.clicked.connect(self.gotoLogin)
        self.btnLiftLog.clicked.connect(self.gotoLiftLog)
        self.btnSettings.clicked.connect(self.onClickBtnSettings)
        self.btnBack.clicked.connect(self.gotoHome)
        self.btnPrev.clicked.connect(self.gotoFrontSquat)
        self.btnNext.clicked.connect(self.gotoSumoDeadlift)

    def initNav(self):
        pxm0 = QPixmap("img/menuWhiteColor24Px.png")
        icon0 = QIcon(pxm0)
        pxm1 = QPixmap("img/homeWhiteColor24Px.png")
        icon1 = QIcon(pxm1)
        pxm2 = QPixmap("img/userWhiteColor24Px.png")
        icon2 = QIcon(pxm2)
        pxm3 = QPixmap("img/document.png")
        icon3 = QIcon(pxm3)
        pxm4 = QPixmap("img/analytics.png")
        icon4 = QIcon(pxm4)
        pxm5 = QPixmap("img/bar-chart.png")
        icon5 = QIcon(pxm5)
        pxm6 = QPixmap("img/list.png")
        icon6 = QIcon(pxm6)
        pxm7 = QPixmap("img/meal.png")
        icon7 = QIcon(pxm7)
        self.btnToggle.setIcon(icon0)
        self.btnHome.setIcon(icon1)
        self.btnLiftLog.setIcon(icon3)
        self.btnTDEE.setIcon(icon7)
        self.btnLiftStats.setIcon(icon4)
        self.btnLiftRecord.setIcon(icon6)
        self.btnStrengthStandard.setIcon(icon5)
        self.btnAccount.setIcon(icon2)
        pxm4 = QPixmap("img/Tulisan JournFit-01.png")
        self.appLogo.setPixmap(pxm4)
        pxm7 = QPixmap("img/logout.png")
        icon7 = QIcon(pxm7)
        self.btnLogout.setIcon(icon7)
        pxm8 = QPixmap("img/padlock.png")
        icon8 = QIcon(pxm8)
        self.btnChangePsw.setIcon(icon8)
        pxm9 = QPixmap("img/settingsWhiteColor24Px.png")
        icon9 = QIcon(pxm9)
        self.btnSettings.setIcon(icon9)
        pxm10 = QPixmap("img/pdf.png")
        icon10 = QIcon(pxm10)
        self.btnToPDF.setIcon(icon10)
        pxm11 = QPixmap("img/mail.png")
        icon11 = QIcon(pxm11)
        self.btnToEmail.setIcon(icon11)
        self.btnLogout.setVisible(False)
        self.btnChangePsw.setVisible(False)
        self.btnToPDF.setVisible(False)
        self.btnToEmail.setVisible(False)
        if self.user.image == "":
            pxmFoto = QPixmap("img/user.png")
            self.profileFoto.setPixmap(pxmFoto)
        else:
            pxmFoto = QPixmap(self.user.image)
            self.profileFoto.setPixmap(pxmFoto)

        self.btnToggle.setStyleSheet('*{text-align: center}')
        self.btnHome.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftLog.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(4, 155, 255); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnTDEE.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftStats.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftRecord.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnStrengthStandard.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnAccount.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.profileName.setStyleSheet('*{border-radius : 10px; color: rgb(255, 255, 255);}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnSettings.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnToPDF.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnToEmail.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnChangePsw.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLogout.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')

        self.btnHome.setText("")
        self.btnLiftLog.setText("")
        self.btnTDEE.setText("")
        self.btnLiftStats.setText("")
        self.btnLiftRecord.setText("")
        self.btnStrengthStandard.setText("")
        self.btnAccount.setText("")
        self.profileName.setText(self.user.name)
        self.btnSettings.setText("")
        self.btnToPDF.setText("")
        self.btnToEmail.setText("")
        self.btnChangePsw.setText("")
        self.btnLogout.setText("")

        #connection
        self.btnTDEE.clicked.connect(self.gotoTDEE)
        self.btnLiftStats.clicked.connect(self.gotoLiftStats)
        self.btnLiftRecord.clicked.connect(self.gotoLiftRecord)
        self.btnStrengthStandard.clicked.connect(self.gotoStrengthStandard)
        self.btnAccount.clicked.connect(self.gotoAccount)
        clickable(self.profileName).connect(self.gotoAccount)
        clickable(self.profileFoto).connect(self.gotoAccount)

    def slideToRight(self):
        width = self.LeftSideMenu.width()
        if width <= 100 :
            self.btnHome.setText("Home")
            self.btnLiftLog.setText("Lift Log")
            self.btnTDEE.setText("TDEE Stats")
            self.btnLiftStats.setText("Lift Stats")
            self.btnLiftRecord.setText("Lift Record")
            self.btnStrengthStandard.setText("Strength Standard")
            self.btnAccount.setText("Account")
            self.btnSettings.setText("Settings")
            self.btnToPDF.setText("Export To PDF")
            self.btnToEmail.setText("Sent To Email")
            self.btnChangePsw.setText("Change Password")
            self.btnLogout.setText("Logout")
            newWidth = 225
        else:
            self.btnHome.setText("")
            self.btnLiftLog.setText("")
            self.btnTDEE.setText("")
            self.btnLiftStats.setText("")
            self.btnLiftRecord.setText("")
            self.btnStrengthStandard.setText("")
            self.btnAccount.setText("")
            self.btnSettings.setText("")
            self.btnToPDF.setText("")
            self.btnToEmail.setText("")
            self.btnChangePsw.setText("")
            self.btnLogout.setText("")
            newWidth = 50

        self.animation = QPropertyAnimation(self.LeftSideMenu, b"minimumWidth")
        self.animation.setDuration(500)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()

    def onClickBtnSettings(self):
        self.settingClick += 1
        if self.settingClick%2 == 0:
            self.btnLogout.setVisible(False)
            self.btnChangePsw.setVisible(False)
            self.btnToPDF.setVisible(False)
            self.btnToEmail.setVisible(False)
            self.slideToRight()
        else:
            self.btnLogout.setVisible(True)
            self.btnChangePsw.setVisible(True)
            self.btnToPDF.setVisible(True)
            self.btnToEmail.setVisible(True)
            self.slideToRight()

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
    
    def gotoAccount(self):
        acc = accountPage()
        widget.addWidget(acc)
        widget.setCurrentWidget(acc) 

    def gotoChangePsw(self):
        changePsw = changePswPageFromInside()
        widget.addWidget(changePsw)
        widget.setCurrentWidget(changePsw)

    def gotoLogin(self):
        login = loginPage()
        widget.addWidget(login)
        widget.setCurrentWidget(login)

    def gotoLiftLog(self):
        liftLog = liftLogPage()
        widget.addWidget(liftLog)
        widget.setCurrentWidget(liftLog)

    def gotoHome(self):
        home = homePage()
        widget.addWidget(home)
        widget.setCurrentWidget(home)

    def gotoFrontSquat(self):
        fs = excFrontSquat()
        widget.addWidget(fs)
        widget.setCurrentWidget(fs)

    def gotoSumoDeadlift(self):
        sdl = excSumoDeadlift()
        widget.addWidget(sdl)
        widget.setCurrentWidget(sdl)

class excSumoDeadlift(QMainWindow):
    def __init__(self):
        super(excSumoDeadlift, self).__init__()
        loadUi("sdl.ui", self)

        self.user = User(getLastSession())
        self.settingClick = 0
        self.initConnection()
        self.initNav()
        self.initUI()

    def initUI(self):
        pass

    def initConnection(self):
        self.btnToggle.clicked.connect(self.slideToRight)
        self.btnToPDF.clicked.connect(exportToPDF)
        self.btnToEmail.clicked.connect(sentToEmail)
        self.btnChangePsw.clicked.connect(self.gotoChangePsw)
        self.btnLogout.clicked.connect(self.gotoLogin)
        self.btnLiftLog.clicked.connect(self.gotoLiftLog)
        self.btnSettings.clicked.connect(self.onClickBtnSettings)
        self.btnBack.clicked.connect(self.gotoHome)
        self.btnPrev.clicked.connect(self.gotoOverheadPress)
        self.btnNext.clicked.connect(self.gotoLatPulldown)

    def initNav(self):
        pxm0 = QPixmap("img/menuWhiteColor24Px.png")
        icon0 = QIcon(pxm0)
        pxm1 = QPixmap("img/homeWhiteColor24Px.png")
        icon1 = QIcon(pxm1)
        pxm2 = QPixmap("img/userWhiteColor24Px.png")
        icon2 = QIcon(pxm2)
        pxm3 = QPixmap("img/document.png")
        icon3 = QIcon(pxm3)
        pxm4 = QPixmap("img/analytics.png")
        icon4 = QIcon(pxm4)
        pxm5 = QPixmap("img/bar-chart.png")
        icon5 = QIcon(pxm5)
        pxm6 = QPixmap("img/list.png")
        icon6 = QIcon(pxm6)
        pxm7 = QPixmap("img/meal.png")
        icon7 = QIcon(pxm7)
        self.btnToggle.setIcon(icon0)
        self.btnHome.setIcon(icon1)
        self.btnLiftLog.setIcon(icon3)
        self.btnTDEE.setIcon(icon7)
        self.btnLiftStats.setIcon(icon4)
        self.btnLiftRecord.setIcon(icon6)
        self.btnStrengthStandard.setIcon(icon5)
        self.btnAccount.setIcon(icon2)
        pxm4 = QPixmap("img/Tulisan JournFit-01.png")
        self.appLogo.setPixmap(pxm4)
        pxm7 = QPixmap("img/logout.png")
        icon7 = QIcon(pxm7)
        self.btnLogout.setIcon(icon7)
        pxm8 = QPixmap("img/padlock.png")
        icon8 = QIcon(pxm8)
        self.btnChangePsw.setIcon(icon8)
        pxm9 = QPixmap("img/settingsWhiteColor24Px.png")
        icon9 = QIcon(pxm9)
        self.btnSettings.setIcon(icon9)
        pxm10 = QPixmap("img/pdf.png")
        icon10 = QIcon(pxm10)
        self.btnToPDF.setIcon(icon10)
        pxm11 = QPixmap("img/mail.png")
        icon11 = QIcon(pxm11)
        self.btnToEmail.setIcon(icon11)
        self.btnLogout.setVisible(False)
        self.btnChangePsw.setVisible(False)
        self.btnToPDF.setVisible(False)
        self.btnToEmail.setVisible(False)
        if self.user.image == "":
            pxmFoto = QPixmap("img/user.png")
            self.profileFoto.setPixmap(pxmFoto)
        else:
            pxmFoto = QPixmap(self.user.image)
            self.profileFoto.setPixmap(pxmFoto)

        self.btnToggle.setStyleSheet('*{text-align: center}')
        self.btnHome.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftLog.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(4, 155, 255); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnTDEE.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftStats.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftRecord.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnStrengthStandard.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnAccount.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.profileName.setStyleSheet('*{border-radius : 10px; color: rgb(255, 255, 255);}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnSettings.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnToPDF.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnToEmail.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnChangePsw.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLogout.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')

        self.btnHome.setText("")
        self.btnLiftLog.setText("")
        self.btnTDEE.setText("")
        self.btnLiftStats.setText("")
        self.btnLiftRecord.setText("")
        self.btnStrengthStandard.setText("")
        self.btnAccount.setText("")
        self.profileName.setText(self.user.name)
        self.btnSettings.setText("")
        self.btnToPDF.setText("")
        self.btnToEmail.setText("")
        self.btnChangePsw.setText("")
        self.btnLogout.setText("")

        #connection
        self.btnTDEE.clicked.connect(self.gotoTDEE)
        self.btnLiftStats.clicked.connect(self.gotoLiftStats)
        self.btnLiftRecord.clicked.connect(self.gotoLiftRecord)
        self.btnStrengthStandard.clicked.connect(self.gotoStrengthStandard)
        self.btnAccount.clicked.connect(self.gotoAccount)
        clickable(self.profileName).connect(self.gotoAccount)
        clickable(self.profileFoto).connect(self.gotoAccount)

    def slideToRight(self):
        width = self.LeftSideMenu.width()
        if width <= 100 :
            self.btnHome.setText("Home")
            self.btnLiftLog.setText("Lift Log")
            self.btnTDEE.setText("TDEE Stats")
            self.btnLiftStats.setText("Lift Stats")
            self.btnLiftRecord.setText("Lift Record")
            self.btnStrengthStandard.setText("Strength Standard")
            self.btnAccount.setText("Account")
            self.btnSettings.setText("Settings")
            self.btnToPDF.setText("Export To PDF")
            self.btnToEmail.setText("Sent To Email")
            self.btnChangePsw.setText("Change Password")
            self.btnLogout.setText("Logout")
            newWidth = 225
        else:
            self.btnHome.setText("")
            self.btnLiftLog.setText("")
            self.btnTDEE.setText("")
            self.btnLiftStats.setText("")
            self.btnLiftRecord.setText("")
            self.btnStrengthStandard.setText("")
            self.btnAccount.setText("")
            self.btnSettings.setText("")
            self.btnToPDF.setText("")
            self.btnToEmail.setText("")
            self.btnChangePsw.setText("")
            self.btnLogout.setText("")
            newWidth = 50

        self.animation = QPropertyAnimation(self.LeftSideMenu, b"minimumWidth")
        self.animation.setDuration(500)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()

    def onClickBtnSettings(self):
        self.settingClick += 1
        if self.settingClick%2 == 0:
            self.btnLogout.setVisible(False)
            self.btnChangePsw.setVisible(False)
            self.btnToPDF.setVisible(False)
            self.btnToEmail.setVisible(False)
            self.slideToRight()
        else:
            self.btnLogout.setVisible(True)
            self.btnChangePsw.setVisible(True)
            self.btnToPDF.setVisible(True)
            self.btnToEmail.setVisible(True)
            self.slideToRight()

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
    
    def gotoAccount(self):
        acc = accountPage()
        widget.addWidget(acc)
        widget.setCurrentWidget(acc) 

    def gotoChangePsw(self):
        changePsw = changePswPageFromInside()
        widget.addWidget(changePsw)
        widget.setCurrentWidget(changePsw)

    def gotoLogin(self):
        login = loginPage()
        widget.addWidget(login)
        widget.setCurrentWidget(login)

    def gotoLiftLog(self):
        liftLog = liftLogPage()
        widget.addWidget(liftLog)
        widget.setCurrentWidget(liftLog)

    def gotoHome(self):
        home = homePage()
        widget.addWidget(home)
        widget.setCurrentWidget(home)

    def gotoOverheadPress(self):
        ohp = excOverheadPress()
        widget.addWidget(ohp)
        widget.setCurrentWidget(ohp)

    def gotoLatPulldown(self):
        lp = excLatPulldown()
        widget.addWidget(lp)
        widget.setCurrentWidget(lp)

class liftLogPage(QMainWindow):
    def __init__(self):
        super(liftLogPage, self).__init__()
        loadUi("LiftLog.ui", self)

        self.today = QDate.currentDate().addDays(0)
        self.dateSelect = self.today
        self.toggleEdit = 0
        self.mediaClick = 0
        self.settingClick = 0
        self.user = User(getLastSession())

        self.initUI()
        self.initNav()
        self.initCalendar()
        self.initConnection()
        self.onClickCalendar()
        
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
        self.btnSettings.clicked.connect(self.onClickBtnSettings)
        self.btnToPDF.clicked.connect(exportToPDF)
        self.btnToEmail.clicked.connect(sentToEmail)
        self.btnMediaOption.clicked.connect(self.onClickMediaOption)
        self.btnChangePsw.clicked.connect(self.gotoChangePsw)
        self.btnLogout.clicked.connect(self.gotoLogin)
        self.btnHome.clicked.connect(self.gotoHome)

        #media connection all 36 of them
        self.btnMediaE1S1.clicked.connect(self.onClickBtnMediaE1S1)
        self.btnMediaE1S2.clicked.connect(self.onClickBtnMediaE1S2)
        self.btnMediaE1S3.clicked.connect(self.onClickBtnMediaE1S3)
        self.btnMediaE1S4.clicked.connect(self.onClickBtnMediaE1S4)
        self.btnMediaE1S5.clicked.connect(self.onClickBtnMediaE1S5)
        self.btnMediaE1S6.clicked.connect(self.onClickBtnMediaE1S6)

    def gotoChangePsw(self):
        changePsw = changePswPageFromInside()
        widget.addWidget(changePsw)
        widget.setCurrentWidget(changePsw)

    def gotoLogin(self):
        login = loginPage()
        widget.addWidget(login)
        widget.setCurrentWidget(login)

    def gotoHome(self):
        home = homePage()
        widget.addWidget(home)
        widget.setCurrentWidget(home)

    def initCalendar(self):
        self.calendarWidget.setSelectedDate(self.today)
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
        
        for date in self.qtDateFromStringPlan():
            if self.today.daysTo(date) > 0:
                format = QTextCharFormat()
                format.setFontUnderline(True)
                format.setFontWeight(10)
                format.setUnderlineColor(QColor.fromRgb(0,0,0,50))
                format.setBackground(QColor.fromRgb(98,145,255))
                self.calendarWidget.setDateTextFormat(date,format)

        for date in self.qtDateFromString():
            format = QTextCharFormat()
            format.setFontUnderline(True)
            format.setFontWeight(10)
            format.setUnderlineColor(QColor.fromRgb(0,0,0,50))
            format.setBackground(QColor.fromRgb(136,216,199))
            self.calendarWidget.setDateTextFormat(date,format)

    def initNav(self):
        pxm0 = QPixmap("img/menuWhiteColor24Px.png")
        icon0 = QIcon(pxm0)
        pxm1 = QPixmap("img/homeWhiteColor24Px.png")
        icon1 = QIcon(pxm1)
        pxm2 = QPixmap("img/userWhiteColor24Px.png")
        icon2 = QIcon(pxm2)
        pxm3 = QPixmap("img/document.png")
        icon3 = QIcon(pxm3)
        pxm4 = QPixmap("img/analytics.png")
        icon4 = QIcon(pxm4)
        pxm5 = QPixmap("img/bar-chart.png")
        icon5 = QIcon(pxm5)
        pxm6 = QPixmap("img/list.png")
        icon6 = QIcon(pxm6)
        pxm7 = QPixmap("img/meal.png")
        icon7 = QIcon(pxm7)
        self.btnToggle.setIcon(icon0)
        self.btnHome.setIcon(icon1)
        self.btnLiftLog.setIcon(icon3)
        self.btnTDEE.setIcon(icon7)
        self.btnLiftStats.setIcon(icon4)
        self.btnLiftRecord.setIcon(icon6)
        self.btnStrengthStandard.setIcon(icon5)
        self.btnAccount.setIcon(icon2)
        pxm4 = QPixmap("img/Tulisan JournFit-01.png")
        self.appLogo.setPixmap(pxm4)
        pxm7 = QPixmap("img/logout.png")
        icon7 = QIcon(pxm7)
        self.btnLogout.setIcon(icon7)
        pxm8 = QPixmap("img/padlock.png")
        icon8 = QIcon(pxm8)
        self.btnChangePsw.setIcon(icon8)
        pxm9 = QPixmap("img/settingsWhiteColor24Px.png")
        icon9 = QIcon(pxm9)
        self.btnSettings.setIcon(icon9)
        pxm10 = QPixmap("img/pdf.png")
        icon10 = QIcon(pxm10)
        self.btnToPDF.setIcon(icon10)
        pxm11 = QPixmap("img/mail.png")
        icon11 = QIcon(pxm11)
        self.btnToEmail.setIcon(icon11)
        self.btnLogout.setVisible(False)
        self.btnChangePsw.setVisible(False)
        self.btnToPDF.setVisible(False)
        self.btnToEmail.setVisible(False)
        if self.user.image == "":
            pxmFoto = QPixmap("img/user.png")
            self.profileFoto.setPixmap(pxmFoto)
        else:
            pxmFoto = QPixmap(self.user.image)
            self.profileFoto.setPixmap(pxmFoto)

        self.btnToggle.setStyleSheet('*{text-align: center}')
        self.btnHome.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftLog.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(4, 155, 255); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnTDEE.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftStats.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftRecord.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnStrengthStandard.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnAccount.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.profileName.setStyleSheet('*{border-radius : 10px; color: rgb(255, 255, 255);}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnSettings.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnToPDF.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnToEmail.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnChangePsw.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLogout.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')

        self.btnHome.setText("")
        self.btnLiftLog.setText("")
        self.btnTDEE.setText("")
        self.btnLiftStats.setText("")
        self.btnLiftRecord.setText("")
        self.btnStrengthStandard.setText("")
        self.btnAccount.setText("")
        self.profileName.setText(self.user.name)
        self.btnSettings.setText("")
        self.btnToPDF.setText("")
        self.btnToEmail.setText("")
        self.btnChangePsw.setText("")
        self.btnLogout.setText("")

        #connection
        self.btnTDEE.clicked.connect(self.gotoTDEE)
        self.btnLiftStats.clicked.connect(self.gotoLiftStats)
        self.btnLiftRecord.clicked.connect(self.gotoLiftRecord)
        self.btnStrengthStandard.clicked.connect(self.gotoStrengthStandard)
        self.btnAccount.clicked.connect(self.gotoAccount)
        clickable(self.profileName).connect(self.gotoAccount)
        clickable(self.profileFoto).connect(self.gotoAccount)

    def slideToRight(self):
        width = self.LeftSideMenu.width()
        if width <= 100 :
            self.btnHome.setText("Home")
            self.btnLiftLog.setText("Lift Log")
            self.btnTDEE.setText("TDEE Stats")
            self.btnLiftStats.setText("Lift Stats")
            self.btnLiftRecord.setText("Lift Record")
            self.btnStrengthStandard.setText("Strength Standard")
            self.btnAccount.setText("Account")
            self.btnSettings.setText("Settings")
            self.btnToPDF.setText("Export To PDF")
            self.btnToEmail.setText("Sent To Email")
            self.btnChangePsw.setText("Change Password")
            self.btnLogout.setText("Logout")
            newWidth = 225
        else:
            self.btnHome.setText("")
            self.btnLiftLog.setText("")
            self.btnTDEE.setText("")
            self.btnLiftStats.setText("")
            self.btnLiftRecord.setText("")
            self.btnStrengthStandard.setText("")
            self.btnAccount.setText("")
            self.btnSettings.setText("")
            self.btnToPDF.setText("")
            self.btnToEmail.setText("")
            self.btnChangePsw.setText("")
            self.btnLogout.setText("")
            newWidth = 50

        self.animation = QPropertyAnimation(self.LeftSideMenu, b"minimumWidth")
        self.animation.setDuration(500)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()

    def onClickBtnSettings(self):
        self.settingClick += 1
        if self.settingClick%2 == 0:
            self.btnLogout.setVisible(False)
            self.btnChangePsw.setVisible(False)
            self.btnToPDF.setVisible(False)
            self.btnToEmail.setVisible(False)
            self.slideToRight()
        else:
            self.btnLogout.setVisible(True)
            self.btnChangePsw.setVisible(True)
            self.btnToPDF.setVisible(True)
            self.btnToEmail.setVisible(True)
            self.slideToRight()

    def qtDateFromString(self):
        dateList = returnDateLogin(getLastSession())
        qtDate = [QDate.fromString(d, "yyyy-MM-dd") for d in dateList]
        return qtDate

    def qtDateFromStringPlan(self):
        dateList = returnDatePlan(getLastSession())
        qtDate = [QDate.fromString(d, "yyyy-MM-dd") for d in dateList]
        return qtDate

    def onClickCalendar(self):
        btnList = [self.btnSubmitE1,self.btnSubmitE2,self.btnSubmitE3,self.btnSubmitE4,self.btnSubmitE5,self.btnSubmitE6]
        date = self.calendarWidget.selectedDate()
        self.dateSelect = date
        user = self.user
        # == 0 need attention
        if self.today.daysTo(date) < 0 : #change <= later
            self.styleRecord()
            result = user.showRecordOn(f'{date.year()}-{date.month()}-{date.day()}')
        elif self.today.daysTo(date) > 0 :
            self.stylePlan()
            result = user.showPlanOn(f'{date.year()}-{date.month()}-{date.day()}')
        else:
            if date in self.qtDateFromString() and date in self.qtDateFromStringPlan():
                result = user.showRecordOn(f'{date.year()}-{date.month()}-{date.day()}')
                #result += user.showPlanOn(f'{date.year()}-{date.month()}-{date.day()}')
            elif date in self.qtDateFromString():
                self.styleRecord()
                result = user.showRecordOn(f'{date.year()}-{date.month()}-{date.day()}')
            elif date in self.qtDateFromStringPlan():
                self.stylePlan()
                result = user.showPlanOn(f'{date.year()}-{date.month()}-{date.day()}')
            else: #inspect later
                result = user.showRecordOn(f'{date.year()}-{date.month()}-{date.day()}')
        
        self.clearView()
        self.writeToTable(result)
        self.btnToggleEdit.setStyleSheet('QPushButton {background-color: rgb(255, 201, 66);}')
        self.btnToggleEdit.setText("Toggle Edit Mode")
        self.toggleEdit = 0
        for btn in btnList:
            btn.setStyleSheet('QPushButton {background-color: rgb(85, 170, 0);}')
            btn.setText("Submit")
        if self.today.daysTo(date) < 0: #if past days
            self.disableData()
            self.btnToggleEdit.setEnabled(True)
        elif date in self.qtDateFromStringPlan() and date != self.today:
            self.disableData()
            self.btnToggleEdit.setEnabled(True)
        else:   # if days ahead
            self.enableData()
            self.btnToggleEdit.setEnabled(False)

        if self.today.daysTo(date) == 0 : 
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
                self.submitDateRow(1,getLastSession())
                if(firstRow[0].text() != " "):
                    self.cmbExcercise1.setEnabled(False)
                    for obj in firstRow + firstSp:
                        obj.setReadOnly(True)
                self.cmbExcercise1.setStyleSheet('*{color: rgb(0,0,0);}')
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
                self.submitDateRow(2,getLastSession())
                if(secondRow[0].text() != " "):
                    self.cmbExcercise2.setEnabled(False)
                    for obj in secondRow + secondSp:
                        obj.setReadOnly(True)
                self.cmbExcercise2.setStyleSheet('*{color: rgb(0,0,0);}')
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
                self.submitDateRow(3,getLastSession())
                if(thirdRow[0].text() != " "):
                    self.cmbExcercise3.setEnabled(False)
                    for obj in thirdRow + thirdSp:
                        obj.setReadOnly(True)
                self.cmbExcercise3.setStyleSheet('*{color: rgb(0,0,0);}')
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
                self.submitDateRow(4,getLastSession())
                if(fourthRow[0].text() != " "):
                    self.cmbExcercise4.setEnabled(False)
                    for obj in fourthRow + fourthSp:
                        obj.setReadOnly(True)
                self.cmbExcercise4.setStyleSheet('*{color: rgb(0,0,0);}')
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
                self.submitDateRow(5,getLastSession())
                if(fifthRow[0].text() != " "):
                    self.cmbExcercise5.setEnabled(False)
                    for obj in fifthRow + fifthSp:
                        obj.setReadOnly(True)
                self.cmbExcercise5.setStyleSheet('*{color: rgb(0,0,0);}')
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
                self.submitDateRow(6,getLastSession())
                if(sixthRow[0].text() != " "):
                    self.cmbExcercise6.setEnabled(False)
                    for obj in sixthRow + sixthSp:
                        obj.setReadOnly(True)
                self.cmbExcercise6.setStyleSheet('*{color: rgb(0,0,0);}')
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

    def onClickMediaOption(self):
        firstMedia = [self.btnMediaE1S1,self.btnMediaE1S2,self.btnMediaE1S3,self.btnMediaE1S4,self.btnMediaE1S5,self.btnMediaE1S6]
        secondMedia = [self.btnMediaE2S1,self.btnMediaE2S2,self.btnMediaE2S3,self.btnMediaE2S4,self.btnMediaE2S5,self.btnMediaE2S6]
        thirdMedia = [self.btnMediaE3S1,self.btnMediaE3S2,self.btnMediaE3S3,self.btnMediaE3S4,self.btnMediaE3S5,self.btnMediaE3S6]
        fourthMedia = [self.btnMediaE4S1,self.btnMediaE4S2,self.btnMediaE4S3,self.btnMediaE4S4,self.btnMediaE4S5,self.btnMediaE4S6]
        fifthMedia = [self.btnMediaE5S1,self.btnMediaE5S2,self.btnMediaE5S3,self.btnMediaE5S4,self.btnMediaE5S5,self.btnMediaE5S6]
        sixthMedia = [self.btnMediaE6S1,self.btnMediaE6S2,self.btnMediaE6S3,self.btnMediaE6S4,self.btnMediaE6S5,self.btnMediaE6S6]
        if self.mediaClick%2 == 0:
            for btn in firstMedia + secondMedia + thirdMedia + fourthMedia + fifthMedia + sixthMedia:
                btn.setVisible(True)
        else:
            for btn in firstMedia + secondMedia + thirdMedia + fourthMedia + fifthMedia + sixthMedia:
                btn.setVisible(False)

        firstHidden = [self.hiddenE1S1,self.hiddenE1S2,self.hiddenE1S3,self.hiddenE1S4,self.hiddenE1S5,self.hiddenE1S6]
        secondHidden = [self.hiddenE2S1,self.hiddenE2S2,self.hiddenE2S3,self.hiddenE2S4,self.hiddenE2S5,self.hiddenE2S6]
        thirdHidden = [self.hiddenE3S1,self.hiddenE3S2,self.hiddenE3S3,self.hiddenE3S4,self.hiddenE3S5,self.hiddenE3S6]
        fourthHidden = [self.hiddenE4S1,self.hiddenE4S2,self.hiddenE4S3,self.hiddenE4S4,self.hiddenE4S5,self.hiddenE4S6]
        fifthHidden = [self.hiddenE5S1,self.hiddenE5S2,self.hiddenE5S3,self.hiddenE5S4,self.hiddenE5S5,self.hiddenE5S6]
        sixthHidden = [self.hiddenE6S1,self.hiddenE6S2,self.hiddenE6S3,self.hiddenE6S4,self.hiddenE6S5,self.hiddenE6S6]

        for i in range(0,6):
            try:
                if len(Lift(firstHidden[i].text()).media) > 0:
                    firstMedia[i].setText("Play")
                    firstMedia[i].setStyleSheet('QPushButton {background-color: rgb(255, 201, 66);}')
                    print(f'IN {i}')
                else:
                    firstMedia[i].setText("Add Media")
                    firstMedia[i].setStyleSheet('QPushButton {background-color: rgb(0, 170, 0);}')
                    print(f'OUT {i}')
            except:
                pass
        self.mediaClick += 1

    def onClickBtnMediaE1S1(self):
        if self.btnMediaE1S1.text() == "Play":
            video = Lift(self.hiddenE1S1.text()).media
            #self.showVideoOf("D:/Progress/BP 20201023 80X1.mp4")
            self.showVideoOf(video)

        else:
            file = dialog()
            file.openFileNameDialog()
            id = self.hiddenE1S1.text()
            lift = Lift(id)
            lift.insertMedia(file.file)
            
            self.btnMediaE1S1.setText("Play")
            self.btnMediaE1S1.setStyleSheet('QPushButton {background-color: rgb(255, 201, 66);}')

    def onClickBtnMediaE1S2(self):
        if self.btnMediaE1S2.text() == "Play":
            video = Lift(self.hiddenE1S2.text()).media
            #self.showVideoOf("D:/Progress/BP 20201023 80X1.mp4")
            self.showVideoOf(video)

        else:
            file = dialog()
            file.openFileNameDialog()
            id = self.hiddenE1S2.text()
            lift = Lift(id)
            lift.insertMedia(file.file)
            
            self.btnMediaE1S2.setText("Play")
            self.btnMediaE1S2.setStyleSheet('QPushButton {background-color: rgb(255, 201, 66);}')

    def onClickBtnMediaE1S3(self):
        if self.btnMediaE1S3.text() == "Play":
            video = Lift(self.hiddenE1S3.text()).media
            #self.showVideoOf("D:/Progress/BP 20201023 80X1.mp4")
            self.showVideoOf(video)

        else:
            file = dialog()
            file.openFileNameDialog()
            id = self.hiddenE1S3.text()
            lift = Lift(id)
            lift.insertMedia(file.file)
            
            self.btnMediaE1S3.setText("Play")
            self.btnMediaE1S3.setStyleSheet('QPushButton {background-color: rgb(255, 201, 66);}')

    def onClickBtnMediaE1S4(self):
        if self.btnMediaE1S4.text() == "Play":
            video = Lift(self.hiddenE1S4.text()).media
            #self.showVideoOf("D:/Progress/BP 20201023 80X1.mp4")
            self.showVideoOf(video)

        else:
            file = dialog()
            file.openFileNameDialog()
            id = self.hiddenE1S4.text()
            lift = Lift(id)
            lift.insertMedia(file.file)
            
            self.btnMediaE1S4.setText("Play")
            self.btnMediaE1S4.setStyleSheet('QPushButton {background-color: rgb(255, 201, 66);}')

    def onClickBtnMediaE1S5(self):
        if self.btnMediaE1S5.text() == "Play":
            video = Lift(self.hiddenE1S5.text()).media
            #self.showVideoOf("D:/Progress/BP 20201023 80X1.mp4")
            self.showVideoOf(video)

        else:
            file = dialog()
            file.openFileNameDialog()
            id = self.hiddenE1S5.text()
            lift = Lift(id)
            lift.insertMedia(file.file)
            
            self.btnMediaE1S5.setText("Play")
            self.btnMediaE1S5.setStyleSheet('QPushButton {background-color: rgb(255, 201, 66);}')

    def onClickBtnMediaE1S6(self):
        if self.btnMediaE1S6.text() == "Play":
            video = Lift(self.hiddenE1S6.text()).media
            #self.showVideoOf("D:/Progress/BP 20201023 80X1.mp4")
            self.showVideoOf(video)

        else:
            file = dialog()
            file.openFileNameDialog()
            id = self.hiddenE1S6.text()
            lift = Lift(id)
            lift.insertMedia(file.file)
            
            self.btnMediaE1S6.setText("Play")
            self.btnMediaE1S6.setStyleSheet('QPushButton {background-color: rgb(255, 201, 66);}')



    def showPopUp(self,message):
        msg = QMessageBox()
        msg.setWindowTitle("JournFit")
        msg.setText(message)
        msg.Icon(QMessageBox.Information)
        msg.StandardButton(QMessageBox.Ok|QMessageBox.Open)
        msg.setStyleSheet("QLabel{font-size: 20px; text-align: center;} QPushButton{ width:75px; font-size: 10px; }");
        x = msg.exec_()

    def showVideoOf(self, video):
        class VideoWindow(QMainWindow):

            def __init__(self, parent=None):
                super(VideoWindow, self).__init__(parent)
                self.setWindowTitle("JournFit") 

                self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

                videoWidget = QVideoWidget()

                self.playButton = QPushButton()
                self.playButton.setEnabled(False)
                self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
                self.playButton.clicked.connect(self.play)

                self.positionSlider = QSlider(Qt.Horizontal)
                self.positionSlider.setRange(0, 0)
                self.positionSlider.sliderMoved.connect(self.setPosition)

                self.errorLabel = QLabel()
                self.errorLabel.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Maximum)
                
                # Create exit action
                exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
                exitAction.setShortcut('Ctrl+Q')
                exitAction.setStatusTip('Exit application')
                exitAction.triggered.connect(self.exitCall)
                
                # Create a widget for window contents
                wid = QWidget(self)
                self.setCentralWidget(wid)

                # Create layouts to place inside widget
                controlLayout = QHBoxLayout()
                controlLayout.setContentsMargins(0, 0, 0, 0)
                controlLayout.addWidget(self.playButton)
                controlLayout.addWidget(self.positionSlider)

                layout = QVBoxLayout()
                layout.addWidget(videoWidget)
                layout.addLayout(controlLayout)
                layout.addWidget(self.errorLabel)

                # Set widget to contain window contents
                wid.setLayout(layout)

                self.mediaPlayer.setVideoOutput(videoWidget)
                self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
                self.mediaPlayer.positionChanged.connect(self.positionChanged)
                self.mediaPlayer.durationChanged.connect(self.durationChanged)
                self.mediaPlayer.error.connect(self.handleError)
                
                #fileName = "D:/Progress/BP 20201023 80X1.mp4"
                self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(video)))
                self.playButton.setEnabled(True)

            def exitCall(self):
                sys.exit(app.exec_())

            def play(self):
                if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
                    self.mediaPlayer.pause()
                else:
                    self.mediaPlayer.play()

            def mediaStateChanged(self, state):
                if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
                    self.playButton.setIcon(
                            self.style().standardIcon(QStyle.SP_MediaPause))
                else:
                    self.playButton.setIcon(
                            self.style().standardIcon(QStyle.SP_MediaPlay))

            def positionChanged(self, position):
                self.positionSlider.setValue(position)

            def durationChanged(self, duration):
                self.positionSlider.setRange(0, duration)

            def setPosition(self, position):
                self.mediaPlayer.setPosition(position)

            def handleError(self):
                self.playButton.setEnabled(False)
                self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())

        loop = QEventLoop() 
        video = VideoWindow()
        video.resize(640, 480)
        video.show()
        loop.exec()

        #app = QApplication(sys.argv)
        #videoplayer = VideoPlayer()
        #videoplayer.resize(640, 480)
        #videoplayer.show()
        #QCoreApplication.processEvents()
        #sys.exit(app.exec_())


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
        print("Submit")
        rowMaster = self.returnRowData(row, user_id)
        if self.today.daysTo(self.dateSelect) > 0:
            print("Plan Add")
            for row in rowMaster:
                plan = Plan(row[0], row[1], row[2], row[3], row[4], row[5])
                plan.addPlan()
            print("Plan Add")
            print(rowMaster)
        else:
            print("Lift Add")
            for row in rowMaster:
                lift = Lift(row[0], row[1], row[2], row[3], row[4], row[5])
                lift.addLift()
            print("Lift Add")
            print(rowMaster)

    def submitDateRow(self, row, user_id):
        print("Submit Date")
        rowMaster = self.returnRowData(row, user_id)
        date = self.calendarWidget.selectedDate()
        selDate = f'{date.year()}-{date.month()}-{date.day()}'
        print(selDate)
        if self.today.daysTo(self.dateSelect) > 0:
            for row in rowMaster:
                print(row)
                try:
                    plan = Plan(row[0], row[1], selDate, row[2], row[3], row[4], row[5])
                    plan.addPlan()
                except Exception as ex:
                    msg = f'Error : {type(ex).__name__} ,arg = {ex.args}'
                    print(msg)
            print("Plan Add")
            print(rowMaster)
        else:
            for row in rowMaster:
                print(row)
                try:
                    lift = Lift(row[0], row[1], selDate, row[2], row[3], row[4], row[5])
                    lift.addLift()
                except Exception as ex:
                    msg = f'Error : {type(ex).__name__} ,arg = {ex.args}'
                    print(msg)
            print("Lift Add")
            print(rowMaster)
        self.initCalendar()

    def editRow(self, row, user_id):
        rowMaster = self.returnRowData(row, user_id)
        if self.today.daysTo(self.dateSelect) > 0:
            for row in rowMaster:
                try:
                    plan = Plan(row[6])
                    plan.updatePlan(row[1], row[2], row[3], row[4], row[5])
                except Exception as ex:
                    msg = f'Error : {type(ex).__name__} ,arg = {ex.args}'
                    print(msg)
        else:
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
        self.initCalendar()

    def deleteRow(self, row, user_id):
        rowMaster = self.returnRowData(row, user_id)
        if self.today.daysTo(self.dateSelect) > 0:
            for row in rowMaster:
                try:
                    plan = Plan(row[6])
                    plan.deletePlan()
                    #deleteLift(row[6])
                    #print(row[6])
                except Exception as ex:
                    msg = f'Error : {type(ex).__name__} ,arg = {ex.args}'
                    print(msg)
        else:
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
        # == 0 need attention
        if self.today.daysTo(date) < 0 :
            result = user.showRecordOn(f'{date.year()}-{date.month()}-{date.day()}')
        elif self.today.daysTo(date) > 0 :
            result = user.showPlanOn(f'{date.year()}-{date.month()}-{date.day()}')
        else:
            pass
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
        firstMedia = [self.btnMediaE1S1,self.btnMediaE1S2,self.btnMediaE1S3,self.btnMediaE1S4,self.btnMediaE1S5,self.btnMediaE1S6]
        secondMedia = [self.btnMediaE2S1,self.btnMediaE2S2,self.btnMediaE2S3,self.btnMediaE2S4,self.btnMediaE2S5,self.btnMediaE2S6]
        thirdMedia = [self.btnMediaE3S1,self.btnMediaE3S2,self.btnMediaE3S3,self.btnMediaE3S4,self.btnMediaE3S5,self.btnMediaE3S6]
        fourthMedia = [self.btnMediaE4S1,self.btnMediaE4S2,self.btnMediaE4S3,self.btnMediaE4S4,self.btnMediaE4S5,self.btnMediaE4S6]
        fifthMedia = [self.btnMediaE5S1,self.btnMediaE5S2,self.btnMediaE5S3,self.btnMediaE5S4,self.btnMediaE5S5,self.btnMediaE5S6]
        sixthMedia = [self.btnMediaE6S1,self.btnMediaE6S2,self.btnMediaE6S3,self.btnMediaE6S4,self.btnMediaE6S5,self.btnMediaE6S6]
        for cmb in cmbExcList:
            cmb.setCurrentIndex(-1)
        for r in firstRow + secondRow + thirdRow + fourthRow + fifthRow + sixthRow:
            r.setText(" ")
        for sp in firstSp + secondSp + thirdSp + fourthSp + fifthSp + sixthSp:
            sp.setValue(0)
        for hd in firstHidden + secondHidden + thirdHidden + fourthHidden + fifthHidden + sixthHidden:
            hd.setText("-")
        for btn in firstMedia + secondMedia + thirdMedia + fourthMedia + fifthMedia + sixthMedia:
            btn.setVisible(False)
        self.mediaClick = 0

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
    
    def gotoAccount(self):
        acc = accountPage()
        widget.addWidget(acc)
        widget.setCurrentWidget(acc) 

    def gotoChangePsw(self):
        changePsw = changePswPageFromInside()
        widget.addWidget(changePsw)
        widget.setCurrentWidget(changePsw)

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

    def stylePlan(self):
        cmbExcList = [self.cmbExcercise1,self.cmbExcercise2,self.cmbExcercise3,self.cmbExcercise4,self.cmbExcercise5,self.cmbExcercise6]
        for c in cmbExcList:
            c.setStyleSheet('*{color: rgb(98,145,255);}')

    def styleRecord(self):
        cmbExcList = [self.cmbExcercise1,self.cmbExcercise2,self.cmbExcercise3,self.cmbExcercise4,self.cmbExcercise5,self.cmbExcercise6]
        for c in cmbExcList:
            c.setStyleSheet('*{color: rgb(0,0,0);}')

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

        self.user = User(getLastSession())
        self.settingClick = 0
        
        self.initNav()
        self.initConnection()
        self.initHeader()
        self.initTDEE()

    def initConnection(self):
        self.btnToggle.clicked.connect(self.slideToRight)
        self.btnRecalculate.clicked.connect(self.initTDEE)
        self.btnSettings.clicked.connect(self.onClickBtnSettings)
        self.btnToPDF.clicked.connect(exportToPDF)
        self.btnToEmail.clicked.connect(sentToEmail)
        self.btnHome.clicked.connect(self.gotoHome)

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
        pxm1 = QPixmap("img/homeWhiteColor24Px.png")
        icon1 = QIcon(pxm1)
        pxm2 = QPixmap("img/userWhiteColor24Px.png")
        icon2 = QIcon(pxm2)
        pxm3 = QPixmap("img/document.png")
        icon3 = QIcon(pxm3)
        pxm4 = QPixmap("img/analytics.png")
        icon4 = QIcon(pxm4)
        pxm5 = QPixmap("img/bar-chart.png")
        icon5 = QIcon(pxm5)
        pxm6 = QPixmap("img/list.png")
        icon6 = QIcon(pxm6)
        pxm7 = QPixmap("img/meal.png")
        icon7 = QIcon(pxm7)
        self.btnToggle.setIcon(icon0)
        self.btnHome.setIcon(icon1)
        self.btnLiftLog.setIcon(icon3)
        self.btnTDEE.setIcon(icon7)
        self.btnLiftStats.setIcon(icon4)
        self.btnLiftRecord.setIcon(icon6)
        self.btnStrengthStandard.setIcon(icon5)
        self.btnAccount.setIcon(icon2)
        pxm4 = QPixmap("img/Tulisan JournFit-01.png")
        self.appLogo.setPixmap(pxm4)
        pxm7 = QPixmap("img/logout.png")
        icon7 = QIcon(pxm7)
        self.btnLogout.setIcon(icon7)
        pxm8 = QPixmap("img/padlock.png")
        icon8 = QIcon(pxm8)
        self.btnChangePsw.setIcon(icon8)
        pxm9 = QPixmap("img/settingsWhiteColor24Px.png")
        icon9 = QIcon(pxm9)
        self.btnSettings.setIcon(icon9)
        pxm10 = QPixmap("img/pdf.png")
        icon10 = QIcon(pxm10)
        self.btnToPDF.setIcon(icon10)
        pxm11 = QPixmap("img/mail.png")
        icon11 = QIcon(pxm11)
        self.btnToEmail.setIcon(icon11)
        self.btnLogout.setVisible(False)
        self.btnChangePsw.setVisible(False)
        self.btnToPDF.setVisible(False)
        self.btnToEmail.setVisible(False)
        if self.user.image == "":
            pxmFoto = QPixmap("img/user.png")
            self.profileFoto.setPixmap(pxmFoto)
        else:
            pxmFoto = QPixmap(self.user.image)
            self.profileFoto.setPixmap(pxmFoto)

        self.btnToggle.setStyleSheet('*{text-align: center}')
        self.btnHome.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftLog.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnTDEE.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(4, 155, 255); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftStats.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftRecord.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnStrengthStandard.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnAccount.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.profileName.setStyleSheet('*{border-radius : 10px; color: rgb(255, 255, 255);}*:hover {background-color: rgb(4, 155, 255);}')
        self.profileName.setText(self.user.name)
        self.btnSettings.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnToPDF.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnToEmail.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnChangePsw.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLogout.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')

        self.btnHome.setText("")
        self.btnLiftLog.setText("")
        self.btnTDEE.setText("")
        self.btnLiftStats.setText("")
        self.btnLiftRecord.setText("")
        self.btnStrengthStandard.setText("")
        self.btnAccount.setText("")
        self.btnSettings.setText("")
        self.btnToPDF.setText("")
        self.btnToEmail.setText("")
        self.btnChangePsw.setText("")
        self.btnLogout.setText("")

        #connection
        self.btnLiftLog.clicked.connect(self.gotoLiftLog)
        self.btnLiftStats.clicked.connect(self.gotoLiftStats)
        self.btnLiftRecord.clicked.connect(self.gotoLiftRecord)
        self.btnStrengthStandard.clicked.connect(self.gotoStrengthStandard)
        self.btnAccount.clicked.connect(self.gotoAccount)
        clickable(self.profileName).connect(self.gotoAccount)
        clickable(self.profileFoto).connect(self.gotoAccount)
    
    def slideToRight(self):
        width = self.LeftSideMenu.width()
        if width <= 100 :
            self.btnHome.setText("Home")
            self.btnLiftLog.setText("Lift Log")
            self.btnTDEE.setText("TDEE Stats")
            self.btnLiftStats.setText("Lift Stats")
            self.btnLiftRecord.setText("Lift Record")
            self.btnStrengthStandard.setText("Strength Standard")
            self.btnAccount.setText("Account")
            self.btnSettings.setText("Settings")
            self.btnToPDF.setText("Export To PDF")
            self.btnToEmail.setText("Sent To Email")
            self.btnChangePsw.setText("Change Password")
            self.btnLogout.setText("Logout")
            newWidth = 225
        else:
            self.btnHome.setText("")
            self.btnLiftLog.setText("")
            self.btnTDEE.setText("")
            self.btnLiftStats.setText("")
            self.btnLiftRecord.setText("")
            self.btnStrengthStandard.setText("")
            self.btnAccount.setText("")
            self.btnSettings.setText("")
            self.btnToPDF.setText("")
            self.btnToEmail.setText("")
            self.btnChangePsw.setText("")
            self.btnLogout.setText("")
            newWidth = 50

        self.animation = QPropertyAnimation(self.LeftSideMenu, b"minimumWidth")
        self.animation.setDuration(500)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()

    def snapImg(self):
        rectangle = QRect(QPoint(89, 122), QSize(1338, 831))
        pxm = self.grab(rectangle)
        pxm.save("screenshot/tdee.png")

    def onClickBtnSettings(self):
        self.settingClick += 1
        if self.settingClick%2 == 0:
            self.btnLogout.setVisible(False)
            self.btnChangePsw.setVisible(False)
            self.btnToPDF.setVisible(False)
            self.btnToEmail.setVisible(False)
            self.slideToRight()
        else:
            self.btnLogout.setVisible(True)
            self.btnChangePsw.setVisible(True)
            self.btnToPDF.setVisible(True)
            self.btnToEmail.setVisible(True)
            self.slideToRight()

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

    def gotoAccount(self):
        acc = accountPage()
        widget.addWidget(acc)
        widget.setCurrentWidget(acc)

    def gotoChangePsw(self):
        changePsw = changePswPageFromInside()
        widget.addWidget(changePsw)
        widget.setCurrentWidget(changePsw)

    def gotoLogin(self):
        login = loginPage()
        widget.addWidget(login)
        widget.setCurrentWidget(login)

    def gotoHome(self):
        home = homePage()
        widget.addWidget(home)
        widget.setCurrentWidget(home)


class liftStatsPage(QMainWindow):
    def __init__(self):
        super(liftStatsPage, self).__init__()
        loadUi("liftStats.ui", self)

        self.user = User(getLastSession())
        self.settingClick = 0
        self.btnToggle.clicked.connect(self.slideToRight)
        self.initNav()
        self.initConnection()
        self.writeData()
        #clear view and try except the func

        print("Lift Stats")

    def initNav(self):
        pxm0 = QPixmap("img/menuWhiteColor24Px.png")
        icon0 = QIcon(pxm0)
        pxm1 = QPixmap("img/homeWhiteColor24Px.png")
        icon1 = QIcon(pxm1)
        pxm2 = QPixmap("img/userWhiteColor24Px.png")
        icon2 = QIcon(pxm2)
        pxm3 = QPixmap("img/document.png")
        icon3 = QIcon(pxm3)
        pxm4 = QPixmap("img/analytics.png")
        icon4 = QIcon(pxm4)
        pxm5 = QPixmap("img/bar-chart.png")
        icon5 = QIcon(pxm5)
        pxm6 = QPixmap("img/list.png")
        icon6 = QIcon(pxm6)
        pxm7 = QPixmap("img/meal.png")
        icon7 = QIcon(pxm7)
        self.btnToggle.setIcon(icon0)
        self.btnHome.setIcon(icon1)
        self.btnLiftLog.setIcon(icon3)
        self.btnTDEE.setIcon(icon7)
        self.btnLiftStats.setIcon(icon4)
        self.btnLiftRecord.setIcon(icon6)
        self.btnStrengthStandard.setIcon(icon5)
        self.btnAccount.setIcon(icon2)
        pxm4 = QPixmap("img/Tulisan JournFit-01.png")
        self.appLogo.setPixmap(pxm4)
        pxm7 = QPixmap("img/logout.png")
        icon7 = QIcon(pxm7)
        self.btnLogout.setIcon(icon7)
        pxm8 = QPixmap("img/padlock.png")
        icon8 = QIcon(pxm8)
        self.btnChangePsw.setIcon(icon8)
        pxm9 = QPixmap("img/settingsWhiteColor24Px.png")
        icon9 = QIcon(pxm9)
        self.btnSettings.setIcon(icon9)
        pxm10 = QPixmap("img/pdf.png")
        icon10 = QIcon(pxm10)
        self.btnToPDF.setIcon(icon10)
        pxm11 = QPixmap("img/mail.png")
        icon11 = QIcon(pxm11)
        self.btnToEmail.setIcon(icon11)
        self.btnLogout.setVisible(False)
        self.btnChangePsw.setVisible(False)
        self.btnToPDF.setVisible(False)
        self.btnToEmail.setVisible(False)
        if self.user.image == "":
            pxmFoto = QPixmap("img/user.png")
            self.profileFoto.setPixmap(pxmFoto)
        else:
            pxmFoto = QPixmap(self.user.image)
            self.profileFoto.setPixmap(pxmFoto)

        self.btnToggle.setStyleSheet('*{text-align: center}')
        self.btnHome.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftLog.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnTDEE.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftStats.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(4, 155, 255); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftRecord.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnStrengthStandard.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnAccount.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.profileName.setStyleSheet('*{border-radius : 10px; color: rgb(255, 255, 255);}*:hover {background-color: rgb(4, 155, 255);}')
        self.profileName.setText(self.user.name)
        self.btnSettings.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnToPDF.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnToEmail.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnChangePsw.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLogout.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')

        self.btnHome.setText("")
        self.btnLiftLog.setText("")
        self.btnTDEE.setText("")
        self.btnLiftStats.setText("")
        self.btnLiftRecord.setText("")
        self.btnStrengthStandard.setText("")
        self.btnAccount.setText("")
        self.btnSettings.setText("")
        self.btnToPDF.setText("")
        self.btnToEmail.setText("")
        self.btnChangePsw.setText("")
        self.btnLogout.setText("")

        #connection
        self.btnLiftLog.clicked.connect(self.gotoLiftLog)
        self.btnTDEE.clicked.connect(self.gotoTDEE)
        self.btnLiftRecord.clicked.connect(self.gotoLiftRecord)
        self.btnStrengthStandard.clicked.connect(self.gotoStrengthStandard)
        self.btnAccount.clicked.connect(self.gotoAccount)
        clickable(self.profileName).connect(self.gotoAccount)
        clickable(self.profileFoto).connect(self.gotoAccount)

    def initConnection(self):
        self.btnSettings.clicked.connect(self.onClickBtnSettings)
        self.btnToPDF.clicked.connect(exportToPDF)
        self.btnToEmail.clicked.connect(sentToEmail)
        self.btnHome.clicked.connect(self.gotoHome)

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

    def snapImg(self):
        rectangle = QRect(QPoint(89, 122), QSize(1338, 831))
        pxm = self.grab(rectangle)
        pxm.save("screenshot/liftstats.png")

    def slideToRight(self):
        width = self.LeftSideMenu.width()
        if width <= 100 :
            self.btnHome.setText("Home")
            self.btnLiftLog.setText("Lift Log")
            self.btnTDEE.setText("TDEE Stats")
            self.btnLiftStats.setText("Lift Stats")
            self.btnLiftRecord.setText("Lift Record")
            self.btnStrengthStandard.setText("Strength Standard")
            self.btnAccount.setText("Account")
            self.btnSettings.setText("Settings")
            self.btnToPDF.setText("Export To PDF")
            self.btnToEmail.setText("Sent To Email")
            self.btnChangePsw.setText("Change Password")
            self.btnLogout.setText("Logout")
            newWidth = 225
        else:
            self.btnHome.setText("")
            self.btnLiftLog.setText("")
            self.btnTDEE.setText("")
            self.btnLiftStats.setText("")
            self.btnLiftRecord.setText("")
            self.btnStrengthStandard.setText("")
            self.btnAccount.setText("")
            self.btnSettings.setText("")
            self.btnToPDF.setText("")
            self.btnToEmail.setText("")
            self.btnChangePsw.setText("")
            self.btnLogout.setText("")
            newWidth = 50

        self.animation = QPropertyAnimation(self.LeftSideMenu, b"minimumWidth")
        self.animation.setDuration(500)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()

    def onClickBtnSettings(self):
        self.settingClick += 1
        if self.settingClick%2 == 0:
            self.btnLogout.setVisible(False)
            self.btnChangePsw.setVisible(False)
            self.btnToPDF.setVisible(False)
            self.btnToEmail.setVisible(False)
            self.slideToRight()
        else:
            self.btnLogout.setVisible(True)
            self.btnChangePsw.setVisible(True)
            self.btnToPDF.setVisible(True)
            self.btnToEmail.setVisible(True)
            self.slideToRight()

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

    def gotoAccount(self):
        acc = accountPage()
        widget.addWidget(acc)
        widget.setCurrentWidget(acc) 

    def gotoChangePsw(self):
        changePsw = changePswPageFromInside()
        widget.addWidget(changePsw)
        widget.setCurrentWidget(changePsw)

    def gotoLogin(self):
        login = loginPage()
        widget.addWidget(login)
        widget.setCurrentWidget(login)

    def gotoHome(self):
        home = homePage()
        widget.addWidget(home)
        widget.setCurrentWidget(home)


class liftRecordPage(QMainWindow):
    def __init__(self):
        super(liftRecordPage, self).__init__()
        loadUi("liftRecord.ui", self)

        self.user = User(getLastSession())
        self.settingClick = 0

        self.btnToggle.clicked.connect(self.slideToRight)
        self.initNav()
        self.writeData()
        self.plotChart()

    def initNav(self):
        pxm0 = QPixmap("img/menuWhiteColor24Px.png")
        icon0 = QIcon(pxm0)
        pxm1 = QPixmap("img/homeWhiteColor24Px.png")
        icon1 = QIcon(pxm1)
        pxm2 = QPixmap("img/userWhiteColor24Px.png")
        icon2 = QIcon(pxm2)
        pxm3 = QPixmap("img/document.png")
        icon3 = QIcon(pxm3)
        pxm4 = QPixmap("img/analytics.png")
        icon4 = QIcon(pxm4)
        pxm5 = QPixmap("img/bar-chart.png")
        icon5 = QIcon(pxm5)
        pxm6 = QPixmap("img/list.png")
        icon6 = QIcon(pxm6)
        pxm7 = QPixmap("img/meal.png")
        icon7 = QIcon(pxm7)
        self.btnToggle.setIcon(icon0)
        self.btnHome.setIcon(icon1)
        self.btnLiftLog.setIcon(icon3)
        self.btnTDEE.setIcon(icon7)
        self.btnLiftStats.setIcon(icon4)
        self.btnLiftRecord.setIcon(icon6)
        self.btnStrengthStandard.setIcon(icon5)
        self.btnAccount.setIcon(icon2)
        pxm4 = QPixmap("img/Tulisan JournFit-01.png")
        self.appLogo.setPixmap(pxm4)
        pxm7 = QPixmap("img/logout.png")
        icon7 = QIcon(pxm7)
        self.btnLogout.setIcon(icon7)
        pxm8 = QPixmap("img/padlock.png")
        icon8 = QIcon(pxm8)
        self.btnChangePsw.setIcon(icon8)
        pxm9 = QPixmap("img/settingsWhiteColor24Px.png")
        icon9 = QIcon(pxm9)
        self.btnSettings.setIcon(icon9)
        pxm10 = QPixmap("img/pdf.png")
        icon10 = QIcon(pxm10)
        self.btnToPDF.setIcon(icon10)
        pxm11 = QPixmap("img/mail.png")
        icon11 = QIcon(pxm11)
        self.btnToEmail.setIcon(icon11)
        self.btnLogout.setVisible(False)
        self.btnChangePsw.setVisible(False)
        self.btnToPDF.setVisible(False)
        self.btnToEmail.setVisible(False)
        if self.user.image == "":
            pxmFoto = QPixmap("img/user.png")
            self.profileFoto.setPixmap(pxmFoto)
        else:
            pxmFoto = QPixmap(self.user.image)
            self.profileFoto.setPixmap(pxmFoto)

        self.btnToggle.setStyleSheet('*{text-align: center}')
        self.btnHome.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftLog.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnTDEE.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftStats.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftRecord.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(4, 155, 255); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnStrengthStandard.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnAccount.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.profileName.setStyleSheet('*{border-radius : 10px; color: rgb(255, 255, 255);}*:hover {background-color: rgb(4, 155, 255);}')
        self.profileName.setText(self.user.name)
        self.btnSettings.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnToPDF.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnToEmail.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnChangePsw.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLogout.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')

        self.btnHome.setText("")
        self.btnLiftLog.setText("")
        self.btnTDEE.setText("")
        self.btnLiftStats.setText("")
        self.btnLiftRecord.setText("")
        self.btnStrengthStandard.setText("")
        self.btnAccount.setText("")
        self.btnSettings.setText("")
        self.btnToPDF.setText("")
        self.btnToEmail.setText("")
        self.btnChangePsw.setText("")
        self.btnLogout.setText("")

        #connection
        self.btnLiftLog.clicked.connect(self.gotoLiftLog)
        self.btnTDEE.clicked.connect(self.gotoTDEE)
        self.btnLiftStats.clicked.connect(self.gotoLiftStats)
        self.btnStrengthStandard.clicked.connect(self.gotoStrengthStandard)
        self.btnAccount.clicked.connect(self.gotoAccount)
        clickable(self.profileName).connect(self.gotoAccount)
        clickable(self.profileFoto).connect(self.gotoAccount)
        self.btnSettings.clicked.connect(self.onClickBtnSettings)
        self.btnToPDF.clicked.connect(exportToPDF)
        self.btnToEmail.clicked.connect(sentToEmail)
        self.btnHome.clicked.connect(self.gotoHome)

    def plotChart(self):
        self.radioBS.toggled.connect(self.clickedBS)
        self.radioFS.toggled.connect(self.clickedFS)
        self.radioDL.toggled.connect(self.clickedDL)
        self.radioSDL.toggled.connect(self.clickedSDL)
        self.radioBP.toggled.connect(self.clickedBP)
        self.radioIBP.toggled.connect(self.clickedIBP)
        self.radioOHP.toggled.connect(self.clickedOHP)
    
    def clickedBS(self):
        r = repMaxHistoryOf("BS",self.user.userID)
        img = plotToImage(r)
        imgQ = ImageQt(img)
        pxm = QPixmap.fromImage(imgQ)
        pxm1 = pxm.scaledToWidth(1071)
        pxm2 = pxm.scaledToHeight(401)
        #pxm2 = pxm.scaled(1071, 401, Qt.KeepAspectRatio)
        self.labelChart.setPixmap(pxm2)
        r.close()

    def clickedFS(self):
        r = repMaxHistoryOf("FS",self.user.userID)
        img = plotToImage(r)
        imgQ = ImageQt(img)
        pxm = QPixmap.fromImage(imgQ)
        pxm1 = pxm.scaledToWidth(1071)
        pxm2 = pxm.scaledToHeight(401)
        #pxm2 = pxm.scaled(1071, 401, Qt.KeepAspectRatio)
        self.labelChart.setPixmap(pxm2)
        r.close()

    def clickedDL(self):
        r = repMaxHistoryOf("DL",self.user.userID)
        img = plotToImage(r)
        imgQ = ImageQt(img)
        pxm = QPixmap.fromImage(imgQ)
        pxm1 = pxm.scaledToWidth(1071)
        pxm2 = pxm.scaledToHeight(401)
        #pxm2 = pxm.scaled(1071, 401, Qt.KeepAspectRatio)
        self.labelChart.setPixmap(pxm2)
        r.close()

    def clickedSDL(self):
        r = repMaxHistoryOf("SDL",self.user.userID)
        img = plotToImage(r)
        imgQ = ImageQt(img)
        pxm = QPixmap.fromImage(imgQ)
        pxm1 = pxm.scaledToWidth(1071)
        pxm2 = pxm.scaledToHeight(401)
        #pxm2 = pxm.scaled(1071, 401, Qt.KeepAspectRatio)
        self.labelChart.setPixmap(pxm2)
        r.close()

    def clickedBP(self):
        r = repMaxHistoryOf("BP",self.user.userID)
        img = plotToImage(r)
        imgQ = ImageQt(img)
        pxm = QPixmap.fromImage(imgQ)
        pxm1 = pxm.scaledToWidth(1071)
        pxm2 = pxm.scaledToHeight(401)
        #pxm2 = pxm.scaled(1071, 401, Qt.KeepAspectRatio)
        self.labelChart.setPixmap(pxm2)
        r.close()

    def clickedIBP(self):
        r = repMaxHistoryOf("IBP",self.user.userID)
        img = plotToImage(r)
        imgQ = ImageQt(img)
        pxm = QPixmap.fromImage(imgQ)
        pxm1 = pxm.scaledToWidth(1071)
        pxm2 = pxm.scaledToHeight(401)
        #pxm2 = pxm.scaled(1071, 401, Qt.KeepAspectRatio)
        self.labelChart.setPixmap(pxm2)
        r.close()

    def clickedOHP(self):
        r = repMaxHistoryOf("OHP",self.user.userID)
        img = plotToImage(r)
        imgQ = ImageQt(img)
        pxm = QPixmap.fromImage(imgQ)
        pxm1 = pxm.scaledToWidth(1071)
        pxm2 = pxm.scaledToHeight(401)
        #pxm2 = pxm.scaled(1071, 401, Qt.KeepAspectRatio)
        self.labelChart.setPixmap(pxm2)
        r.close()

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
            self.btnStrengthStandard.setText("Strength Standard")
            self.btnAccount.setText("Account")
            self.btnSettings.setText("Settings")
            self.btnToPDF.setText("Export To PDF")
            self.btnToEmail.setText("Sent To Email")
            self.btnChangePsw.setText("Change Password")
            self.btnLogout.setText("Logout")
            newWidth = 225
        else:
            self.btnHome.setText("")
            self.btnLiftLog.setText("")
            self.btnTDEE.setText("")
            self.btnLiftStats.setText("")
            self.btnLiftRecord.setText("")
            self.btnStrengthStandard.setText("")
            self.btnAccount.setText("")
            self.btnSettings.setText("")
            self.btnToPDF.setText("")
            self.btnToEmail.setText("")
            self.btnChangePsw.setText("")
            self.btnLogout.setText("")
            newWidth = 50

        self.animation = QPropertyAnimation(self.LeftSideMenu, b"minimumWidth")
        self.animation.setDuration(500)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()

    def snapImg(self):
        rectangle = QRect(QPoint(89, 122), QSize(1338, 371))
        pxm = self.grab(rectangle)
        pxm.save("screenshot/liftrecord.png")

    def onClickBtnSettings(self):
        self.settingClick += 1
        if self.settingClick%2 == 0:
            self.btnLogout.setVisible(False)
            self.btnChangePsw.setVisible(False)
            self.btnToPDF.setVisible(False)
            self.btnToEmail.setVisible(False)
            self.slideToRight()
        else:
            self.btnLogout.setVisible(True)
            self.btnChangePsw.setVisible(True)
            self.btnToPDF.setVisible(True)
            self.btnToEmail.setVisible(True)
            self.slideToRight()

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

    def gotoAccount(self):
        acc = accountPage()
        widget.addWidget(acc)
        widget.setCurrentWidget(acc)

    def gotoChangePsw(self):
        changePsw = changePswPageFromInside()
        widget.addWidget(changePsw)
        widget.setCurrentWidget(changePsw)

    def gotoLogin(self):
        login = loginPage()
        widget.addWidget(login)
        widget.setCurrentWidget(login)

    def gotoHome(self):
        home = homePage()
        widget.addWidget(home)
        widget.setCurrentWidget(home)


class strengthStandardPage(QMainWindow):
    def __init__(self):
        super(strengthStandardPage, self).__init__()
        loadUi("strengthStandard.ui", self)

        self.user = User(getLastSession())
        self.settingClick = 0

        self.btnToggle.clicked.connect(self.slideToRight)
        self.initNav()
        self.initConnection()

    def initNav(self):
        pxm0 = QPixmap("img/menuWhiteColor24Px.png")
        icon0 = QIcon(pxm0)
        pxm1 = QPixmap("img/homeWhiteColor24Px.png")
        icon1 = QIcon(pxm1)
        pxm2 = QPixmap("img/userWhiteColor24Px.png")
        icon2 = QIcon(pxm2)
        pxm3 = QPixmap("img/document.png")
        icon3 = QIcon(pxm3)
        pxm4 = QPixmap("img/analytics.png")
        icon4 = QIcon(pxm4)
        pxm5 = QPixmap("img/bar-chart.png")
        icon5 = QIcon(pxm5)
        pxm6 = QPixmap("img/list.png")
        icon6 = QIcon(pxm6)
        pxm7 = QPixmap("img/meal.png")
        icon7 = QIcon(pxm7)
        self.btnToggle.setIcon(icon0)
        self.btnHome.setIcon(icon1)
        self.btnLiftLog.setIcon(icon3)
        self.btnTDEE.setIcon(icon7)
        self.btnLiftStats.setIcon(icon4)
        self.btnLiftRecord.setIcon(icon6)
        self.btnStrengthStandard.setIcon(icon5)
        self.btnAccount.setIcon(icon2)
        pxm4 = QPixmap("img/Tulisan JournFit-01.png")
        self.appLogo.setPixmap(pxm4)
        pxm7 = QPixmap("img/logout.png")
        icon7 = QIcon(pxm7)
        self.btnLogout.setIcon(icon7)
        pxm8 = QPixmap("img/padlock.png")
        icon8 = QIcon(pxm8)
        self.btnChangePsw.setIcon(icon8)
        pxm9 = QPixmap("img/settingsWhiteColor24Px.png")
        icon9 = QIcon(pxm9)
        self.btnSettings.setIcon(icon9)
        pxm10 = QPixmap("img/pdf.png")
        icon10 = QIcon(pxm10)
        self.btnToPDF.setIcon(icon10)
        pxm11 = QPixmap("img/mail.png")
        icon11 = QIcon(pxm11)
        self.btnToEmail.setIcon(icon11)
        self.btnLogout.setVisible(False)
        self.btnChangePsw.setVisible(False)
        self.btnToPDF.setVisible(False)
        self.btnToEmail.setVisible(False)
        if self.user.image == "":
            pxmFoto = QPixmap("img/user.png")
            self.profileFoto.setPixmap(pxmFoto)
        else:
            pxmFoto = QPixmap(self.user.image)
            self.profileFoto.setPixmap(pxmFoto)

        self.btnToggle.setStyleSheet('*{text-align: center}')
        self.btnHome.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftLog.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnTDEE.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftStats.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftRecord.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnStrengthStandard.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(4, 155, 255); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnAccount.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.profileName.setStyleSheet('*{border-radius : 10px; color: rgb(255, 255, 255);}*:hover {background-color: rgb(4, 155, 255);}')
        self.profileName.setText(self.user.name)
        self.btnSettings.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnToPDF.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnToEmail.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnChangePsw.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLogout.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')

        self.btnHome.setText("")
        self.btnLiftLog.setText("")
        self.btnTDEE.setText("")
        self.btnLiftStats.setText("")
        self.btnLiftRecord.setText("")
        self.btnStrengthStandard.setText("")
        self.btnAccount.setText("")
        self.btnSettings.setText("")
        self.btnToPDF.setText("")
        self.btnToEmail.setText("")
        self.btnChangePsw.setText("")
        self.btnLogout.setText("")

        #connection
        self.btnLiftLog.clicked.connect(self.gotoLiftLog)
        self.btnTDEE.clicked.connect(self.gotoTDEE)
        self.btnLiftStats.clicked.connect(self.gotoLiftStats)
        self.btnLiftRecord.clicked.connect(self.gotoLiftRecord)
        self.btnAccount.clicked.connect(self.gotoAccount)
        clickable(self.profileName).connect(self.gotoAccount)
        clickable(self.profileFoto).connect(self.gotoAccount)

    def initConnection(self):
        self.btnToggle.clicked.connect(self.slideToRight)
        self.btnChangePsw.clicked.connect(self.gotoChangePsw)
        self.btnLogout.clicked.connect(self.gotoLogin)
        self.btnSettings.clicked.connect(self.onClickBtnSettings)
        self.btnToPDF.clicked.connect(exportToPDF)
        self.btnToEmail.clicked.connect(sentToEmail)
        self.btnHome.clicked.connect(self.gotoHome)

    def slideToRight(self):
        width = self.LeftSideMenu.width()
        if width <= 100 :
            self.btnHome.setText("Home")
            self.btnLiftLog.setText("Lift Log")
            self.btnTDEE.setText("TDEE Stats")
            self.btnLiftStats.setText("Lift Stats")
            self.btnLiftRecord.setText("Lift Record")
            self.btnStrengthStandard.setText("Strength Standard")
            self.btnAccount.setText("Account")
            self.btnSettings.setText("Settings")
            self.btnToPDF.setText("Export To PDF")
            self.btnToEmail.setText("Sent To Email")
            self.btnChangePsw.setText("Change Password")
            self.btnLogout.setText("Logout")
            newWidth = 225
        else:
            self.btnHome.setText("")
            self.btnLiftLog.setText("")
            self.btnTDEE.setText("")
            self.btnLiftStats.setText("")
            self.btnLiftRecord.setText("")
            self.btnStrengthStandard.setText("")
            self.btnAccount.setText("")
            self.btnSettings.setText("")
            self.btnToPDF.setText("")
            self.btnToEmail.setText("")
            self.btnChangePsw.setText("")
            self.btnLogout.setText("")
            newWidth = 50

        self.animation = QPropertyAnimation(self.LeftSideMenu, b"minimumWidth")
        self.animation.setDuration(500)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()

    def onClickBtnSettings(self):
        self.settingClick += 1
        if self.settingClick%2 == 0:
            self.btnLogout.setVisible(False)
            self.btnChangePsw.setVisible(False)
            self.btnToPDF.setVisible(False)
            self.btnToEmail.setVisible(False)
            self.slideToRight()
        else:
            self.btnLogout.setVisible(True)
            self.btnChangePsw.setVisible(True)
            self.btnToPDF.setVisible(True)
            self.btnToEmail.setVisible(True)
            self.slideToRight()

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

    def gotoAccount(self):
        acc = accountPage()
        widget.addWidget(acc)
        widget.setCurrentWidget(acc) 

    def gotoChangePsw(self):
        changePsw = changePswPageFromInside()
        widget.addWidget(changePsw)
        widget.setCurrentWidget(changePsw)

    def gotoLogin(self):
        login = loginPage()
        widget.addWidget(login)
        widget.setCurrentWidget(login)

    def gotoHome(self):
        home = homePage()
        widget.addWidget(home)
        widget.setCurrentWidget(home)


class accountPage(QMainWindow):
    def __init__(self):
        super(accountPage, self).__init__()
        loadUi("Account.ui", self)

        self.user = User(getLastSession())
        self.settingClick = 0

        self.initNav()
        self.initConnection()
        self.initAccount()
        #self.sentToEmail()
        #self.exportToPDF()

        self.btnEdit.setText("Edit") 
        self.btnEdit.setStyleSheet('QPushButton {background-color: rgb(17, 140, 255);}')
        self.disableData()

    def initNav(self):
        pxm0 = QPixmap("img/menuWhiteColor24Px.png")
        icon0 = QIcon(pxm0)
        pxm1 = QPixmap("img/homeWhiteColor24Px.png")
        icon1 = QIcon(pxm1)
        pxm2 = QPixmap("img/userWhiteColor24Px.png")
        icon2 = QIcon(pxm2)
        pxm3 = QPixmap("img/document.png")
        icon3 = QIcon(pxm3)
        pxm4 = QPixmap("img/analytics.png")
        icon4 = QIcon(pxm4)
        pxm5 = QPixmap("img/bar-chart.png")
        icon5 = QIcon(pxm5)
        pxm6 = QPixmap("img/list.png")
        icon6 = QIcon(pxm6)
        pxm7 = QPixmap("img/meal.png")
        icon7 = QIcon(pxm7)
        self.btnToggle.setIcon(icon0)
        self.btnHome.setIcon(icon1)
        self.btnLiftLog.setIcon(icon3)
        self.btnTDEE.setIcon(icon7)
        self.btnLiftStats.setIcon(icon4)
        self.btnLiftRecord.setIcon(icon6)
        self.btnStrengthStandard.setIcon(icon5)
        self.btnAccount.setIcon(icon2)
        pxm4 = QPixmap("img/Tulisan JournFit-01.png")
        self.appLogo.setPixmap(pxm4)
        if self.user.image == "":
            pxmFoto = QPixmap("img/user.png")
            self.profileFoto.setPixmap(pxmFoto)
            self.labelFP.setPixmap(pxmFoto)
        else:
            pxmFoto = QPixmap(self.user.image)
            self.profileFoto.setPixmap(pxmFoto)
            self.labelFP.setPixmap(pxmFoto)
        pxm6 = QPixmap("img/logoutWhite.png")
        icon6 = QIcon(pxm6)
        self.btnEdit.setIcon(icon6)
        pxm5 = QPixmap("img/camera.png")
        icon5 = QIcon(pxm5)
        self.btnChangeFP.setIcon(icon5)
        pxm7 = QPixmap("img/logout.png")
        icon7 = QIcon(pxm7)
        self.btnLogout.setIcon(icon7)
        pxm8 = QPixmap("img/padlock.png")
        icon8 = QIcon(pxm8)
        self.btnChangePsw.setIcon(icon8)
        pxm9 = QPixmap("img/settingsWhiteColor24Px.png")
        icon9 = QIcon(pxm9)
        self.btnSettings.setIcon(icon9)
        pxm10 = QPixmap("img/pdf.png")
        icon10 = QIcon(pxm10)
        self.btnToPDF.setIcon(icon10)
        pxm11 = QPixmap("img/mail.png")
        icon11 = QIcon(pxm11)
        self.btnToEmail.setIcon(icon11)
        self.btnLogout.setVisible(False)
        self.btnChangePsw.setVisible(False)
        self.btnToPDF.setVisible(False)
        self.btnToEmail.setVisible(False)

        self.btnToggle.setStyleSheet('*{text-align: center}')
        self.btnHome.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftLog.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnTDEE.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftStats.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLiftRecord.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnStrengthStandard.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnAccount.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(4, 155, 255); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnSettings.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnToPDF.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnToEmail.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnChangePsw.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.btnLogout.setStyleSheet('QPushButton{padding-left: 15px;}*{text-align: left; background-color: rgb(3, 114, 188); border:none; border-radius : 10px; color: rgb(255, 255, 255); padding : 20px 5px;}*:hover {background-color: rgb(4, 155, 255);}')
        self.profileName.setStyleSheet('*{border-radius : 10px; color: rgb(255, 255, 255);}*:hover {background-color: rgb(4, 155, 255);}')
        self.profileName.setText(self.user.name)
        
        self.btnHome.setText("")
        self.btnLiftLog.setText("")
        self.btnTDEE.setText("")
        self.btnLiftStats.setText("")
        self.btnLiftRecord.setText("")
        self.btnStrengthStandard.setText("")
        self.btnAccount.setText("")
        self.btnSettings.setText("")
        self.btnToPDF.setText("")
        self.btnToEmail.setText("")
        self.btnChangePsw.setText("")
        self.btnLogout.setText("")

        #connection
        self.btnLiftLog.clicked.connect(self.gotoLiftLog)
        self.btnTDEE.clicked.connect(self.gotoTDEE)
        self.btnLiftStats.clicked.connect(self.gotoLiftStats)
        self.btnLiftRecord.clicked.connect(self.gotoLiftRecord)
        self.btnStrengthStandard.clicked.connect(self.gotoStrengthStandard)

    def initConnection(self):
        self.btnToggle.clicked.connect(self.slideToRight)
        self.btnChangePsw.clicked.connect(self.gotoChangePsw)
        self.btnLogout.clicked.connect(self.gotoLogin)
        self.btnEdit.clicked.connect(self.onClickBtnEdit)
        self.btnChangeFP.clicked.connect(self.onClickBtnChangeFP)
        self.btnSettings.clicked.connect(self.onClickBtnSettings)
        self.btnToPDF.clicked.connect(exportToPDF)
        self.btnToEmail.clicked.connect(sentToEmail)
        self.btnHome.clicked.connect(self.gotoHome)

    def initAccount(self):
        d = self.user.dateOfBirth.strftime("%Y-%m-%d")
        date = QDate.fromString(d, "yyyy-MM-dd")
        day = {1:"Monday", 2:"Tuesday", 3:"Wednesday", 4:"Thursday", 5:"Friday", 6:"Saturday", 7:"Monday"}
        recordCount = countRecordOf(self.user.userID)
        sessionCount = countLoginOf(self.user.userID)
        pswchgCount = countPswChangeOf(self.user.userID)
        last5Session = getLastFiveSession(self.user.userID)
        last5Record = getLastFiveRecord(self.user.userID)

        self.txtFullname.setText(self.user.fullname)
        self.txtName.setText(self.user.name)
        self.txtEmail.setText(self.user.email)
        self.cmbDate.setCurrentIndex(date.day())
        self.cmbMonth.setCurrentIndex(date.month())
        self.cmbYear.setCurrentText(str(date.year()))
        self.txtHeight.setText(f'{self.user.height} cm')
        self.txtWeight.setText(f'{self.user.weight} kg')
        self.txtBodyfat.setText(f'{self.user.bodyfat} %')
        self.cmbExperience.setCurrentIndex(self.user.experience)
        self.cmbActivity.setCurrentIndex(self.user.activity)
        self.txtRecordCount.setText(str(recordCount))
        self.txtLoginCount.setText(str(sessionCount))
        self.txtPswchgCount.setText(str(pswchgCount))

        self.txtSession1.setText(last5Session[0])
        self.txtSession2.setText(last5Session[1])
        self.txtSession3.setText(last5Session[2])
        self.txtSession4.setText(last5Session[3])
        self.txtSession5.setText(last5Session[4])

        try:
            self.txtRecord1.setText(last5Record[0] + ", " + day[QDate.fromString(last5Record[0], "yyyy-MM-dd").dayOfWeek()])
            self.txtRecord2.setText(last5Record[1] + ", " + day[QDate.fromString(last5Record[1], "yyyy-MM-dd").dayOfWeek()])
            self.txtRecord3.setText(last5Record[2] + ", " + day[QDate.fromString(last5Record[2], "yyyy-MM-dd").dayOfWeek()])
            self.txtRecord4.setText(last5Record[3] + ", " + day[QDate.fromString(last5Record[3], "yyyy-MM-dd").dayOfWeek()])
            self.txtRecord5.setText(last5Record[4] + ", " + day[QDate.fromString(last5Record[4], "yyyy-MM-dd").dayOfWeek()])
        except:
            self.txtRecord1.setText(last5Record[0])
            self.txtRecord2.setText(last5Record[1])
            self.txtRecord3.setText(last5Record[2])
            self.txtRecord4.setText(last5Record[3])
            self.txtRecord5.setText(last5Record[4])

    def slideToRight(self):
        width = self.LeftSideMenu.width()
        if width <= 100 :
            self.btnHome.setText("Home")
            self.btnLiftLog.setText("Lift Log")
            self.btnTDEE.setText("TDEE Stats")
            self.btnLiftStats.setText("Lift Stats")
            self.btnLiftRecord.setText("Lift Record")
            self.btnStrengthStandard.setText("Strength Standard")
            self.btnAccount.setText("Account")
            self.btnSettings.setText("Settings")
            self.btnToPDF.setText("Export To PDF")
            self.btnToEmail.setText("Sent To Email")
            self.btnChangePsw.setText("Change Password")
            self.btnLogout.setText("Logout")
            newWidth = 225
        else:
            self.btnHome.setText("")
            self.btnLiftLog.setText("")
            self.btnTDEE.setText("")
            self.btnLiftStats.setText("")
            self.btnLiftRecord.setText("")
            self.btnStrengthStandard.setText("")
            self.btnAccount.setText("")
            self.btnSettings.setText("")
            self.btnToPDF.setText("")
            self.btnToEmail.setText("")
            self.btnChangePsw.setText("")
            self.btnLogout.setText("")
            newWidth = 50

        self.animation = QPropertyAnimation(self.LeftSideMenu, b"minimumWidth")
        self.animation.setDuration(500)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()

    def onClickBtnSettings(self):
        self.settingClick += 1
        if self.settingClick%2 == 0:
            self.btnLogout.setVisible(False)
            self.btnChangePsw.setVisible(False)
            self.btnToPDF.setVisible(False)
            self.btnToEmail.setVisible(False)
            self.slideToRight()
        else:
            self.btnLogout.setVisible(True)
            self.btnChangePsw.setVisible(True)
            self.btnToPDF.setVisible(True)
            self.btnToEmail.setVisible(True)
            self.slideToRight()

    def onClickBtnEdit(self):
        self.toggleEdit += 1
        fullname = self.txtFullname.text()
        name = self.txtName.text()
        email = self.txtEmail.text()
        dobDay = self.cmbDate.currentText()
        dobMonth = self.cmbMonth.currentIndex()
        dobYear = self.cmbYear.currentText()
        weight = self.txtWeight.text().strip(" kg")
        height = self.txtHeight.text().strip(" cm")
        bf = self.txtBodyfat.text().strip(" %")
        exp = self.cmbExperience.currentIndex()
        activity = self.cmbActivity.currentIndex()
        if self.toggleEdit % 2 == 1 :
            self.enableData()
            self.btnEdit.setText("Submit")
            self.btnEdit.setStyleSheet('QPushButton {background-color: rgb(85, 170, 0);}')
        else :
            self.btnEdit.setText("Edit") 
            self.btnEdit.setStyleSheet('QPushButton {background-color: rgb(17, 140, 255);}')
            self.disableData()
            self.user.updateUser(fullname, name, email, dobDay, dobMonth, dobYear, weight, height, bf, exp, activity)

    def onClickBtnChangeFP(self):
        file = dialog()
        file.openFileNameDialog()
        self.user.insertImage(file.file)
        pxmFoto = QPixmap(file.file)
        self.profileFoto.setPixmap(pxmFoto)
        self.labelFP.setPixmap(pxmFoto)

    def enableData(self):
        self.txtFullname.setReadOnly(False)
        self.txtName.setReadOnly(False)
        self.txtEmail.setReadOnly(False)
        self.cmbDate.setEnabled(True)
        self.cmbMonth.setEnabled(True)
        self.cmbYear.setEnabled(True)
        self.txtHeight.setReadOnly(False)
        self.txtWeight.setReadOnly(False)
        self.txtBodyfat.setReadOnly(False)
        self.cmbExperience.setEnabled(True)
        self.cmbActivity.setEnabled(True)

    def disableData(self):
        self.txtFullname.setReadOnly(True)
        self.txtName.setReadOnly(True)
        self.txtEmail.setReadOnly(True)
        self.cmbDate.setEnabled(False)
        self.cmbMonth.setEnabled(False)
        self.cmbYear.setEnabled(False)
        self.txtHeight.setReadOnly(True)
        self.txtWeight.setReadOnly(True)
        self.txtBodyfat.setReadOnly(True)
        self.cmbExperience.setEnabled(False)
        self.cmbActivity.setEnabled(False)

    def snapImg(self):
        rectangle = QRect(QPoint(89, 122), QSize(1338, 831))
        pxm = self.grab(rectangle)
        pxm.save("screenshot/account.png")

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

    def gotoStrengthStandard(self):
        strengthSt = strengthStandardPage()
        widget.addWidget(strengthSt)
        widget.setCurrentWidget(strengthSt)

    def gotoChangePsw(self):
        changePsw = changePswPageFromInside()
        widget.addWidget(changePsw)
        widget.setCurrentWidget(changePsw)

    def gotoLogin(self):
        login = loginPage()
        widget.addWidget(login)
        widget.setCurrentWidget(login)

    def gotoHome(self):
        home = homePage()
        widget.addWidget(home)
        widget.setCurrentWidget(home)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    news = scrapingContent("https://www.health.com/fitness","https://www.t-nation.com/training/","https://www.theguardian.com/sport/olympic-games-2020")
    widget = QtWidgets.QStackedWidget()
    #web = QWebEngineView()
    #web.load(QUrl("https://www.health.com/fitness/this-50-push-up-challenge-will-transform-your-body-in-30-days"))
    #web.show()
    screen1 = loginPage()
    widget.addWidget(screen1)
    widget.show()


    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")