Algo Trader: Simple Moving Average, Mean Reversion, and Bollinger Bands Strategy

This project is an algorithmic trading system that uses the Simple Moving Average (SMA), Mean Reversion, and Bollinger Bands strategies to trade on the Alpaca paper trading account. The trading system is built using Python and the Alpaca API.

How It Works
The algorithm uses the following strategies to make trading decisions:

Mean Reversion: The meanRev() function takes in a list of prices and a ticker symbol, and it implements a mean reversion strategy. The strategy involves buying a stock when its price is 2% below its 5-day moving average, and selling it when its price is 2% above its 5-day moving average. The function prints out the buy and sell signals and the total profit made, and it also writes the results to a JSON file.

Simple Moving Average: The simpleMoving() function is similar to meanRev(), but it implements a simple moving average strategy instead of a mean reversion strategy. The strategy involves buying a stock when its price is above its 5-day moving average, and selling it when its price is below its 5-day moving average. The function prints out the buy and sell signals and the total profit made, and it also writes the results to a JSON file.

Bollinger Bands: The bollinger() function implements a bollinger band strategy. The strategy involves buying a stock when its price breaks above its upper bollinger band (which is 2 standard deviations above its 5-day moving average), and selling it when its price breaks below its lower bollinger band (which is 2 standard deviations below its 5-day moving average). The function prints out the buy and sell signals and the total profit made, and it also writes the results to a JSON file.

Requirements
To run this project, you will need the following:

Python 3.6 or higher
Alpaca API keys
pandas, numpy, alpaca_trade_api, and matplotlib Python packages
Usage
Clone this repository to your local machine.

Open the config.py file and enter your Alpaca API keys.

Open the main.py file and adjust the SYMBOL and INTERVAL variables to match the stock you want to trade and the timeframe you want to use.

Run the main.py file.

Disclaimer
This project is for educational purposes only and should not be used for real trading without proper testing and risk management. The author is not responsible for any losses incurred while using this software.




