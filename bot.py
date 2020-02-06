import os

from telegram import Bot, Update
from telegram.ext import Dispatcher

bot = None
dispatcher = None

def init():
    global dispatcher
    global bot
    bot = Bot(os.environ['TELEGRAM_BOT_API'])
    dispatcher = Dispatcher(bot, None, workers=0, use_context=True)
init()

def add_handler(handler):
    dispatcher.add_handler(handler)

def process_update(update):
    dispatcher.process_update(Update.de_json(update, bot))

def send_message(**args):
    bot.send_message(**args)
