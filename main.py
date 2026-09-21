import os
import asyncio
import requests
from fastapi import FastAPI
from telegram import Bot
import threading
import time

app = FastAPI()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
bot = Bot(token=TOKEN) if TOKEN else None

@app.get("/")
def home():
    return {"status": "Bot is Running"}

def get_btc_price():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
        return r.json()['price']
    except:
        return None

def background_bot():
    while True:
        try:
            if bot and CHAT_ID:
                price = get_btc_price()
                if price:
                    msg = f"BTC Price: ${price} - Bot ACTIVE"
                    asyncio.run(bot.send_message(chat_id=CHAT_ID, text=msg))
            time.sleep(3600)
        except:
            time.sleep(60)

threading.Thread(target=background_bot, daemon=True).start()
