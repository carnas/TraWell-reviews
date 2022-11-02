from rest_framework import serializers

from reviews.models import Review
from users.models import User


class UserNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'first_name', 'avg_rate', 'avatar')


class ReviewListSerializer(serializers.ModelSerializer):
    reviewer = UserNestedSerializer(many=False)

    class Meta:
        model = Review
        fields = ('review_id', 'stars', 'description', 'was_rated_driver', 'created_on', 'reviewer')