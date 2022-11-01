from django.http import JsonResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action

from reviews.models import Review
from reviews.serializers import ReviewListSerializer
from users.models import User
from utils.authorization import is_authorized


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewListSerializer
    queryset = Review.objects.all()

    @action(detail=False, methods=['get'], url_path=r'user_reviews/(?P<user_id>[^/.]+)', )
    def user_reviews(self, request, user_id, *args, **kwargs):
        if is_authorized(request):
            try:
                rated_user = User.objects.get(user_id=user_id)
            except User.DoesNotExist:
                return JsonResponse(status=status.HTTP_404_NOT_FOUND, data=f'User with id={user_id} not found', safe=False)

            reviews = Review.objects.filter(rated=rated_user)
            serializer = ReviewListSerializer(reviews, many=True)
            return JsonResponse(status=status.HTTP_200_OK, data=serializer.data, safe=False)
        else:
            return JsonResponse(status=status.HTTP_401_UNAUTHORIZED, data='Not authorized', safe=False)
