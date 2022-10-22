import factory.django

from . import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User
