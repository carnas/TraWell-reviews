from django.urls import path

from rides.views import get_not_rated_rides

urlpatterns = [
    path('<int:user_id>', get_not_rated_rides)
]
