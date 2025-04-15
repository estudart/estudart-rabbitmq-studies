from src.utils.extensions import create_rabbit_instance



def callback(ch, method, properties, body):
    print(body)

rabbit_instance = create_rabbit_instance('consumer')
rabbit_instance.consume('letterbox', callback)