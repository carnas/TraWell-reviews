import factory.django

from users.factories import UserFactory
from . import models


class RideFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Ride

    driver = factory.SubFactory(UserFactory)

    @factory.post_generation
    def passengers(self, create, extracted):
        if not create:
            return

        if extracted:
            for passenger in extracted:
                self.passengers.add(passenger)
