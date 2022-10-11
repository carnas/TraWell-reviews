from django.contrib import admin
from .models import User, Ride, RidePassenger, Review


admin.site.register(User)
admin.site.register(Ride)
admin.site.register(RidePassenger)
admin.site.register(Review)
