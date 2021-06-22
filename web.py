import sys
from PyQt5.Qt import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication
 
 
 
def showWeb():
    app = QApplication(sys.argv)
     
    web = QWebEngineView()
     
    web.load(QUrl("https://www.health.com/fitness/this-50-push-up-challenge-will-transform-your-body-in-30-days"))
     
    web.show()
     
     
    sys.exit(app.exec_())