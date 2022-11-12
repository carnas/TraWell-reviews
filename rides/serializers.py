from rest_framework import serializers

from rides.models import Ride


class NotRatedRideSerializer(serializers.ModelSerializer):
    was_driver = serializers.SerializerMethodField('check_user_was_driver')

    def check_user_was_driver(self, ride):
        return ride.driver == self.context

    class Meta:
        model = Ride
        fields = ('ride_id', 'city_from', 'city_to', 'start_date', 'was_driver')
