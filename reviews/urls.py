from django.urls import path

from reviews.views import get_reviews

urlpatterns = [
    path('<int:user_id>', get_reviews),
]