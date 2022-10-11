from django.db import models


class User(models.Model):
    pass


class Ride(models.Model):
    driver = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class RidePassenger(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    passenger = models.ForeignKey(User, on_delete=models.CASCADE)


class Review(models.Model):
    stars = models.IntegerField()
    description = models.CharField(max_length=500, null=True, blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='reviewer')
    rated = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rated')
    was_rated_driver = models.BooleanField()
    ride = models.ForeignKey(Ride, on_delete=models.DO_NOTHING)

