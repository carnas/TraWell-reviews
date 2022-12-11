import json

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from reviews.factories import ReviewFactory
from rides.factories import RideFactory
from users.factories import UserFactory
from users.models import User

AUTH_TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJVWUxwNjc4ZWkzcm1xQ0Y0VHV5TGZBSUg2WDFnTURkSFIzWkZpSjlPS1Q0In0.eyJleHAiOjE2NjYzNjAyNjQsImlhdCI6MTY2NjM1OTk2NCwiYXV0aF90aW1lIjoxNjY2MzU5OTYzLCJqdGkiOiI5YTM5MmNhNy0zZjE5LTQzNjgtODI1Ny0xMWNhOTAyNzdlM2MiLCJpc3MiOiJodHRwOi8vbG9jYWxob3N0Ojg0MDMvYXV0aC9yZWFsbXMvVHJhV2VsbCIsImF1ZCI6WyJzb2NpYWwtb2F1dGgiLCJyZWFsbS1tYW5hZ2VtZW50IiwicmVhY3QiLCJhY2NvdW50Il0sInN1YiI6IjY1ODMwOWYxLTdiZmMtNDcxYy05MmNhLTkzYTUwZjk2MmU2ZSIsInR5cCI6IkJlYXJlciIsImF6cCI6ImtyYWtlbmQiLCJzZXNzaW9uX3N0YXRlIjoiZmJhM2M4NmUtYjUzMS00Yzk2LWIyYTctM2VkYTc0ZmVmZWFlIiwiYWNyIjoiMSIsImFsbG93ZWQtb3JpZ2lucyI6WyJodHRwOi8vbG9jYWxob3N0OjkwMDAiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwiYXBwLWFkbWluIiwidW1hX2F1dGhvcml6YXRpb24iLCJhcHAtdXNlciIsInByaXZhdGVfdXNlciIsImRlZmF1bHQtcm9sZXMtdHJhd2VsbCJdfSwicmVzb3VyY2VfYWNjZXNzIjp7InNvY2lhbC1vYXV0aCI6eyJyb2xlcyI6WyJhZG1pbiIsInVzZXIiXX0sInJlYWxtLW1hbmFnZW1lbnQiOnsicm9sZXMiOlsidmlldy1pZGVudGl0eS1wcm92aWRlcnMiLCJ2aWV3LXJlYWxtIiwibWFuYWdlLWlkZW50aXR5LXByb3ZpZGVycyIsImltcGVyc29uYXRpb24iLCJyZWFsbS1hZG1pbiIsImNyZWF0ZS1jbGllbnQiLCJtYW5hZ2UtdXNlcnMiLCJxdWVyeS1yZWFsbXMiLCJ2aWV3LWF1dGhvcml6YXRpb24iLCJxdWVyeS1jbGllbnRzIiwicXVlcnktdXNlcnMiLCJtYW5hZ2UtZXZlbnRzIiwibWFuYWdlLXJlYWxtIiwidmlldy1ldmVudHMiLCJ2aWV3LXVzZXJzIiwidmlldy1jbGllbnRzIiwibWFuYWdlLWF1dGhvcml6YXRpb24iLCJtYW5hZ2UtY2xpZW50cyIsInF1ZXJ5LWdyb3VwcyJdfSwia3Jha2VuZCI6eyJyb2xlcyI6WyJhZG1pbiIsInVzZXIiXX0sInJlYWN0Ijp7InJvbGVzIjpbImFkbWluIiwidXNlciJdfSwiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInNpZCI6ImZiYTNjODZlLWI1MzEtNGM5Ni1iMmE3LTNlZGE3NGZlZmVhZSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJ1c2VyX3R5cGUiOiJQcml2YXRlIEFjY291bnQiLCJkYXRlX29mX2JpcnRoIjoiMjAwMC0wMy0wOSIsImZhY2Vib29rIjoiaHR0cHM6Ly9vcGVuLnNwb3RpZnkuY29tL2NvbGxlY3Rpb24vdHJhY2tzIiwibmFtZSI6Ik1vbmlrYSBHYWxpxYRza2EiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiIzbW9uaWthMTAwQGdtYWlsLmNvbSIsImluc3RhZ3JhbSI6IiIsImdpdmVuX25hbWUiOiJNb25pa2EiLCJmYW1pbHlfbmFtZSI6IkdhbGnFhHNrYSIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BTG01d3UxVlV1S3JQazdyeHJTRzdHQndWNXU1bHZqLUdZRFgzbEFHTzJCTj1zOTYtYyIsImVtYWlsIjoiM21vbmlrYTEwMEBnbWFpbC5jb20ifQ.SNJBOywc5PGuwkqJQztwdfeHEaLvJHVpHlJ8aEtFcLTOIP_HsaaLfjcPdIc2DAu4QhUaB1LCAIKCWsw6LJ9KQoraWY_oX3xV1AmByejnPb8emH-2KUqmx9MaYcTRNARlyyZsjtKBAd_Wj7b-7i758N7WNI26mRzeV0TQVk8PJ6bHZX3vIAprzzlHA8xUCNEHEj7AsTaOwNTkGH5KoCygPsP1ej8oKxwC72foTz9EBHPZrhdDIXVgTgZ255ONfTdq4dIIvlnHkSgnjt1fTaJ-5oE0qs6fVI0_7bk0qPEIHUjY31UB7pR9fdaaneEAUaJ-DswrhaRc3guuSvRPofZwiw"


class ReviewViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=AUTH_TOKEN)

    def test_get_user_reviews_user_does_not_exist(self):
        response = self.client.get(f"/reviews/user_reviews/1")
        results = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(results, 'User with id=1 not found')

    def test_get_user_reviews_missing_user_type_parameter(self):
        user = UserFactory()
        response = self.client.get(f"/reviews/user_reviews/{user.user_id}")
        results = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(results, 'Missing user_type parameter')

    def test_get_user_reviews_invalid_user_type_parameter(self):
        user = UserFactory()
        parameters = {'user_type': 'al'}
        response = self.client.get(f"/reviews/user_reviews/{user.user_id}", data=parameters, format='json')
        results = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(results, 'Invalid user_type parameter')

    def test_get_user_reviews_with_all_user_type_rating_order_my_first(self):
        user = UserFactory()
        user2 = UserFactory(email='3monika100@gmail.com')
        ride = RideFactory(driver=user2)
        review = ReviewFactory(reviewer=user2, rated=user, ride=ride)
        parameters = {'user_type': 'all', 'rating_order': 'my_first'}
        response = self.client.get(f"/reviews/user_reviews/{user.user_id}", data=parameters, format='json')
        results = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(results['results'][0]['review_id'], review.review_id)

    def test_get_user_reviews_with_driver_user_type_rating_order_invalid(self):
        user = UserFactory()
        user2 = UserFactory(email='3monika100@gmail.com')
        ride = RideFactory(driver=user)
        review = ReviewFactory(reviewer=user2, rated=user, ride=ride)
        parameters = {'user_type': 'driver', 'rating_order': 'des'}
        response = self.client.get(f"/reviews/user_reviews/{user.user_id}", data=parameters, format='json')
        results = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(results, "Invalid rating_order parameter")

    def test_post_user_review_successful(self):
        user = UserFactory()
        user2 = UserFactory(email='3monika100@gmail.com')
        ride = RideFactory(driver=user, passengers=User.objects.filter(user_id=user2.user_id))
        data = {'rating': 3, 'description': '', 'was_rated_driver': True, 'reviewer': user2.user_id,
                'rated': user.user_id, 'ride': ride.ride_id, 'rated_user_type': 'driver'}
        response = self.client.post(f"/reviews/user_reviews/{user.user_id}", data=data, format='json')
        results = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(results['stars'], data['rating'])

    def test_post_user_review_invalid_stars_parameter(self):
        user = UserFactory()
        user2 = UserFactory(email='3monika100@gmail.com')
        ride = RideFactory(driver=user, passengers=User.objects.filter(user_id=user2.user_id))
        data = {'stars': 3, 'description': '', 'was_rated_driver': True, 'reviewer': user2.user_id,
                'rated': user.user_id, 'ride': ride.ride_id, 'rated_user_type': 'driver'}
        response = self.client.post(f"/reviews/user_reviews/{user.user_id}", data=data, format='json')
        results = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(results, 'Wrong parameters')

    def test_post_user_review_reviewer_user_not_exist(self):
        user = UserFactory()
        ride = RideFactory(driver=user)
        data = {'rating': 3, 'description': '', 'was_rated_driver': True, 'reviewer': 100,
                'rated': user.user_id, 'ride': ride.ride_id, 'rated_user_type': 'driver'}
        response = self.client.post(f"/reviews/user_reviews/{user.user_id}", data=data, format='json')
        results = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(results, 'Reviewer user does not exist')

    def test_post_user_reviews_review_exist_already(self):
        user = UserFactory()
        user2 = UserFactory(email='3monika100@gmail.com')
        ride = RideFactory(driver=user, passengers=User.objects.filter(user_id=user2.user_id))
        review = ReviewFactory(reviewer=user2, rated=user, ride=ride)
        data = {'rating': 3, 'description': '', 'was_rated_driver': True, 'ride': ride.ride_id,
                'rated_user_type': 'driver'}
        response = self.client.post(f"/reviews/user_reviews/{user.user_id}", data=data, format='json')
        results = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(results, "The review exists already")

    def test_delete_user_review_not_allowed(self):
        user = UserFactory()
        user2 = UserFactory(email='3monika100@gmail.com')
        user3 = UserFactory()
        ride = RideFactory(driver=user, passengers=User.objects.filter(user_id=user2.user_id))
        review = ReviewFactory(reviewer=user3, rated=user, ride=ride)
        response = self.client.delete(f"/reviews/{review.review_id}")
        results = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(results, "Not allowed")

    def test_delete_user_review_successful(self):
        user = UserFactory()
        user2 = UserFactory(email='3monika100@gmail.com')
        ride = RideFactory(driver=user, passengers=User.objects.filter(user_id=user2.user_id))
        review = ReviewFactory(reviewer=user2, rated=user, ride=ride)
        response = self.client.delete(f"/reviews/{review.review_id}")
        results = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(results, "Review deleted successfully")

    def test_delete_user_review_not_found(self):
        user = UserFactory(email='3monika100@gmail.com')
        response = self.client.delete(f"/reviews/1")
        results = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(results['detail'], "Not found.")

