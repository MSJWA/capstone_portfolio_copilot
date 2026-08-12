import psxdata

#df = psxdata.stocks("LUCK", start="2025-01-01", end="2025-12-31")
#print(df.head())

#kse100 = psxdata.tickers(index="KSE100")
#print(kse100)

df = psxdata.stocks("FAKETICKER123", start="2025-01-01", end="2025-12-31")
print(df)

from psxdata.exceptions import PSXServerError

def get_current_price(ticker: str) -> float | None:
    try:
        df = psxdata.stocks(ticker, start="2025-01-01", end="2025-12-31")
        if df.empty:
            return None
        return df.iloc[0]["close"]
    except PSXServerError:
        return None