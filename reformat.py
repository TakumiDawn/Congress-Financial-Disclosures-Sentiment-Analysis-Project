from fileDirectoryCreation import *
from pandas import read_csv

def reformat():
    sp500_path = fileDirectory + '/StockHistory/^GSPC.csv'
    nsaq_path = fileDirectory + '/StockHistory/^IXIC.csv'
    house_path = fileDirectory + '/Congress/houseTransactions.csv'
    senate_path = fileDirectory + '/Congress/senateTransactions.csv'

    sp500_series = read_csv(sp500_path, header=0, parse_dates=[0], skiprows=range(1,17614),
                            usecols= ['Date', 'Close']).set_index(['Date']).dropna()
    nsaq_series = read_csv(nsaq_path, header=0, parse_dates=[0], skiprows=range(1,12336),
                           usecols= ['Date', 'Close']).set_index(['Date']).dropna()

    start_remove = '2020-01-02'
    house_series = read_csv(house_path, header=0, parse_dates=[0],
                            usecols=['transaction_date', 'type', 'amount']).set_index(['transaction_date'])
    house_series = house_series.query('index > @start_remove ').dropna()
    # print(house_series.head(5))
    senate_series = read_csv(senate_path, header=0, parse_dates=[0],
                            usecols=['transaction_date', 'type', 'amount']).set_index(['transaction_date'])
    senate_series = senate_series.query('index > @start_remove ').dropna()
    senate_series['type'] = senate_series['type'].replace(['Purchase','Sale (Full)','Sale (Partial)','Exchange'],
                                                  ['purchase','sale_full','sale_partial', 'exchange'])

    # print(senate_series.head(5))
    return sp500_series, nsaq_series, house_series, senate_series


if __name__ == "__main__":
    reformat()

