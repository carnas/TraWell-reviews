from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    avg_rate = models.DecimalField(max_digits=3, decimal_places=2)
    avatar = models.URLField(blank=True, default="")
