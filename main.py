from fastapi import FastAPI
import ccxt
import os
import asyncio
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

app = FastAPI()
exchange = ccxt.binance()

coins = ["BTC/USDT", "ETH/USDT", "SOL/USDT"]

@app.get("/")
def home():
    return {"status": "Bot Chal Raha Hai - Faisal Bhai"}

@app.get("/signals")
def get_all_signals():
    result = []
    for coin in coins:
        try:
            ticker = exchange.fetch_ticker(coin)
            price = ticker['last']
            # Simple logic: agar 24h se upar hai to BUY
            signal = "BUY" if price > ticker['open'] else "SELL"
            result.append({"coin": coin, "price": price, "signal": signal})
        except Exception as e:
            result.append({"coin": coin, "error": str(e)})
    return result

# --- Telegram Part ---
TOKEN = os.getenv("TELEGRAM") or os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot Active hai! ✅\n /signals likho to price check kar sakte ho.\n\nYe bot ab 24 ghante chalega!")

async def signals_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "📊 Live Signals:\n\n"
    data = get_all_signals()
    for item in data:
        text += f"{item['coin']}: {item.get('price')} - {item.get('signal','-')}\n"
    await update.message.reply_text(text)

def run_bot():
    if not TOKEN:
        print("TELEGRAM Token nahi mila")
        return
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("signals", signals_cmd))
    print("Telegram Bot Polling Started...")
    application.run_polling()

# Bot ko background me chalao taake FastAPI bhi chalta rahe
threading.Thread(target=run_bot, daemon=True).start()
