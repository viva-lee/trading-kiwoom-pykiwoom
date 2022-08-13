# 키움증권 API 에 대한 반환값을 가져오기 위한 모듈
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QAxContainer import *
from pykiwoom.kiwoom import *
from datetime import datetime
# from time import time

import pandas as pd
import numpy as np

from config.settings import *
# from strategy import *


class Worker(QThread):
    marketInfo = pyqtSignal(dict)
    # tradeInfo = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.isRun = False
        self.kiwoom = Kiwoom()
        self.kiwoom.CommConnect(block=True)
        self.kiwoom.GetConditionLoad()
        self.conditions = self.kiwoom.GetConditionNameList()

        # self.kiwoom = QAxWidget('KHOPENAPI.KHOpenAPICtrl.1')
        # self.kiwoom.dynamicCall('CommConnect()')
        # self.kiwoom.dynamicCall('GetConditionLoad()')
        # self.conditions = self.kiwoom.dynamicCall('GetConditionNameList()')
        print(self.conditions)
        self.connectState = False

    def getInitState(self):
        state = self.kiwoom.GetConnectState()
        if state == 0:
            self.connectState = False
        elif state == 1:
            self.connectState = True


    def run(self):
        while self.isRun:
            self.getInitState()
            print(self.connectState)
            data = {}
            # 데이터 추가
            if self.connectState == True:
                data['state'] = True
                data['condition'] = [name for index, name in self.conditions]
                data['tickers'] = self.getMarketInfo()
            else:
                data['state'] = False

            # 데이터 송신
            self.marketInfo.emit(data)
            self.sleep(60)

    def getMarketInfo(self):
        # 데이터
        # try:
        searchList = {}
        for index, name in self.conditions:
            tickers = self.kiwoom.SendCondition("0101", name, index, 0)
            tickersName = []
            for ticker in tickers:
                tickerName = self.kiwoom.GetMasterCodeName(ticker)
                tickersName.append(tickerName)
            searchList[name] = [tickers, tickersName]
        return searchList
        # except:
        #     return None

    # def getTradeInfo(self, ticker):
    #     # 00 : 지정가, 03 : 시장가
    #     if 매수:
    #         kiwoom.SendOrder("시장가매수", "0101", stockAccount, 1, ticker, 주문수량, 주문단가, "03", "")
    #     elif 매도:
    #         kiwoom.SendOrder("시장가매도", "0101", stockAccount, 2, ticker, 주문수량, 0, "03", "")

# 로그인


# 종목검색식


# 자동거래
