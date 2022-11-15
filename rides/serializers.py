from rest_framework import serializers

from rides.models import Ride, Participation
from users.serializers import UserSerializer

class NotRatedRideSerializer(serializers.ModelSerializer):
    was_driver = serializers.SerializerMethodField('check_user_was_driver')

    def check_user_was_driver(self, ride):
        return ride.driver == self.context

    class Meta:
        model = Ride
        fields = ('ride_id', 'city_from', 'city_to', 'start_date', 'was_driver')


class RideSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Ride
        fields = ('ride_id', 'city_from', 'city_to', 'start_date', 'driver')


class RideUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ('ride_id', 'city_from', 'city_to', 'start_date')


class ParticipationSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Participation
        fields = ('id', 'ride', 'user')

