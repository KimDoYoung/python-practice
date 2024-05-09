from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import requests
import re
# .env 파일 로드
load_dotenv()

def get_dividiend(code):
    url = "https://finance.naver.com/item/main.nhn?code=" + code
    resp = requests.get(url)
    html = resp.text
    soup = BeautifulSoup(html, "html5lib")
    tags = soup.select("#_dvr")
    dividend = tags[0].text
    return dividend


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('안녕하세요! 에코 봇입니다.')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pattern = r'^\d{6}$'
    input_string = update.message.text
    if bool(re.match(pattern, input_string)):
        code = input_string
        dividend = get_dividiend(code)
        await update.message.reply_text(f'{code}의 배당율은 {dividend} 입니다.')
    else:
        await update.message.reply_text(update.message.text)


def main():
    TELEGRAM_BOT_KEY=os.getenv('TELEGRAM_BOT_KEY')
    application = Application.builder().token(TELEGRAM_BOT_KEY).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
