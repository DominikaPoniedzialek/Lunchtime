import pytest
from django.contrib.auth.models import User

from django.test import Client

from lunchtime.models import Restaurant


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
def restaurant():
    restaurant = Restaurant.objects.create(name='La Trattoria', address='Dąbrowskiego 3', phone='124568765',
                                           email='trattoria@krakow.pl', description='Wspaniałe makarony!',
                                           owner=User.objects.create_user(username='username1', password='password1'),
                                           logo='/home/desktop/logo.jpg')
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


