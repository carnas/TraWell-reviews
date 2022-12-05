from rides.models import Ride, Participation
from rides.serializers import RideSerializer, RideUpdateSerializer
from users.models import User


def create_ride(message):
    ride, _ = Ride.objects.update_or_create(ride_id=message['ride_id'],
                                            defaults={'city_from': message['city_from']['name'],
                                                      'city_to': message["city_to"]['name'],
                                                      'start_date': message["start_date"],
                                                      'driver_id': message['driver']['user_id']})
    return ride


def add_participation_to_ride(message, ride):
    passengers = message['passengers']
    for passenger in passengers:
        user = User.objects.get(user_id=passenger['user']['user_id'])
        participation, _ = Participation.objects.get_or_create(user=user, ride=ride)


def create_history_ride(message):
    new_ride = Ride.objects.create(
        ride_id=message['ride_id'],
        city_from=message['city_from'],
        city_to=message['city_to'],
        start_date=message['start_date'],
        driver_id=message['driver']
    )
    new_ride.save()
    return new_ride


def update_ride(message, ride):
    try:
        Ride.objects.get(ride_id=message['ride_id'])
    except Ride.DoesNotExist:
        ride_data = {
            'city_from': message['city_from'],
            'city_to': message["city_to"],
            'start_date': message['start_date'],
        }
        serializer = RideUpdateSerializer(ride, data=ride_data, partial=True)
        if serializer.is_valid():
            serializer.save()


def check_and_create_user(message):
    try:
        user = User.objects.get(user_id=message['user_id'])
    except User.DoesNotExist:
        user = User.objects.create(
            user_id=message['user_id'],
            first_name=message['first_name'],
            email=message["email"],
            avg_rate=message["avg_rate"],
            avatar=message["avatar"],
        )
        user.save()
    return user
