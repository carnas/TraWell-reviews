import scripts.create_users
import scripts.create_rides
import scripts.create_reviews

USERS_AMOUNT = 20
RIDES_AMOUNT = 100
REVIEWS_AMOUNT = 100

scripts.create_users.create(USERS_AMOUNT)
scripts.create_rides.create(RIDES_AMOUNT)
scripts.create_reviews.create(REVIEWS_AMOUNT)
