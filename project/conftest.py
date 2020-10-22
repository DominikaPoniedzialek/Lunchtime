import datetime

import pytest
from django.contrib.auth.models import User

from django.test import Client

from lunchtime.models import Restaurant, Meal, Table, Review, Reservation


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def user():
    user = User.objects.create_user(username='username4', password='password4',
                                    first_name='Dominika', last_name='Poniedziałek', email='user4@example.com')
    return user


@pytest.fixture
def restaurant(user):
    restaurant = Restaurant.objects.create(name='La Trattoria', address='Dąbrowskiego 3', phone='124568765',
                                           email='trattoria@krakow.pl', description='Wspaniałe makarony!',
                                           owner=user, logo='/home/desktop/logo.jpg')
    return restaurant


@pytest.fixture
def restaurant_list():
    Restaurant.objects.create(name='La Trattoria', address='Dąbrowskiego 3', phone='124568765',
                              email='trattoria@krakow.pl', description='Wspaniałe makarony!',
                              owner=User.objects.create_user(username='username1', password='password1'),
                              logo='/home/desktop/logo.jpg')
    Restaurant.objects.create(name='Trattoria Parma', address='Dąbrowskiego 34', phone='124568787',
                              email='parma@krakow.pl', description='Doskonała pizza!',
                              owner=User.objects.create_user(username='username2', password='password2'),
                              logo='/home/desktop/logo.jpg')
    Restaurant.objects.create(name='Frutti di Mare', address='Lwowska 3', phone='234568765',
                              email='lwowska@krakow.pl', description='Wspaniałe owoce morza!',
                              owner=User.objects.create_user(username='username3', password='password3'),
                              logo='/home/desktop/logo.jpg')
    return Restaurant.objects.all().order_by('name')


@pytest.fixture
def meal(restaurant):
    meal = Meal.objects.create(category=2, name='pizza hawajska', description='pizza z szynką i ananasem', price=28.00,
                               restaurant=restaurant)
    return meal


@pytest.fixture
def meals(restaurant):
    meal_1 = Meal.objects.create(category=2, name='pizza hawajska', description='pizza z szynką i ananasem',
                                 price=28.00, restaurant=restaurant)
    meal_2 = Meal.objects.create(category=2, name='pizza', description='parma', price=26.00, restaurant=restaurant)
    return Meal.objects.all()

@pytest.fixture
def menu_breakfast(restaurant):
    breakfast = Meal.objects.create(category=1, name='sałatka owocowa', description='sałatka ze świeżych owoców',
                                    price=12.00, restaurant=restaurant)
    return breakfast


@pytest.fixture
def menu_lunch(restaurant):
    lunch = Meal.objects.create(category=2, name='pizza', description='parma', price=26.00, restaurant=restaurant)
    return lunch


@pytest.fixture
def menu_dinner(restaurant):
    dinner = Meal.objects.create(category=3, name='pieczeń z jagnięciny', description='pieczeń w sosie własnym',
                                 price=52.00, restaurant=restaurant)
    return dinner


@pytest.fixture
def table(restaurant):
    table = Table.objects.create(persons=2, reserved=False, restaurant=restaurant)
    return table


@pytest.fixture
def review(restaurant, user):
    review = Review.objects.create(rate=5, review="Pysznie!", date=datetime.datetime.now(), user=user, restaurant=restaurant)
    return review


@pytest.fixture
def review_list(restaurant, user):
    Review.objects.create(rate=5, review="Pysznie!", date=datetime.datetime.now(), user=user, restaurant=restaurant)
    Review.objects.create(rate=4, review="Świetne dania", date=datetime.datetime.now(), user=user, restaurant=restaurant)
    Review.objects.create(rate=3, review="Miła obsługa", date=datetime.datetime.now(), user=user, restaurant=restaurant)
    return Review.objects.all().order_by('-date')


@pytest.fixture
def reservation(restaurant, user, meals, table):
    reservation_1 = Reservation.objects.create(restaurant=restaurant, table=table, date=datetime.date.today(), time='10:30:00',
                                               user=user)
    reservation_1.meal.set(meals)
    return reservation_1


@pytest.fixture
def reservation_list(restaurant, user, meals, table):
    reservation_1 = Reservation.objects.create(restaurant=restaurant, table=table, date=datetime.date.today(),
                                               time='10:30:00', user=user)
    reservation_1.meal.set(meals)
    reservation_2 = Reservation.objects.create(restaurant=restaurant, table=table, date=datetime.date.today(),
                                               time='14:30:00', user=user)
    reservation_2.meal.set(meals)
    reservation_3 = Reservation.objects.create(restaurant=restaurant, table=table, date=datetime.date.today(),
                                               time='12:00:00', user=user)
    reservation_3.meal.set(meals)
    return Reservation.objects.all().order_by('-date')

