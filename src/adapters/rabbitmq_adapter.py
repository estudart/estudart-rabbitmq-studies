import os
import time
from threading import Thread

import pika
from dotenv import load_dotenv

load_dotenv()

class RabbitMQ:
    def __init__(self, connection_type):
        self.user = os.getenv('RABBITMQ_USER', 'user')
        self.password = os.getenv('RABBITMQ_PASSWORD', 'password')
        self.host = os.getenv('RABBITMQ_HOST', 'localhost')
        self.port = int(os.getenv('RABBITMQ_PORT', 5672))

        self.connection_type = connection_type

        self.connection = None
        self.channel = None

        self._connect()

    def _start_keep_alive(self):
        print("Started keep alive thread")
        keep_alive_thread = Thread(target=self.keep_alive, daemon=True)
        keep_alive_thread.start()

    def keep_alive(self):
        while self.connection and self.connection.is_open:
            try:
                self.connection.process_data_events()
            except Exception as err:
                break
            time.sleep(5)

    def _connect(self):
        if self.connection_type == "producer":
            parameters = pika.ConnectionParameters(
                host=self.host,
                heartbeat=10,
                blocked_connection_timeout=5,
                connection_attempts=3,
                retry_delay=5
            )
        else:
            parameters = pika.ConnectionParameters(host=self.host)
            
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

        if self.connection_type == "producer":
            self._start_keep_alive()

    def close(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()

    def consume(self, queue_name, callback):
        print("Starting consuming")
        if not self.channel:
            raise Exception("Connection is not established.")
        self.channel.queue_declare(queue=queue_name)
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

    def publish(self, queue_name, message):
        if not self.channel:
            self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)
        self.channel.basic_publish(exchange='',
                                   routing_key=queue_name,
                                   body=message,
                                   properties=pika.BasicProperties(
                                       delivery_mode=2,  # make message persistent
                                   ))
        print(f"Sent message to queue {queue_name}: {message}")