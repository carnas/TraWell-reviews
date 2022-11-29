import random

from statistics import mean

from reviews.factories import ReviewFactory
from reviews.models import Review
from reviews_service import tasks
from reviews_service.celery import queue_users
from rides.models import Ride
from users.serializers import UserSerializer


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

            new_rated_average_rate = calculate_user_avg_rate(rated)
            rated.avg_rate = new_rated_average_rate
            rated.save()

            tasks.publish_message(UserSerializer(rated).data, 'avg_change', queue_users, 'use')


def calculate_user_avg_rate(rated):
    reviews = Review.objects.filter(rated=rated)
    rates = map(lambda review: review.stars, reviews)
    avg_rate = mean(rates)

    return avg_rate
