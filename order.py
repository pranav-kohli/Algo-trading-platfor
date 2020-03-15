import random
import time
import constants as ct

orderCache = 0
orderStatusDict = {}

def placeOrder():
    '''
    This func is run on the server 
    '''
    rn = random.randint(1,10)
    #print('Order recieved for {0} {1}'.format(self.action, self.stockName))
    time.sleep(3)
    print('Please wait while your order is being processed at the Exchange')
    global orderCache
    global orderStatusDict
    orderCache += 1
    if rn % 2 == 0:
        orderStatusDict[str(orderCache)] =  ct.CPass
        #return {str(orderCache) : ct.CPass}
    else:
        orderStatusDict[str(orderCache)] =  ct.CFail
        #return {str(orderCache) : ct.CFail}
    return {str(orderCache) : ''}



def getOrderStatus(orderId):
    global orderStatusDict
    if orderId in orderStatusDict:
        status = orderStatusDict[orderId]
    else:
        print('Order Id {0} is not in system. Please send correct order ID'.format(orderId))
        status = 'Error'
    return {orderId : status}
