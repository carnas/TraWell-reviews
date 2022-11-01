from django.urls import path

urlpatterns = [
    path('<int:user_id>', get_reviews),
]