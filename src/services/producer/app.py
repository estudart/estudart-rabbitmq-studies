from src.utils.extensions import rabbit_instance

for i in range(10):
    rabbit_instance.publish(
        'letterbox',
        message=(
            f"This is a new message: {i}"
        )
    )