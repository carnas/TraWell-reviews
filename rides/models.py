from django.db import models

from users.models import User


class Ride(models.Model):
    ride_id = models.AutoField(primary_key=True)
    city_from = models.CharField(max_length=110)
    city_to = models.CharField(max_length=110)
    start_date = models.DateTimeField()
    driver = models.ForeignKey(User, related_name='driver', on_delete=models.SET_NULL, blank=False, null=True)
    passengers = models.ManyToManyField(User, blank=True, through='Participation')


class Participation(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, related_name='passenger', on_delete=models.SET_NULL, null=True)
