Algoritmic Trading Platform 

Python Version : 3.5(Visual studio)

Libraries used :- 
random,
time,
xmlrpc,
pandas,
threading,

Instructions

Copy the project to a path of your choice
Open command prompt
type 'python Algo_trading_platform.py'
Happy trading



Flow: 
After running the above command, the server is started.
The program reads stock quotes from a file called stocks.csv(included in the project)
Data validation is performed on the market data and action is determined whether to buy or sell
The order is then passed on to the exchange server which determines whether it is successfull or failed.
The exchange returns appropriate status to the caller
