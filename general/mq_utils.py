import os
import pika

SERVER_HOST = os.getenv('SERVER_HOST')
MINDTRACE_SECRET = os.getenv("MINDTRACE_SECRET")
credentials = pika.PlainCredentials("juumii", MINDTRACE_SECRET)
parameters = pika.ConnectionParameters(host=SERVER_HOST, port=5672, credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.basic_qos(prefetch_count=1)

# exchange
knode_event_exchange = "knode_event_exchange"
channel.exchange_declare(exchange=knode_event_exchange, exchange_type='direct', durable=True)

# mqs
update_knode_event_mq = "update_knode_event_mq"
routing_key_update = "update_knode"
channel.queue_declare(queue=update_knode_event_mq, durable=True)
channel.queue_bind(queue=update_knode_event_mq, exchange=knode_event_exchange, routing_key=routing_key_update)

