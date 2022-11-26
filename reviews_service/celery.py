from __future__ import absolute_import, unicode_literals

import os

import django
import kombu
from celery import Celery, bootsteps

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reviews_service.settings')
django.setup()

from users.models import User
from users.serializers import UserSerializer
from rides.models import Ride, Participation
from rides.serializers import RideSerializer, ParticipationSerializer
from utils.celery_utils import *

app = Celery('reviews_service')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# setting publisher
with app.pool.acquire(block=True) as conn:
    exchange = kombu.Exchange(
        name='trawell_exchange',
        type='direct',
        durable=True,
        channel=conn,
    )
    exchange.declare()

    queue_users = kombu.Queue(
        name='users',
        exchange=exchange,
        routing_key='use',
        channel=conn,
        message_ttl=600,
        queue_arguments={
            'x-queue_rides-type': 'classic'
        },
        durable=True
    )
    queue_users.declare()

    queue_reviews = kombu.Queue(
        name='reviews',
        exchange=exchange,
        routing_key='review',
        channel=conn,
        message_ttl=600,
        queue_arguments={
            'x-queue_rides-type': 'classic'
        },
        durable=True
    )
    queue_reviews.declare()


    # setting consumer
    class MyConsumerStep(bootsteps.ConsumerStep):

        def get_consumers(self, channel):
            return [kombu.Consumer(channel,
                                   queues=[queue_reviews],
                                   callbacks=[self.handle_message],
                                   accept=['json'])]

        def handle_message(self, body, message):
            print('Received message: {0!r}'.format(body))
            print(message)

            if body['title'] == 'users':
                try:
                    user = User.objects.get(user_id=body['message']['user_id'])
                    user_data = {
                        'first_name': body['message']['first_name'],
                        'avg_rate': body['message']['avg_rate'],
                        'avatar': body['message']['avatar'],
                    }
                    serializer = UserSerializer(user, data=user_data, partial=True)
                    if serializer.is_valid():
                        serializer.save()

                except User.DoesNotExist:
                    check_and_create_user(body['message'])

            if body['title'] == 'rides.create':
                check_and_create_user(body['message']['driver'])
                create_ride(body['message'])

            if body['title'] == 'rides.create.many':
                for ride in body['message']:
                    check_and_create_user(ride['driver'])
                    create_ride(ride)

            if body['title'] == 'rides.update':
                check_and_create_user(body['message']['ride']['driver'])
                try:
                    ride = Ride.objects.get(ride_id=body['message']['ride']['ride_id'])
                    update_ride(body['message']['ride'], ride)
                except Ride.DoesNotExist:
                    create_ride(body['message']['ride'])

            if body['title'] == 'rides.update.many':
                for instance in body['message']:
                    check_and_create_user(body['message']['ride']['driver'])
                    try:
                        ride = Ride.objects.get(ride_id=instance['ride']['ride_id'])
                        update_ride(body['message']['ride'], ride)
                    except Ride.DoesNotExist:
                        create_ride(instance['ride'])

            if body['title'] == 'rides.cancel':
                check_and_create_user(body['message']['ride']['driver'])
                try:
                    ride = Ride.objects.get(ride_id=body['message']['ride']['ride_id'])
                    update_ride(body['message']['ride'], ride)
                except Ride.DoesNotExist:
                    create_ride(body['message']['ride'])

            if body['title'] == 'rides.cancel.many':
                for ride in body['message']:
                    check_and_create_user(body['message']['ride']['driver'])
                    try:
                        ride = Ride.objects.get(ride_id=ride['ride']['ride_id'])
                        update_ride(body['message']['ride'], ride)
                    except Ride.DoesNotExist:
                        create_ride(ride['ride'])

            if body['title'] == 'participation':
                check_and_create_user(body['message']['ride']['driver'])
                check_and_create_user(body['message']['user'])

                try:
                    ride = Ride.objects.get(ride_id=body['message']['ride']['ride_id'])
                    update_ride(body['message']['ride'], ride)
                except Ride.DoesNotExist:
                    create_ride(body['message']['ride'])

                try:
                    Participation.objects.get(id=body['message']['id'])
                except Participation.DoesNotExist:
                    participation = Participation.objects.create(
                        id=body['message']['id'],
                        ride_id=body['message']['ride']['ride_id'],
                        user_id=body['message']['ride']['driver']['user_id']
                    )
                    participation.save()
            if body['title'] == 'rides.archive':
                print(body['message'])
                rides = body['message']
                for ride in rides:
                    try:
                        ride_obj = Ride.objects.get(ride_id=ride['ride_id'])
                        add_participation_to_ride(ride, ride_obj)
                    except Ride.DoesNotExist:
                        create_history_ride(ride)

            message.ack()


    app.steps['consumer'].add(MyConsumerStep)

    # user_id, email, first_name, avg_rate, avatar
    # ride_id, city_from, city_to, start_date, driver, passengers
    # ride, user
