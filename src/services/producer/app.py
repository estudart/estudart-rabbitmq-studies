from src.utils.extensions import create_rabbit_instance

rabbit_instance = create_rabbit_instance('producer')

while True:
    user_message = input(f"Type new message: ")
    rabbit_instance.publish(
        'letterbox',
        message=(
            f"This is a new message: {user_message}"
        )
    )