import boto3
import json
import logging
from datetime import datetime, timedelta

def delay_message(eta, **message):
    client = boto3.client(
        service_name='sqs',
        endpoint_url='https://message-queue.api.cloud.yandex.net',
        region_name='ru-central1'
        )
    queue_url = client.create_queue(QueueName='notify').get('QueueUrl')
    delay = max(min(int((eta-datetime.utcnow()).total_seconds()), 900), 0)
    logging.debug('queue message delay: {} sec'.format(delay))
    logging.debug('message: {}'.format(message))
    client.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps({'eta': eta.isoformat(), 'msg': message}),
        DelaySeconds=delay
    )
