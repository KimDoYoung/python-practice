# telegram_bot.py

import asyncio
import re
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from telegram.error import BadRequest, TelegramError
from backend.app.core.dependency import get_user_service
from backend.app.core.logger import get_logger
logger = get_logger(__name__)

TELEGRAM_BOT_TOKEN = None
TELEGRAM_USER_ID = None
Telebot_Application = None
polling_task = None

async def initialize_telegram_bot():
    global TELEGRAM_BOT_TOKEN, TELEGRAM_USER_ID
    user_service = get_user_service()
    user = await user_service.get_1('kdy987')  # await 추가
    TELEGRAM_BOT_TOKEN = user.get_value_by_key("TELEGRAM_BOT_TOKEN")
    TELEGRAM_USER_ID = user.get_value_by_key("TELEGRAM_USER_ID")    
    logger.debug(f"TELEGRAM_BOT_TOKEN: {TELEGRAM_BOT_TOKEN}, TELEGRAM_USER_ID: {TELEGRAM_USER_ID}")
    return TELEGRAM_BOT_TOKEN, TELEGRAM_USER_ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    from backend.app.background.danta_machine import start_danta_machine
    await start_danta_machine()
    await update.message.reply_text('단타머신 시작합니다.')

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    from backend.app.background.danta_machine import stop_danta_machine
    await stop_danta_machine()
    await update.message.reply_text('단타머신 종료되었습니다.')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pattern = r'^\d{6}$'
    input_string = update.message.text
    if bool(re.match(pattern, input_string)):
        code = input_string
        dividend = 0.00
        await update.message.reply_text(f'{code}의 배당율은 {dividend} 입니다.')
    else:
        await update.message.reply_text(update.message.text)


async def send_message_telegram_user(bot: Bot, chat_id: str, message: str):
    await bot.send_message(chat_id=chat_id, text=message)

async def send_danta_message(message: str):
    global TELEGRAM_BOT_TOKEN, TELEGRAM_USER_ID
    logger.info(f"Sending message to {TELEGRAM_USER_ID}")
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    try:
        await bot.send_message(chat_id=TELEGRAM_USER_ID, text=message)
    except BadRequest as e:
        logger.error(f"BadRequest Error: {e}")
    except TelegramError as e:
        logger.error(f"TelegramError: {e}")

async def polling():
    global polling_task
    await Telebot_Application.updater.start_polling()

async def main():
    global TELEGRAM_BOT_TOKEN, TELEGRAM_USER_ID 
    global Telebot_Application
    global polling_task
    
    await initialize_telegram_bot()

    Telebot_Application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    stop_handler = CommandHandler('stop', stop)

    Telebot_Application.add_handler(start_handler)
    Telebot_Application.add_handler(stop_handler)
    Telebot_Application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    await Telebot_Application.initialize()  # 추가
    await Telebot_Application.start()
    # polling 작업을 별도의 태스크로 실행합니다.
    polling_task = asyncio.create_task(polling())

# 텔레그램 봇 실행 작업
async def start_telegram_bot():
    await main()

# 텔레그램 봇 정지 작업
async def stop_telegram_bot():
    global Telebot_Application
    global polling_task

    if polling_task:
        polling_task.cancel()
        try:
            await polling_task
        except asyncio.CancelledError:
            pass

    if Telebot_Application:
        await Telebot_Application.updater.stop()
        await Telebot_Application.stop()
        await Telebot_Application.shutdown()
        logger.info("텔레그램 봇 종료")

if __name__ == "__main__":
    start_telegram_bot()
