# -- coding: utf-8 --

import init #should be first, activation virtualenv here

import logging
import json
import re
import bot
import sqs
import os

import arrow
from dateutil import tz
from datetime import datetime, timedelta
from telegram.ext import CommandHandler, MessageHandler, Filters
from rutimeparser import parse, get_last_clear_text

def start(update, context):
    bot.send_message(chat_id=update.effective_chat.id, text=_('''Notification bot. Will send you a message at given time
Format: YYYY-MM-DD HH:MM <message>'''))
bot.dispatcher.add_handler(CommandHandler('start', start))

RE_MESSAGE = re.compile('(\d\d\d\d[-]\d\d[-]\d\d +\d\d[:]\d\d) +(.*)', re.MULTILINE)
def message(update, context):
    eta, text = None, None

    mo = RE_MESSAGE.match(update.message.text)
    if mo:
        eta = arrow.get(arrow.get(mo.group(1)).datetime, tz.gettz())
        text = mo.group(2)
    else:
        try:
            eta = arrow.get(parse(update.message.text, allowed_results=(datetime,), tz=os.environ['TZ']))
            text = get_last_clear_text(update.message.text)
        except:
            logging.exception('error parsing date')
    logging.debug('eta: %s'%eta)
    logging.debug('text: %s'%text)

    if text:
        sqs.delay_message(
            eta = eta.to('UTC').naive,
            text = text,
            chat_id = update.effective_chat.id,
            reply_to_message_id = update.message.message_id,
            quote = True
        )
        bot.send_message(
            text = _('will notify you at: %s')%eta.format(),
            chat_id = update.effective_chat.id,
            reply_to_message_id = update.message.message_id,
            quote = True
        )
    else:
        start(update, context)
bot.dispatcher.add_handler(MessageHandler(Filters.all, message))

def telegram(event, context):
    logging.debug('event: %s'%event)

    body = json.loads(event['body'])
    bot.process_update(body)

    return {'statusCode': 200}

def notify(event, context):
    logging.debug('event: %s'%event)

    for msg in event['messages']:
        body = json.loads(msg['details']['message']['body'])
        eta = datetime.fromisoformat(body['eta'])
        if eta <= datetime.utcnow():
            bot.send_message(**body['msg'])
        else:
            sqs.delay_message(eta, **body['msg'])

    return {'statusCode': 200}


if __name__ == '__main__':
    event = {'httpMethod': 'POST', 'headers': {'Accept-Encoding': 'gzip, deflate', 'Content-Length': '335', 'Content-Type': 'application/json', 'X-Real-Remote-Address': '[91.108.6.67]:56324', 'X-Request-Id': '5b78251c-fecc-4981-9106-0ccd044a4b06', 'X-Trace-Id': 'f16d2ced-c15c-439e-95da-2578d99a52cf'}, 'path': '', 'params': {}, 'multiValueParams': {}, 'pathParams': {}, 'multiValueHeaders': {'Accept-Encoding': ['gzip, deflate'], 'Content-Length': ['335'], 'Content-Type': ['application/json'], 'X-Real-Remote-Address': ['[91.108.6.67]:56324'], 'X-Request-Id': ['5b78251c-fecc-4981-9106-0ccd044a4b06'], 'X-Trace-Id': ['f16d2ced-c15c-439e-95da-2578d99a52cf']}, 'queryStringParameters': {}, 'multiValueQueryStringParameters': {}, 'requestContext': {'identity': {'sourceIp': '91.108.6.67', 'userAgent': ''}, 'httpMethod': 'POST', 'requestId': '5b78251c-fecc-4981-9106-0ccd044a4b06', 'requestTime': '31/Jan/2020:12:06:23 +0000', 'requestTimeEpoch': 1580472383}, 'body': '{"update_id":333238287,\n"message":{"message_id":4,"from":{"id":35243507,"is_bot":false,"first_name":"Dmitry","last_name":"Balabanov","username":"dimonb","language_code":"ru"},"chat":{"id":35243507,"first_name":"Dmitry","last_name":"Balabanov","username":"dimonb","type":"private"},"date":1580472383,"text":"2020-02-04 16:00 hello"}}', 'isBase64Encoded': False}
    telegram(event, None)
    event = {'messages': [{'event_metadata': {'event_id': 'efe53d99-2873e4fb-36f3941b-4744cae', 'event_type': 'yandex.cloud.events.messagequeue.QueueMessage', 'created_at': '2020-02-04T09:50:12.720Z', 'tracing_context': None, 'cloud_id': 'b1genohq7najdbeeml2r', 'folder_id': 'b1gd54hhts9a44gouqg9'}, 'details': {'queue_id': 'yrn:yc:ymq:ru-central1:b1gd54hhts9a44gouqg9:notify', 'message': {'message_id': 'efe53d99-2873e4fb-36f3941b-4744cae', 'md5_of_body': 'aae408b4d8c785ccefc813c24f1ba5c2', 'body': '{"eta": "2020-02-04T09:50:42.074582", "msg": {"text": "\\u042d\\u0445\\u0445\\u043e: \\u0442\\u0435\\u0441\\u04422", "chat_id": 35243507, "reply_to_message_id": 4, "quote": true}}', 'attributes': {'ApproximateFirstReceiveTimestamp': '1580811438331', 'ApproximateReceiveCount': '13', 'SentTimestamp': '1580809812720'}, 'message_attributes': {}, 'md5_of_message_attributes': ''}}}]}
    notify(event, None)
