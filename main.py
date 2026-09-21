from fastapi import FastAPI
import ccxt

app = FastAPI()
exchange = ccxt.binance()

coins = ["BTC/USDT", "ETH/USDT", "SOL/USDT"]

@app.get("/")
def home():
    return {"status": "Bot Chal Raha Hai"}

@app.get("/signals")
def get_all_signals():
    result = []
    for coin in coins:
        ticker = exchange.fetch_ticker(coin)
        price = ticker['last']
        signal = "BUY" if price > ticker['open'] else "SELL"
        result.append({"coin": coin, "price": price, "signal": signal})
    return result
