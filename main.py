from YFinance_scripts import *
from congress import *
from reformat import *
import plotly.express as px
from statsmodels.tsa.stattools import grangercausalitytests
import matplotlib.pyplot as plt
import seaborn as sns

global fileDirectory

fileDirectory = 'S:/Stocks'

def setup():
    try:
        os.mkdir(fileDirectory)
    except:
        pass

    try:
        os.mkdir(fileDirectory + '/StockHistory/')
    except:
        pass

    # file = urlopen('all_tickers.txt')
    # stockDF = pd.read_csv(file, sep=" ", header=None, names=["Symbol"])
    # stockDF.to_csv(fileDirectory + '/Stock_List.csv', index=False)
    # print(stockDF)

    # We use proloaded Stock_List.csv file instead,
    # because we only need to use S&P500 (^GSPC) and(^IXIC)
    def grangers_causation_matrix(data, variables, test=test_method, verbose=False):
        df = pd.DataFrame(np.zeros((len(variables), len(variables))), columns=variables, index=variables)
        for c in df.columns:
            for r in df.index:
                test_result = grangercausalitytests(data[[r, c]], maxlag=maxlag, verbose=False)
                p_values = [round(test_result[i + 1][0][test][1], 4) for i in range(maxlag)]
                if verbose: print(f'Y = {r}, X = {c}, P Values = {p_values}')
                min_p_value = np.min(p_values)
                df.loc[r, c] = min_p_value
        df.columns = [var + '_x' for var in variables]
        df.index = [var + '_y' for var in variables]
        return df

# test
def grangers_causation_matrix(data, variables, test='ssr_chi2test', verbose=False):
    df = pd.DataFrame(np.zeros((len(variables), len(variables))), columns=variables, index=variables)
    for c in df.columns:
        for r in df.index:
            test_result = grangercausalitytests(data[[r, c]], maxlag=maxlag, verbose=False)
            p_values = [round(test_result[i + 1][0][test][1], 4) for i in range(maxlag)]
            if verbose: print(f'Y = {r}, X = {c}, P Values = {p_values}')
            min_p_value = np.min(p_values)
            df.loc[r, c] = min_p_value
    df.columns = [var + '_x' for var in variables]
    df.index = [var + '_y' for var in variables]
    return df

def main():
    setup()

    # only need to get data for S&P500 (^GSPC) and nasdaq (^IXIC)
    print('Getting S&P500 (^GSPC) and nasdaq (^IXIC) history data')
    getStockHistory()
    print('Getting House Transactions data')
    getHouseTransactions()
    print('Getting Senate Transactions data')
    getSenateTransactions()

    # clean and reformat data
    sp500_series, nsaq_series, house_series, senate_series = reformat()
    index_df = pd.concat([sp500_series, nsaq_series],axis=1).set_axis(['S&P 500', 'NASDAQ'], axis=1, inplace=False)
    # print(sp500_series.shape)
    print(index_df.shape)
    print(index_df.head(10))

    # Visualize the Time Series
    fig = px.line(index_df)
    fig.update_yaxes(matches=None)
    fig.show()

    print(house_series.shape)
    print(house_series.head(5))
    print(senate_series.shape)
    print(senate_series.head(5))


    # Granger Causality Test
    maxlag = 15
    test_method = 'ssr_chi2test'
    # grangers_causation_matrix(df_train_transformed, variables=df_train_transformed.columns)




if __name__ == "__main__":
    main()