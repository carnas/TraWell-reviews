import random

from rides.factories import RideFactory
from users.models import User


def get_list_without_index(list, index):
    res = list[:]
    res.pop(index)
    return res


def create(amount):
    users = User.objects.all()
    for i in range(amount):
        driver_index = random.choice(range(len(users)))
        driver = users[driver_index]
        passengers = random.choices(get_list_without_index(users, driver_index), k=random.randint(0, 9))

        RideFactory(driver=driver, passengers=passengers)
