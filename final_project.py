import requests
import json

import numpy as np
import os
import time
import alpaca_trade_api as tradeapi
import os.path
import csv

#Connecting info for Alpaca
api_key = 'PK6CZ36K8ZZ98TOXPKUB'
api_secret = 'R5E1zku39OCuYFVZHleab4lyHPWofdbeaDUbRqgb'
base_url = 'https://paper-api.alpaca.markets'

api = tradeapi.REST(api_key, api_secret, base_url,
api_version='v2')

def meanRev(prcs, ticker): # pass in a list of prices and the ticker for the trade
    reversed(prcs) #make the last day in the list the current day
    buy = 0
    profit = 0
    start=time.time()
    days = 5
    i = 0
    
    for p in prcs: # iterate through my prices
        
        if i >= days: #have at least 5 days to calculate average
            avg = np.mean(prcs[i-days:i]) #calculate the mean
            
            if p < avg * .98 and buy == 0: #implement mean reversion strategy
                buy = p #set buy = the price that we paid
                print("buying: ", p)
                
                
                if i == len(prcs)-1:#check to see if it's the current date
                    print("You should buy this stock today")
                    #put in a market buy order through alpaca
                    api.submit_order(
                        symbol = ticker,
                        qty=2,
                        side='buy',
                        type='market',
                        time_in_force='gtc'
                        )
                    
            elif p > avg * 1.02 and buy != 0:#continue implementing mean reversion
                profit += p - buy #calculate profit
                buy = 0
                print("selling at: ", p)
                
                if i == len(prcs)-1:#check to see if it's the last day 
                    print("You should sell this stock today")
                    #put in a market sell order through alpaca
                    api.submit_order(
                        symbol = ticker,
                        qty=2,
                        side='sell',
                        type='market',
                        time_in_force='gtc'
                        )
                        
            else:
                pass
        
        i += 1
    
    print('\n')

    results = {"Mean Reversion": ticker,
            "Total Profit": profit,
            "Returns": profit/prcs[0],
            "total time": time.time() - start}
    
    for key, value in results.items():
        print(key + ": " + str(value))
        
    with open('/home/ubuntu/environment/final_project/results.json', 'a') as f:
        
        json.dump(results, f, indent=4)
        
        f.write('\n')
    
def simpleMoving(prcs,ticker):
    reversed(prcs)
    buy = 0
    profit = 0
    start=time.time()
    days = 5
    i = 0

    for p in prcs:#iterate through the prices
        
        if i >= days:# iterate through my prices
            avg = np.mean(prcs[i-days:i])#have at least 5 days to calculate average
            
            if p > avg and buy == 0:#implement simple moving average
                buy = p
                print("buying: ", p)
                
                if i == len(prcs)-1:#check to see if it's the last day 
                    print("You should buy this stock today")
                    #put in a market buy order through alpaca
                    api.submit_order(
                        symbol = ticker,
                        qty=2,
                        side='buy',
                        type='market',
                        time_in_force='gtc'
                        )
            
            elif p < avg and buy != 0:#continue simple moving average
                profit += p - buy
                buy = 0
                print("selling at: ", p)
                
                if i == len(prcs)-1:#check to see if it's the last day 
                    print("You should sell this stock today")
                    #put in a market sell order through alpaca
                    api.submit_order(
                        symbol = ticker,
                        qty=2,
                        side='sell',
                        type='market',
                        time_in_force='gtc'
                        )
            
            else:
                pass
        
        i += 1
    
    print('\n')

    results = {"Simple Moving Average": ticker,
            "Total Profit": profit,
            "Returns": profit/prcs[0],
            "total time": time.time() - start}
    
    for key, value in results.items():
        print(key + ": " + str(value))
        
    with open('/home/ubuntu/environment/final_project/results.json', 'a') as f:
        
        json.dump(results, f, indent=4)
        
        f.write('\n')
        
        
