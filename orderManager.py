import constants as ct
import time
import xmlrpc
import pandas as pd


class OM_Listener():
    '''
    Order manager class which places the order

    '''
    def __init__(self, **kwargs):
        self.proxy =  xmlrpc.client.ServerProxy("http://localhost:8000/")
        return super().__init__(**kwargs)

    def validateResponse(self, response):
        if isinstance(response, dict):
            return response
        else:
            print('response returned from server is not in correct format')

    def sendOrderToExchange(self):
        try:
            response = self.proxy.placeOrder()
            self.validateResponse(response)
            orderId, _ = next((v for i, v in enumerate(response.items()) if i == 0)) #fetch the order id 
            return orderId
        except xmlrpc.client.Fault as err:
            print("A fault occurred")
            print("Fault code: %d" % err.faultCode)
            print("Fault string: %s" % err.faultString)
            return ''
        

    def getOrderStatus(self, orderId):
        try:
            response = self.proxy.getOrderStatus(orderId)
            self.validateResponse(response)
            return response[orderId]
        except xmlrpc.client.Fault as err:
            print("A fault occurred")
            print("Fault code: %d" % err.faultCode)
            print("Fault string: %s" % err.faultString)
            return ''


    def placeOrder(self, user, action, stockName, currentPrice):
        '''
        Recievs order from the user and sends it to the exchange server
        After recieving a response, updates the users capital and portfolio and writes to a csv
        '''

        print('Order recieved for  user ID {0} to {1} {2} shares at price {3}'.format(user.id, action, stockName, currentPrice))
        orderId =  self.sendOrderToExchange()
        status = self.getOrderStatus(orderId)

        #updates users capital and portfolio based on this order
        portfolio = user.updatePortFolio(action, status, stockName, orderId, currentPrice)
        capital = user.initialCapital
        #write data to 'userIdPortfolio.csv'..Each user will have its own csv portfolio file
        self.writeDataToCsv(user.id, portfolio, capital)

            
    def writeDataToCsv(self, id, portfolio, capital):
        #create df from the portfolio dict
        portFolio = pd.DataFrame(data = list(portfolio.items()), columns = [ct.CStockName, ct.CQuantity])
        portFolio['Final Capital'] = capital
        print('saving User' + str(id) + 'Portfolio.csv')
        portFolio.to_csv('User' + str(id) + 'Portfolio.csv')

        
        
        
