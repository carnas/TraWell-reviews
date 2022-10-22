import factory.django

from reviews.models import Review
from rides.factories import RideFactory
from users.factories import UserFactory


class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    stars = factory.Faker('pyint', min_value=1, max_value=5)
    description = factory.Faker('text', max_nb_chars=500)
    reviewer = factory.SubFactory(UserFactory)
    rated = factory.SubFactory(UserFactory)
    was_rated_driver = factory.Faker('pybool')
    ride = factory.SubFactory(RideFactory)
