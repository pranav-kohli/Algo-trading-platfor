import csvReader
import time
import threading
import xmlrpc.server
import order
import constants as ct
import user
import random


'''
The MD_Broadcaster reads data from the csv and notifies all the users hooked to it whenever new data is available
5 users are created with their own initial capital and portfolio.
Each user makes its own decision to buy and sell based on the mentioned criteria and sends their order to the OM_Listener
The OM_Listener class sends them to the exchange server
On recieving confirmation from the server, the initial capital and portfolio is updated and data written to a csv file

'''
myServer = xmlrpc.server.SimpleXMLRPCServer((ct.CHostName, ct.CHostPort))
print(time.asctime(), "Server Starts - %s:%s" % (ct.CHostName, ct.CHostPort))
try:
	#using thread to start our server. It will close when the 'main' thread ends or when you press ctrl + C
	myServer.register_function(order.placeOrder, "placeOrder")
	myServer.register_function(order.getOrderStatus, "getOrderStatus")

	threading.Thread(target=myServer.serve_forever, daemon=True).start()
 
	MDReader = csvReader.MD_Broadcaster('stocks.csv')
    #create 5 users which will be notified when new data is read from csv.
    #Each user have their own initial capital and start with an empty portfolio  
	for i in range(3):
	    userx = user.MD_Listener( i + 1, random.randint(1000,10000), {} )
	    MDReader.attach(userx)  #subscribe these users to the market data reader

    #following will be run in threads
	thread_return={'success': False}
	t1 = threading.Thread(target = MDReader.read, args=(thread_return,))
	t1.start()
	
	for user in MDReader.observers:
	    t = threading.Timer(2, user.parseData, args=(thread_return,)) #starts processing after 2 seconds
	    t.start()
		


except KeyboardInterrupt:
    myServer.server_close()
    print(time.asctime(), "Server Stops - %s:%s" % (ct.CHostName, ct.CHostPort))
	



