from fetch_data import fetch_trade_data
import pandas as pd
from connect import connection
import matplotlib.pyplot as plt

conn = connection()
def calculate_sma(df,window):
    return df["t_close"].rolling(window = window).mean()


def generate_signals(df):
    # Calculate moving averages
    df['sma_50'] = calculate_sma(df, 50)
    df['sma_500'] = calculate_sma(df, 500)
    df['sma_20'] = calculate_sma(df, 20)
    df['sma_200'] = calculate_sma(df, 200)
    df['sma_10'] = calculate_sma(df, 10)
    df['sma_5'] = calculate_sma(df, 5)

    # Initialize signals column
    df['signal'] = 'Hold'

    # Buy signal: crossover of 50-day and 500-day moving averages
    df.loc[(df['sma_50'] > df['sma_500']) & (df['sma_50'].shift(1) < df['sma_500'].shift(1)), 'signal'] = 'Buy'

    # Sell signal: crossover of 20-day and 200-day moving averages
    df.loc[(df['sma_20'] < df['sma_200']) & (df['sma_20'].shift(1) > df['sma_200'].shift(1)), 'signal'] = 'Sell'

    # Close buy positions: crossover of 10-day and 20-day moving averages
    df.loc[(df['sma_10'] < df['sma_20']) & (df['sma_10'].shift(1) > df['sma_20'].shift(1)), 'signal'] = 'Close Buy'

    # Close sell positions: crossover of 5-day and 10-day moving averages
    df.loc[(df['sma_5'] > df['sma_10']) & (df['sma_5'].shift(1) < df['sma_10'].shift(1)), 'signal'] = 'Close Sell'

    return df

def calculate_profit_loss(df):
    # Calculate profit/loss based on signals
    df['profit_loss'] = 0
    buy_price = None
    for index, row in df.iterrows():
        if row['signal'] == 'Buy':
            buy_price = row['t_close']
        elif row['signal'] == 'Sell' and buy_price is not None:
            df.loc[index, 'profit_loss'] = row['t_close'] - buy_price
            buy_price = None
    return df


def visualize_trades(df, tablename):
    # Visualize trades
    fig, ax = plt.subplots()
    ax.plot(df['tdate'], df['t_close'], color='black', label='Close Price')
    ax.scatter(df[df['signal'] == 'Buy']['tdate'], df[df['signal'] == 'Buy']['t_close'], color='green', label='Buy', marker='^', lw=3)
    ax.scatter(df[df['signal'] == 'Sell']['tdate'], df[df['signal'] == 'Sell']['t_close'], color='red', label='Sell', marker='v', lw=3)
    ax.legend()
    ax.set_title(f'{tablename} Stock Prices with Buy/Sell Signals')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    
    symbols = ['AAPL','HDB','INRX','JIOFINNS','MARA','TATAMOTORSNS','TSLA']  # List of symbols you want to analyze

    try:
        for symbol in symbols:
            stock_df = fetch_trade_data(symbol)
            stock_df['sma_50'] = stock_df['t_close'].rolling(window=50).mean()
            stock_df['sma_500'] = stock_df['t_close'].rolling(window=500).mean()
            stock_df['sma_20'] = stock_df['t_close'].rolling(window=20).mean()
            stock_df['sma_200'] = stock_df['t_close'].rolling(window=200).mean()
            stock_df['sma_10'] = stock_df['t_close'].rolling(window=10).mean()
            stock_df['sma_5'] = stock_df['t_close'].rolling(window=5).mean()
            stock_df = generate_signals(stock_df)
            stock_df = calculate_profit_loss(stock_df)
            print(stock_df.head())
            visualize_trades(stock_df, symbol)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        try:
            conn.close()
        except Exception as e:
            print(f"Error while closing connection: {str(e)}")