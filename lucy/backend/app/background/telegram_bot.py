import re
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes,MessageHandler, Update, filters
from dotenv import load_dotenv
import os
import requests

# .env 파일 로드
load_dotenv()

TELEGRAM_BOT_KEY = os.getenv('TELEGRAM_BOT_KEY')
bot = Bot(token=TELEGRAM_BOT_KEY)
application = Application.builder().token(TELEGRAM_BOT_KEY).build()

# FastAPI 서버 주소
FASTAPI_SERVER_URL = "http://localhost:8000"

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pattern = r'^\d{6}$'
    input_string = update.message.text
    if bool(re.match(pattern, input_string)):
        code = input_string
        dividend = get_dividend(code)
        await update.message.reply_text(f'{code}의 배당율은 {dividend} 입니다.')
    else:
        await update.message.reply_text(update.message.text)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('안녕하세요! 에코 봇입니다.')

async def stop_auto_trading(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    response = requests.post(f"{FASTAPI_SERVER_URL}/control_job", json={"action": "stop"})
    result = response.json()
    await update.message.reply_text(result['message'])

def start_telegram_bot():
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop-auto-trading", stop_auto_trading))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    start_telegram_bot()
