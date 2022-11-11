import factory.django
import pytz

from users.factories import UserFactory
from . import models


class RideFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Ride

    city_from = factory.Faker('city')
    city_to = factory.Faker('city')
    start_date = factory.Faker('future_datetime', tzinfo=pytz.timezone('Europe/Warsaw'))
    driver = factory.SubFactory(UserFactory)

    @factory.post_generation
    def passengers(self, create, extracted):
        if not create:
            return

        if extracted:
            for passenger in extracted:
                self.passengers.add(passenger)
