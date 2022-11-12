from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from rides.models import Ride
from rides.serializers import NotRatedRideSerializer
from users.models import User
from utils import user_utils
from utils.authorization import is_authorized


@api_view(['GET'])
def get_not_rated_rides(request, user_id):
    if is_authorized(request):
        try:
            token = request.headers['Authorization'].split(' ')[1]
            email = user_utils.decode_token(token)['email']
            reviewer = User.objects.get(email=email)
            user = User.objects.get(user_id=user_id)
        except KeyError:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data='Invalid token', safe=False)
        except User.DoesNotExist:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND, data=f'User not found', safe=False)

        rides_user_as_driver = Ride.objects.filter(driver=user, passengers__in=[reviewer])
        rides_reviewer_as_driver = Ride.objects.filter(driver=reviewer, passengers__in=[user])
        rides_with_user_and_reviewer = list(rides_user_as_driver) + list(rides_reviewer_as_driver)
        serializer = NotRatedRideSerializer(rides_with_user_and_reviewer, context=user, many=True)
        return JsonResponse(status=status.HTTP_200_OK, data=serializer.data, safe=False)
    else:
        return JsonResponse(status=status.HTTP_401_UNAUTHORIZED, data='Not authorized', safe=False)