def bollinger(prcs,ticker):
    reversed(prcs)
    start=time.time()
    days = 5
    i = 0
    buy = 0
    profit = 0
    sell = 0
    numShortSells = 0
    
    for p in prcs:
        
        if i >= days:# iterate through my prices
            avg = np.mean(prcs[i-days:i])#have at least 5 days to calculate average
            
            if p > avg * 1.02 and buy == 0:#implement bollinger strategy
                buy = p
                print("buying: ", p)
                
                if i == len(prcs)-1:#check to see if it's the last day
                    print("You should buy this stock today")
                    #put in a market buy order through alpaca
                    api.submit_order(
                        symbol = ticker,
                        qty=2,
                        side='buy',
                        type='market',
                        time_in_force='gtc'
                        )
            
            elif p < avg * .98 and buy != 0:#continue bollinger strategy
                profit += p - buy
                buy = 0
                print("selling at: ", p)
                
                if i == len(prcs)-1:#check to see if it's the last day 
                    print("You should sell this stock today")
                    #put in a market sell order through alpaca
                    api.submit_order(
                        symbol = ticker,
                        qty=2,
                        side='sell',
                        type='market',
                        time_in_force='gtc'
                        )
                        
            elif p < avg * .98 and sell == 0:#implement short sell method
                sell = p
                print("short selling: ", p)
                numShortSells +=1 #keep track of total short sells
                
                if i == len(prcs)-1:#check to see if it's the last day 
                    print("You should short sell this stock today")
                    #put in a short sell market order
                    api.submit_order(
                        symbol=ticker,
                        qty=2,
                        side='sell',
                        type='market',
                        time_in_force='gtc'
                    )
            
            elif p > avg * 1.02 and sell != 0:#continue imlementing short sell
                profit += sell - p # calculate profit
                sell = 0 
                print("buying at: ", p)
                
                if i == len(prcs)-1:#check to see if it's the last day 
                    print("You should buy to cover your short position today")
                    #put in a short sell market buy order to cover position
                    api.submit_order(
                        symbol=ticker,
                        qty=2,
                        side='buy',
                        type='market',
                        time_in_force='gtc'
                    )
            
            else:
                pass
        
        i += 1
    
    print('\n')
    
    results = {"Bollinger": ticker,
            "Total Profit": profit,
            "Number of Short Sells":numShortSells,
            "Returns": profit/prcs[0],
            "total time": time.time() - start}
    
    for key, value in results.items():
        print(key + ": " + str(value))
        
    with open('/home/ubuntu/environment/final_project/results.json', 'a') as f:
        
        json.dump(results, f, indent=4)
        
        f.write('\n')

# --------------------------------------------------------------------------------
ticker = ['IBM','KO','MSFT','AMZN','ABNB','ADBE','TSLA','AMC', 'ZI','DIS']# tickers we want to trade
# ticker = ['IBM','MSFT','KO']

for tick in ticker: #loop through tickers

    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol='+tick+'&outputsize=full&apikey=KP79NZ9ITS60M0LM'#pull historical data from alpaca
    
    request = requests.get(url) #create a request object
   
    stockDict = json.loads(request.text) #converts url to a python dictionary
  
    key1 = "Time Series (Daily)"
    key3 = "5. adjusted close"
    prcs = []
    
    existFile = '/home/ubuntu/environment/final_project/data/'+tick+'.csv' 
    check_file = os.path.exists(existFile) #checks to see if the file path exist
    
    if check_file == True: #if the file path exists then append new data

        csv_file = open(existFile, 'r')#opens the file path in read mode
        lines = csv_file.readlines()#creates a list
        last_date = lines[-1].split(",")[0] # gets the last date of our current data
    
        new_lines = []
        for date in stockDict[key1]:
            if date == last_date:
                break
            print(date + "," + stockDict[key1][date][key3]) #print key, value
            new_lines.append(date + "," + stockDict[key1][date][key3]+"\n")
            
        new_lines = new_lines[::-1]
        
        csv_file = open(existFile, 'a')
        csv_file.writelines(new_lines)
        csv_file.close()
     
        mycsv_file = open('/home/ubuntu/environment/final_project/data/'+tick + '.csv', 'r')#opens the file path in read mode
        lines = mycsv_file.readlines()[1:] #creates a list starting from the second line of the list
        
        for line in lines:#iterates through the lines
            newPrice = float(line.split(",")[1].strip()) #retrieves the price
            prcs.append(newPrice) #appends the price to the prcs list

    else: #if it's a new file path
        fil = open('/home/ubuntu/environment/final_project/data/'+tick + '.csv', 'w') #write the new file path
        fil.write("Date,prices\n") #create the headers in line one
        
        for date in reversed(list(stockDict[key1].keys())):#iterate through the dates
            newPrice = float(stockDict[key1][date][key3]) #retrieve the price value
            prcs.append(newPrice) #appends the prices to the prcs list
     
            fil.write(date + "," + stockDict[key1][date][key3] + "\n")#writes the dates and the prices to the new file
    
        fil.close() #closes the file
    
    print("This is the mean reversion strategy for "+tick)
    meanRev(prcs,tick)
    print("\n")
    
    print("This is the simple moving average strategy for "+tick)
    simpleMoving(prcs,tick)
    print("\n")
   
    print("This is the bollinger strategy for "+tick)
    bollinger(prcs,tick)
    print("\n")
    
    time.sleep(12)
    
  # json.dump(stockDict, open(ticker+".json", "w"), indent = 4)# save dictionary to json file