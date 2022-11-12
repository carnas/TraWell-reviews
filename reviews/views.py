from django.http import JsonResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from reviews.models import Review
from reviews.serializers import ReviewListSerializer, ReviewSerializer
from rides.models import Ride
from users.models import User
from utils import user_utils
from utils.authorization import is_authorized
from utils.paginations import ReviewsPagination


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewListSerializer
    pagination_class = ReviewsPagination

    queryset = Review.objects.all()

    def _sort_by_rating_order(self, request, reviews):
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

    def _was_rated_driver(self, rated_user_type):
        if rated_user_type == 'driver':
            return True
        elif rated_user_type == 'passenger':
            return False
        else:
            raise KeyError

    def _check_ride_participation(self, driver, passenger, ride):
        return ride.driver == driver and passenger in ride.passengers.all()

    def _get_user_reviews_at_top(self, reviews, user):
        sorted_reviews = []
        for review in reviews:
            if review.reviewer == user:
                sorted_reviews.insert(0, review)
            else:
                sorted_reviews.append(review)

        return sorted_reviews

    @action(detail=False, methods=['get', 'post'], url_path=r'user_reviews/(?P<user_id>[^/.]+)', )
    def user_reviews(self, request, user_id, *args, **kwargs):
        if is_authorized(request):
            try:
                rated_user = User.objects.get(user_id=user_id)
            except User.DoesNotExist:
                return JsonResponse(status=status.HTTP_404_NOT_FOUND, data=f'User with id={user_id} not found', safe=False)
            if request.method == 'GET':
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
                reviews = self._sort_by_rating_order(request, reviews)

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
                try:
                    token = request.headers['Authorization'].split(' ')[1]
                    email = user_utils.decode_token(token)['email']
                    reviews = self._get_user_reviews_at_top(reviews, User.objects.get(email=email))
                except KeyError:
                    pass

                return self._paginate_reviews(reviews)
            elif request.method == 'POST':
                token = request.headers['Authorization'].split(' ')[1]
                try:
                    email = user_utils.decode_token(token)['email']
                    reviewer = User.objects.get(email=email)
                    was_rated_driver = self._was_rated_driver(request.data['rated_user_type'])
                    ride = Ride.objects.get(ride_id=request.data['ride'])
                    is_participation_valid = self._check_ride_participation(rated_user, reviewer, ride) if was_rated_driver \
                        else self._check_ride_participation(reviewer, rated_user, ride)
                    if is_participation_valid:
                        review = Review.objects.create(stars=request.data['rating'], description=request.data['description'],
                                                       was_rated_driver=was_rated_driver, reviewer=reviewer, rated=rated_user,
                                                       ride=ride)
                        review.save()
                        serializer = ReviewSerializer(review)
                        return JsonResponse(status=status.HTTP_201_CREATED, data=serializer.data)
                    else:
                        return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data="Invalid participation in ride",
                                            safe=False)
                except (KeyError, ValidationError):
                    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data="Wrong parameters", safe=False)
                except User.DoesNotExist:
                    return JsonResponse(status=status.HTTP_404_NOT_FOUND, data="Reviewer user does not exist", safe=False)
                except Ride.DoesNotExist:
                    return JsonResponse(status.HTTP_404_NOT_FOUND, data="Ride does not exist", safe=False)
        else:
            return JsonResponse(status=status.HTTP_401_UNAUTHORIZED, data='Not authorized', safe=False)

    def destroy(self, request, *args, **kwargs):
        if is_authorized(request):
            try:
                review = self.get_object()
                token = request.headers['Authorization'].split(' ')[1]
                email = user_utils.decode_token(token)['email']
                if review.reviewer.email != email:
                    return JsonResponse(status=status.HTTP_403_FORBIDDEN, data=f'Not allowed', safe=False)
                else:
                    review.delete()
                    return JsonResponse(status=status.HTTP_200_OK, data=f'Review deleted successfully',
                                        safe=False)
            except Review.DoesNotExist:
                return JsonResponse(status=status.HTTP_404_NOT_FOUND, data=f'Review not found', safe=False)
            except KeyError:
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data='Invalid token', safe=False)
        else:
            return JsonResponse(status=status.HTTP_401_UNAUTHORIZED, data='Not authorized', safe=False)
