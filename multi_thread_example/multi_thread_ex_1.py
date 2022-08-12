import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import datetime
from multiprocessing import Queue

# 큐를 이용한 멀티스레드
class Worker(QThread):
    trigger = pyqtSignal()
    
    def __init__(self, data_queue, order_queue):
        super().__init__()
        self.data_queue = data_queue # 데이터 받기
        self.order_queue = order_queue # 주문 요청
    
    def run(self):
        while True:
            if not self.data_queue.empty():
                data = self.data_queue.get()
                self.order_queue.put(data)
                self.trigger.emit()
                
class MyWindow(QMainWindow):
    def __init__(self, data_queue, order_queue):
        super().__init__()
        
        # 큐
        self.data_queue = data_queue
        self.order_queue = order_queue
        
        # worker 스레드
        self.worker = Worker(data_queue, order_queue)
        self.worker.trigger.connect(self.pop_order)
        self.worker.start()
    
    def push_data(self):
        now = datetime.datetime.now()
        self.data_queue.put(now.second)
    
    @pyqtSlot()
    def pop_order(self):
        if not self.order_queue.empty():
            data = self.order_queue.get()
            print(data)
                
                
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    data_queue = Queue()
    order_queue = Queue()
    window = MyWindow(data_queue, order_queue)
    window.show()
    
    app.exec_()