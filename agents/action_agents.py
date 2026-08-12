import psxdata
from psxdata.exceptions import PSXServerError
from db import get_connection

def get_current_price(ticker: str) -> float | None:
    try:
        df = psxdata.stocks(ticker, start="2025-01-01", end="2025-12-31")
        if df.empty:
            return None
        return float(df.iloc[0]["close"])
    except PSXServerError:
        return None

def add_holding(user_id: str, ticker: str, quantity: float, avg_cost: float) -> str:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO holdings (user_id, ticker, quantity, avg_cost) VALUES (%s, %s, %s, %s)",
        (user_id, ticker, quantity, avg_cost)
    )
    connection.commit()
    cursor.close()
    connection.close()
    return f"Added {quantity} shares of {ticker} at avg cost {avg_cost}."

def get_portfolio_value(user_id: str) -> str:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT ticker, quantity, avg_cost FROM holdings WHERE user_id = %s", (user_id,))
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    if not rows:
        return "You don't have any holdings yet."

    total_value = 0.0
    details = []

    for ticker, quantity, avg_cost in rows:
        current_price = get_current_price(ticker)
        if current_price is None:
            details.append(f"{ticker}: price unavailable right now")
            continue
        value = quantity * current_price
        total_value += value
        details.append(f"{ticker}: {quantity} shares @ {current_price} = {value:.2f}")

    summary = "\n".join(details)
    return f"Portfolio value: {total_value:.2f}\n{summary}"