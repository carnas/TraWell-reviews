from django.db import models

from rides.models import Ride
from users.models import User


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    stars = models.IntegerField()
    description = models.CharField(max_length=500, null=True, blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='reviewer')
    rated = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rated')
    was_rated_driver = models.BooleanField()
    ride = models.ForeignKey(Ride, on_delete=models.DO_NOTHING)

