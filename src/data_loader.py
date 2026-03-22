import yfinance as yf
import pandas as pd

TICKERS = {
    "BTC/USD": "BTC-USD",
    "ETH/USD": "ETH-USD",
}

START_DATE = "2018-01-01" 
END_DATE = "2026-01-01"

def load_fx_data(tickers: dict = TICKERS, start_date: str = START_DATE, end_date: str = END_DATE) -> pd.DataFrame:
    frames = {}
    for name, ticker in tickers.items():
        df = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True)
        frames[name] = df["Close"].squeeze()
        
    data = pd.DataFrame(frames).dropna()
    data.index.name = "Date"
    return data

def load_returns(data: pd.DataFrame) -> pd.DataFrame:
    return data.pct_change().dropna()

if __name__ == "__main__":
    df = load_fx_data()
    print(df.tail())
    print(f"\nЗагружено строк: {len(df)}")
