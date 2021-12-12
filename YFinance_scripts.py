import yfinance as yf
from datetime import timedelta, date
import datetime
from tqdm import tqdm
from fileDirectoryCreation import *
from ta.others import *


## Defining variables as global variables 
## (can be used without calling this function directly)
global stockList
if(os.path.exists(fileDirectory + '/Stock_List.csv') != True):
    f = open(fileDirectory + "/Stock_List.csv", "a")
    f.close()

else:
    pass

stockList = pd.read_csv(fileDirectory + '/Stock_List.csv')
stockListLen = len(stockList)

# Date format = "2021-09-01"
today = date.today()
strToday = str(today)
tomorow = today + datetime.timedelta(days=1)
strTomorow = str(tomorow)

def getTodaysStockHistory(daysOffset):
    print('Getting today''s stock history.')
    d = daysOffset
    print('get ticker data')
    #2021-09-30 = "$Y-%m-%d"
    today = date.today() - datetime.timedelta(days= 1)
    strToday = today.strftime("%Y-%m-%d")

    tomorow = date.today() - datetime.timedelta(days= 0)
    strTomorow = tomorow.strftime("%Y-%m-%d")
    listLen = len(stockList)
    arr = stockList['Symbol'].to_numpy()
    for i in tqdm(arr.T, ascii=True, bar_format='{l_bar}{bar:30}{r_bar}{bar:-30b}'):
        #print(str(i)+'/'+str(listLen)+' ' + stockList['Symbol'][i])
        try:
            stockTickers = yf.download(i, start=strToday, end=strTomorow, interval = "1m" )
            stockTickers['ABV'] =  i
            stockTickers.to_csv(fileDirectory + '/ByMinuteHistory/'+i+'_'+strTomorow+'.csv')
        except:
            pass

def getStockHistory():
    print('Getting the full history of the stock market.')
    arr = stockList['Symbol'].to_numpy()
    for i in tqdm(arr.T, ascii=True, bar_format='{l_bar}{bar:30}{r_bar}{bar:-30b}'):
        try:
            stock = yf.Ticker(i)
            hist = stock.history(period="max")
            hist.to_csv(fileDirectory + '/StockHistory/'+i+'.csv')
        except:
            pass

def main():
    getStockHistory()

if __name__ == "__main__":
    main()


