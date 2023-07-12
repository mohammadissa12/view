import random

from place.models import PlaceMixin


def create_places():
    for i in range(1, 10001):
        place_type = random.choice(PlaceMixin.PLACE_TYPE_CHOICES)[0]
        city = "baghdad"
        name = f'Place {i}'
        description = 'fdsfs'
        place_details = 'Place Details'
        phone_number = 777
        short_location = "dasda"
        location = '33.3152, 44.3661'

        place = PlaceMixin(
            place_type=place_type,
            city=city,
            name=name,
            description=description,
            place_details=place_details,
            phone_number=phone_number,
            short_location=short_location,
            location=location
        )


create_places()


def create_users():
    for i in range(1, 10000):
        phone_number = 1000000000 + i  # Generate a unique phone number
        user = User(phone_number=phone_number, is_verified=True)
        user.set_password('password')  # Set a default password for all users
        user.save()


create_users()

city_d="baghdad"
def create_places():
    for i in range(1, 10001):
        place_type = random.choice(PlaceMixin.PLACE_TYPE_CHOICES)[0]
        city=PlaceMixin.city(city_d)
        place = PlaceMixin(place_type=place_type,city=city)
        place.save()


create_places()
