from datetime import datetime

from reviews.models import Review
from reviews_service import tasks
from reviews_service.celery import queue_users
from rides.models import Ride
from scripts.create_reviews import calculate_user_avg_rate
from users.models import User
from users.serializers import UserSerializer

reviews = [
    {'stars': 3,
     'description': 'lalalalala',
     'was_rated_driver': True,
     'created_on': datetime.now(),
     'reviewer_email': 'anna.nowak@wp.pl',  # must be in db
     'rated_email': 'anonymous@gmail.com',  # must be in db
     'ride_id': 1}  # must be in db
]


def create_manual_reviews(reviews):
    for review in reviews:
        reviewer = User.objects.get(email=review['reviewer_email'])
        rated = User.objects.get(email=review['rated_email'])
        ride = Ride.objects.get(ride_id=review['ride_id'])
        new_review = Review.objects.create(stars=review['stars'],
                                           description=review['description'],
                                           was_rated_driver=review['was_rated_driver'],
                                           created_on=review['created_on'],
                                           reviewer=reviewer,
                                           rated=rated,
                                           ride=ride)
        new_review.save()

        new_rated_average_rate = calculate_user_avg_rate(rated)
        rated.avg_rate = new_rated_average_rate
        rated.save()

        tasks.publish_message(UserSerializer(rated).data, 'avg_change', queue_users, 'use')


create_manual_reviews(reviews)