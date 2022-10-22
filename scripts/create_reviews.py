import random

from reviews.factories import ReviewFactory
from rides.models import Ride


def create(amount):
    rides = Ride.objects.all()

    for i in range(amount):
        ride = random.choice(rides)
        passengers = ride.passengers.all()
        if passengers:
            if i % 3 == 0:
                was_rated_driver = False
                reviewer = ride.driver
                rated = random.choice(passengers)
            else:
                was_rated_driver = True
                reviewer = random.choice(passengers)
                rated = ride.driver

            ReviewFactory(reviewer=reviewer, rated=rated, was_rated_driver=was_rated_driver, ride=ride)
