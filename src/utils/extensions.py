from src.adapters.rabbitmq_adapter import RabbitMQ

def create_rabbit_instance(connection_type):
    return RabbitMQ(connection_type)