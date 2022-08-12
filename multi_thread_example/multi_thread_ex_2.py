import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# PyQT의 Qthread 이용한 멀티스레드
class Worker(QThread):
    info = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        
    def run(self):
        while True:
            data = self.getInfo()
            self.info.emit(data)
            
    def getInfo(self):
        data = {}
        return data
    
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # worker 스레드
        self.worker = Worker()
        self.worker.info.connect(self.pop_order)
        self.worker.start()
        
    def pop_order(self):
        print(data)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()