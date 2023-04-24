import requests
import json

import numpy as np
import os
import time
import alpaca_trade_api as tradeapi
import os.path

api_key = 'PK6CZ36K8ZZ98TOXPKUB'
api_secret = 'R5E1zku39OCuYFVZHleab4lyHPWofdbeaDUbRqgb'
base_url = 'https://paper-api.alpaca.markets'

api = tradeapi.REST(api_key, api_secret, base_url,
api_version='v2')

def meanRev(prcs, ticker):
    reversed(prcs)
    buy = 0
    profit = 0
    start=time.time()
    days = 5
    i = 0
    
    for p in prcs:
        
        if i >= days:
            avg = np.mean(prcs[i-days:i])
            
            if p < avg * .98 and buy == 0:
                buy = p
                print("buying: ", p)
                # print(len(prcs)) #Andy said should be 200 something
                
                if i == len(prcs)-1:
                    api.submit_order(
                        symbol = ticker,
                        qty=1,
                        side='buy',
                        type='market',
                        time_in_force='gtc'
                        )
                    
            elif p > avg * 1.02 and buy != 0:
                profit += p - buy
                buy = 0
                print("selling at: ", p)
                
                if i == len(prcs)-1:
                    api.submit_order(
                        symbol = ticker,
                        qty=1,
                        side='sell',
                        type='market',
                        time_in_force='gtc'
                        )
                        
            else:
                pass
        
        i += 1
    
    print('\n')

    print("total profit: ", profit)
    print("returns: ", profit/prcs[0])
    print("total time: ", time.time() - start)
    
def simpleMoving(prcs):
    reversed(prcs)
    buy = 0
    profit = 0
    start=time.time()
    days = 5
    i = 0
    
    for p in prcs:
        
        if i >= days:
            avg = np.mean(prcs[i-days:i])
            
            if p > avg and buy == 0:
                buy = p
                print("buying: ", p)
                
                if i == len(prcs)-1:
                    api.submit_order(
                        symbol = ticker,
                        qty=1,
                        side='buy',
                        type='market',
                        time_in_force='gtc'
                        )
            
            elif p < avg and buy != 0:
                profit += p - buy
                buy = 0
                print("selling at: ", p)
                
                if i == len(prcs)-1:
                    api.submit_order(
                        symbol = ticker,
                        qty=1,
                        side='sell',
                        type='market',
                        time_in_force='gtc'
                        )
            
            else:
                pass
        
        i += 1
    
    print('\n')

    print("total profit: ", profit)
    print("returns: ", profit/prcs[0])
    print("total time: ", time.time() - start)
        
def bollinger(prcs):
    reversed(prcs)
    start=time.time()
    days = 5
    i = 0
    buy = 0
    profit = 0
    
    for p in prcs:
        
        if i >= days:
            avg = np.mean(prcs[i-days:i])
            
            if p > avg * 1.02 and buy == 0:
                buy = p
                print("buying: ", p)
                
                if i == len(prcs)-1:
                    api.submit_order(
                        symbol = ticker,
                        qty=1,
                        side='buy',
                        type='market',
                        time_in_force='gtc'
                        )
            
            elif p < avg * .98 and buy != 0:
                profit += p - buy
                buy = 0
                print("selling at: ", p)
                
                if i == len(prcs)-1:
                    api.submit_order(
                        symbol = ticker,
                        qty=1,
                        side='sell',
                        type='market',
                        time_in_force='gtc'
                        )
            
            else:
                pass
        
        i += 1
    
    print('\n')

    print("total profit: ", profit)
    print("returns: ", profit/prcs[0])
    print("total time: ", time.time() - start)
        
def shortsell(prcs):
    reversed(prcs)
    start=time.time()
    days = 5
    i = 0
    sell = 0
    profit = 0
    buy = 0
    
    for p in prcs:
        
        if i >= days:
            avg = np.mean(prcs[i-days:i])
            
            if p > avg and sell == 0:
                sell = p
                print("selling: ", p)
            
            elif p < avg and sell != 0:
                profit += sell - buy
                sell = 0
                print("buying at: ", p)
            
            else:
                pass
        
        i += 1
        
    print('\n')

    print("total profit: ", profit)
    print("returns: ", profit/prcs[0])
    print("total time: ", time.time() - start)
    
#--------------------------------------------------------------------------------
ticker = ['IBM','AAPL','MSFT','AMZN','ABNB','ADBE','TSLA','AMC', 'ZI','DIS']

for tick in ticker:

    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol='+tick+'&outputsize=full&apikey=KP79NZ9ITS60M0LM'
    
    request = requests.get(url)
    # print(request.text)
    # input()
    
    stockDict = json.loads(request.text)
    # json.dump(stockDict, open(ticker+".json", "w"), indent = 4)# save dictionary to json file
    
    key1 = "Time Series (Daily)"
    key3 = "5. adjusted close"
    sell = 0
    
    existFile = '/home/ubuntu/environment/final_project/data/'+tick+'.csv'
    check_file = os.path.exists(existFile)
    
    if check_file == True:
        print("Great")
        
    else:
        print('dang')
        
    
    # fil = open('/home/ubuntu/environment/final_project/data/'+tick + '.csv', 'w')
    # fil.write("Date,prices\n")
    
    # prcs = []
    # for date in stockDict[key1].keys():
    #     newPrice = float(stockDict[key1][date][key3])
    #     prcs.append(newPrice)
     
    #     fil.write(date + "," + stockDict[key1][date][key3] + "\n")
    
    # fil.close()
    
    # print("This is the mean reversion strategy for "+tick)
    # input()
    # meanRev(prcs,tick)
    # print("\n")
    
    # print("This is the simple moving average strategy for "+tick)
    # input()
    # simpleMoving(prcs,buy,profit)
    # print("\n")
   
    # print("This is the bollinger strategy for "+tick)
    # input()
    # bollinger(prcs,buy,profit)
    # print("\n")
    
    # print("This is the shortsell strategy for "+tick)
    # input()
    # shortsell(prcs,buy,profit)
    # print("\n")
    
    # time.sleep(12)
    
