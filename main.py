# -- coding: utf-8 --

import logging
import json
import os

this_file = 'req/bin/activate_this.py'
exec(open(this_file).read(), {'__file__': this_file})

from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, CommandHandler, Filters

import gettext
el = gettext.translation('base', localedir='locales', languages=['ru'])
el.install()

root = logging.getLogger()
root.setLevel(logging.DEBUG)

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=_('Echo: {}').format(update.message.text))

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=_('Notification bot. Will send you a message at given time'))

bot = None
dispatcher = None

def init():
    global dispatcher
    global bot
    bot = Bot(os.environ['TELEGRAM_BOT_API'])
    dispatcher = Dispatcher(bot, None, workers=0, use_context=True)
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.all, echo))
init()

def handler(event, context):
    logging.debug('event: %s'%event)
    body = json.loads(event['body'])

    dispatcher.process_update(Update.de_json(body, bot))

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'isBase64Encoded': False,
        'body': ''
    }

if __name__ == '__main__':
   event = {'httpMethod': 'POST', 'headers': {'Accept-Encoding': 'gzip, deflate', 'Content-Length': '335', 'Content-Type': 'application/json', 'X-Real-Remote-Address': '[91.108.6.67]:56324', 'X-Request-Id': '5b78251c-fecc-4981-9106-0ccd044a4b06', 'X-Trace-Id': 'f16d2ced-c15c-439e-95da-2578d99a52cf'}, 'path': '', 'params': {}, 'multiValueParams': {}, 'pathParams': {}, 'multiValueHeaders': {'Accept-Encoding': ['gzip, deflate'], 'Content-Length': ['335'], 'Content-Type': ['application/json'], 'X-Real-Remote-Address': ['[91.108.6.67]:56324'], 'X-Request-Id': ['5b78251c-fecc-4981-9106-0ccd044a4b06'], 'X-Trace-Id': ['f16d2ced-c15c-439e-95da-2578d99a52cf']}, 'queryStringParameters': {}, 'multiValueQueryStringParameters': {}, 'requestContext': {'identity': {'sourceIp': '91.108.6.67', 'userAgent': ''}, 'httpMethod': 'POST', 'requestId': '5b78251c-fecc-4981-9106-0ccd044a4b06', 'requestTime': '31/Jan/2020:12:06:23 +0000', 'requestTimeEpoch': 1580472383}, 'body': '{"update_id":333238287,\n"message":{"message_id":4,"from":{"id":35243507,"is_bot":false,"first_name":"Dmitry","last_name":"Balabanov","username":"dimonb","language_code":"ru"},"chat":{"id":35243507,"first_name":"Dmitry","last_name":"Balabanov","username":"dimonb","type":"private"},"date":1580472383,"text":"\\u0442\\u0435\\u0441\\u04422"}}', 'isBase64Encoded': False}
   handler(event, None)

