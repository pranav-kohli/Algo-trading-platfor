
import time
import os


class observable():
    '''
    observer base class to be inherited by csv reader
    '''
    def __init__(self):
        self.observers = [] # maintains a list of observers to be notified when new data comes

    def attach(self, observer):
        if not observer in self.observers:
            self.observers.append(observer)

    def detach(self, observer):
        try:
            self.observers.remove(observer)
        except ValueError:
            pass

    def notify(self):
        for observer in self.observers:
            observer.update(self)


class MD_Broadcaster(observable):
    '''
    Market data reader class. Reads the input from csv file and passed it  for further processing
    '''
    def __init__(self, filename, **kwargs):
        self.path = cwd = os.getcwd() + '\\' + filename
        self.data = [] # a list to hold the parsed data
        return super().__init__(**kwargs)

    def displayCapital(self):
        print('Calling csvReader::displayCapital()')
        for user in self.observers:
            print('Final capital for user {0} is {1}'.format(user.id, user.initialCapital))
            print('Final Portfolio as below ')
            for stock,quantity in user.initialPortfolio.items():
                print('Stock : {0}  Quantity : {1}'.format(stock,quantity))

    def read(self, thread_return):
        '''
        Reads data from a csv file and broadcasts it to the listener class
        '''
        try:
            print('Calling csvReader::read()')
            with open(self.path, "r") as fo:
                start = 0
                #enumerate(fo) uses fo.next, so it doesn't need the entire file in memory.
                #Might be a little slower as the file is read sequentially.
                for i, line in enumerate(fo): 
                    print ('Reading line number {0} with values {1}'.format(start,line))
                    dataList = line.split(',')
                    if start == 0:
                        self.data = dataList
                        self.notify() #broadcast the data to listener class
                        start += 1
                        continue
                    if line == 'the-end,,':
                        print('No more data to be read')
                        self.displayCapital()
                        thread_return['success'] = True
                        return
                        #return -1
                
                    dataList[1] = float(dataList[1])
                    dataList[2] = float(dataList[2])
                    self.data = dataList  #broadcast the data to listener class
                    self.notify()
                    start += 1
                    time.sleep(5) # pause for 5 secs
                    print('Heavy calculations going on')
        except:
            print('Issue in reading the csv file')



