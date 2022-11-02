from django.http import JsonResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action

from reviews.models import Review
from reviews.serializers import ReviewListSerializer
from users.models import User
from utils.authorization import is_authorized
from utils.paginations import ReviewsPagination


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewListSerializer
    pagination_class = ReviewsPagination

    queryset = Review.objects.all()

    def _filter_by_rating(self, request, reviews):
        try:
            rating_from = request.GET['rating_from']
            reviews = reviews.filter(stars__gte=rating_from)
        except KeyError:
            pass

        try:
            rating_to = request.GET['rating_to']
            reviews = reviews.filter(stars__lte=rating_to)
        except KeyError:
            pass

        return reviews

    def _paginate_reviews(self, reviews):
        page = self.paginate_queryset(reviews)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(reviews, many=True)
        return JsonResponse(status=status.HTTP_200_OK, data=serializer.data, safe=False)

    @action(detail=False, methods=['get'], url_path=r'user_reviews/(?P<user_id>[^/.]+)', )
    def user_reviews(self, request, user_id, *args, **kwargs):
        if is_authorized(request):
            try:
                rated_user = User.objects.get(user_id=user_id)
            except User.DoesNotExist:
                return JsonResponse(status=status.HTTP_404_NOT_FOUND, data=f'User with id={user_id} not found', safe=False)

            reviews = Review.objects.filter(rated=rated_user)
            try:
                user_ride_type = request.GET['user_type']
                if user_ride_type == 'all':
                    reviews = reviews
                elif user_ride_type == 'driver':
                    reviews = reviews.filter(was_rated_driver=True)
                elif user_ride_type == 'passenger':
                    reviews = reviews.filter(was_rated_driver=False)
                else:
                    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data="Invalid user_type parameter",
                                        safe=False)
            except KeyError:
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data=f"Missing user_type parameter", safe=False)
            reviews = self._filter_by_rating(request, reviews)

            try:
                rating_order = request.GET['rating_order']
                if rating_order == 'asc':
                    reviews = reviews.order_by('stars')
                elif rating_order == 'desc':
                    reviews = reviews.order_by('-stars')
                else:
                    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data="Invalid rating_order parameter",
                                        safe=False)
            except KeyError:
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data=f"Missing rating_order parameter",
                                    safe=False)

            return self._paginate_reviews(reviews)
        else:
            return JsonResponse(status=status.HTTP_401_UNAUTHORIZED, data='Not authorized', safe=False)
