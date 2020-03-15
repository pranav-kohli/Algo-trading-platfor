import orderManager
import pandas as pd
import time
import constants as ct


class MD_Listener():
    '''
    Market data Listener class. Fetches the data from reader class and then validates it.
    If data is correct proceeds to calculate whether it should be a buy or sell trade and
    accordingly invokes the order manager class
    '''
    def __init__(self, id, initCapital, initialPortfolio, **kwargs):
        self.df = pd.DataFrame(columns = [ct.CStockName, ct.CStockClosePrice, ct.CStockCurrentPrice])
        self.id = id
        self.initialCapital = initCapital
        self.initialPortfolio = initialPortfolio # dictionary of stock names and quantity held
        return super().__init__(**kwargs)

    def update(self, observable):
        '''
        updates each users own set of data cache as new data is recieved from the csv reader class
        '''
        print('Calling user::update()')
        self.data = observable.data #reda the broadcasted data from the MD_Broadcaster obj
        #If its the first record validate data headers
        if isinstance(self.data[1], str):
            self.validateHeader()
        else:
            if self.validateData() == 1:
                self.df.loc[len(self.df) ] = self.data #append newly recieved data to existing data

    
    def parseData(self, thread_return):
        '''
        This function is the starting point for the user to place his/her orders
        Each users function wold be called in a thread from the main program so all the orders can be processed parallelly
        '''
        print('Calling user::parseData()')
        #Place the order
        while True: #simple event loop
            time.sleep(5) # pause for 5 secs
            if thread_return['success']: #break when csv readers reaches the end
                break
            self.BuyOrSell()
            

    def validateHeader(self):
        #check header
        if len(self.data) == 3 and isinstance(self.data[0],str) and isinstance(self.data[1],str) and isinstance(self.data[2],str):
            print('data header validated for user {0}'.format(self.id))
            return
        print('data header validation failed for user {0}'.format(self.id))



    def validateData(self):
        #check header
        validate = 1
        if len(self.data) != 3 or len(self.data) == 0:
            print('Wrong data received. The data should be Stock Name and Stock Close price and Stock current price only')
            validate = -1
        if not isinstance(self.data[0],str):
            print("First column should be stock name in string format")
            validate = -1
        if not isinstance(self.data[1],float):
            print("second column should be stock close price in float format")
            validate = -1
        if not isinstance(self.data[2],float):
            print("third column should be current stock price in float format")
            validate = -1

        if validate == 1:
            print('data validation is a success for user {0}'.format(self.id))
        else:
            print('data validation failed for user {0}'.format(self.id))
        return validate

    def buy(self, currentPrice, stockName, orderId):
        if self.initialCapital >= currentPrice:
            quantity = int(self.initialCapital/currentPrice)
            print('Buy successful for stock : {0} for quantity : {1} at price : {2} for order ID {3}'.format(stockName, quantity, currentPrice, orderId))

            #update the current portfolio
            if stockName in self.initialPortfolio:
                self.initialPortfolio[stockName] += quantity
            else:
                self.initialPortfolio[stockName] = quantity

            #update initial capital
            self.initialCapital -= (quantity * currentPrice)
        else:
            print("Risk management check failed. You dont have enough capital to buy shares.")
            print("Sell some n get some!!")

        

    def sell(self, currentPrice, stockName, orderId):
        if stockName in self.initialPortfolio and self.initialPortfolio[stockName] > 0:
            sellQuantity = self.initialPortfolio[stockName]
                    
            print('Sell successful for stock : {0} for quantity : {1} at price : {2} for order ID {3}'.format(stockName, sellQuantity, currentPrice, orderId))

            #update stock quantity to 0 as we plan to sell all
            self.initialPortfolio[stockName] = 0

            #update initial capital
            self.initialCapital += (sellQuantity * currentPrice)

        else: #you dont own the shares
            print('We dont have {0} shares to sell'.format(stockName))


    def BuyOrSell(self):
        print('Calling user::BuyOrSell()')
        SMA = self.calculateAverages( 5)
        LMA = self.calculateAverages( 30)
        
        if SMA < LMA:
            action = ct.CSell
        else:
            action = ct.CBuy

        stockName = self.df[ct.CStockName][0]
        currentPrice = self.df[ct.CStockCurrentPrice].iloc[len(self.df)-1]
        orderInitiater = orderManager.OM_Listener()
        order = orderInitiater.placeOrder(self, action, stockName, currentPrice)
        #orderId, orderStatus = next((v for i, v in enumerate(order.items()) if i == 0)) #fetch the order id and order status 
        #self.updatePortFolio(action, orderStatus, stockName, orderId, currentPrice) 
        

    def calculateAverages(self, dataPoints):
        '''
        calculates average of last n data points 
        SMA : 5 data points
        LMA : 30 data points
        '''
        slicedDf = self.df.tail(dataPoints) 
        return slicedDf[ct.CStockClosePrice].mean()

    def updatePortFolio(self, action, orderStatus, stockName, orderId, currentPrice):
        print('Calling user::updatePortFolio()')
        if orderStatus == ct.CPass:
            #currentPrice = self.df[ct.CStockCurrentPrice].iloc[len(self.df)-1]
            if action == ct.CBuy :
                self.buy( currentPrice, stockName, orderId)
            else:  # if sell
                self.sell(currentPrice, stockName, orderId)

        else: #order failed
            print('Order ID {0} to {1} {2} shares failed'.format(orderId, action, stockName))

        return self.initialPortfolio
