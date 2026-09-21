from fastapi import FastAPI
import ccxt
import os
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import uvicorn

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
            signal = "BUY" if price > ticker['open'] else "SELL"
            result.append({"coin": coin, "price": price, "signal": signal})
        except Exception as e:
            result.append({"coin": coin, "error": str(e)})
    return result

TOKEN = os.getenv("TELEGRAM") or os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot Active hai! ✅ /signals likho")

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

threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
