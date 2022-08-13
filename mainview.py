import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from mainview_ui import Ui_MainWindow
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

from libs.worker import *

class MyWindow(Ui_MainWindow):
    def __init__(self, w):
        Ui_MainWindow.__init__(self)
        self.setupUi(w)

        # 데이터 수집
        self.worker = Worker()
        self.worker.marketInfo.connect(self.updateConditionList)
        # self.worker.tradeInfo.connect(self.updateTradingLog)
        self.worker.start()

        # 조건검색식 리스트
        self.conditionSetting = False
        self.conditionList.itemDoubleClicked.connect(self.conditionDoubleClicked)
        self.currentCondition = ''

        self.pushButton.clicked.connect(self.startService)

    def updateConditionList(self, data):
        if data['state'] == True and self.conditionSetting == False:
            self.conditionList.addItems(data['condition'])
            self.conditionSetting = True
        if self.currentCondition != '':
            self.SearchList.setText(str(data['tickers'][self.currentCondition][1]))
    
    def conditionDoubleClicked(self):
        self.currentCondition = self.conditionList.currentItem().text()
        print(self.currentCondition)

    def startService(self):
        if self.worker.isRun == False:
            self.worker.isRun = True
            self.worker.start()
        else:
            self.worker.isRun = False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Form = QMainWindow()
    execUI = MyWindow(Form)
    Form.show()
    sys.exit(app.exec_())