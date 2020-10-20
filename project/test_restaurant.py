import pytest
from django.contrib.auth.models import User

from lunchtime.models import Restaurant


@pytest.mark.django_db
def test_main_page(client):
    url = ''
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_contact_page(client):
    url = '/contact/'
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_user(client):
    url = '/add_user/'
    assert User.objects.count() == 0
    response = client.post(url, {'username': 'new_user_1', 'password': 'password123', 'password_repeat': 'password123',
                                 'first_name': 'Dominika', 'last_name': 'Poniedzialek', 'email': 'new_user@example.com'})
    assert User.objects.count() == 1
    assert response.status_code == 302
    new_user = User.objects.get(username='new_user_1')
    assert new_user.email == 'new_user@example.com'


@pytest.mark.django_db
def test_user_exist(client, user):
    url = '/add_user/'
    assert User.objects.count() == 1
    response = client.post(url, {'username': 'username4', 'password': 'password1', 'password_repeat': 'password1',
                                 'first_name': 'Dominika', 'last_name': 'Poniedzialek', 'email': 'user4@example.com'})
    assert response.status_code == 200
    assert User.objects.count() == 1


# @pytest.mark.django_db
# def test_different_password(client):
#     url = '/add_user/'
#     response = client.post(url, {'username': 'username5', 'password': 'password12', 'password_repeat': 'password34',
#                                  'first_name': 'Dominika', 'last_name': 'Poniedzialek', 'email': 'user5@example.com'})
#     assert response.status_code == 200
#     assert User.objects.count() == 0


# @pytest.mark.django_db
# def test_login(client, user):
#     url = '/login/'
#     response = client.get(url)
#     client.login(user=user)
#     assert response.status_code == 302


@pytest.mark.django_db
def test_restaurant_in_db(client, restaurant):
    assert Restaurant.objects.count() == 1


@pytest.mark.django_db
def test_restaurant_details(client, restaurant):
    url = f'/restaurant/{restaurant.id}/'
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['restaurant'].name == 'La Trattoria'
    assert response.context['restaurant'].address == 'Dąbrowskiego 3'
    assert response.context['restaurant'].phone == '124568765'
    assert response.context['restaurant'].email == 'trattoria@krakow.pl'
    assert response.context['restaurant'].description == 'Wspaniałe makarony!'
    assert response.context['restaurant'].logo == '/home/desktop/logo.jpg'


# @pytest.mark.django_db
# def test_restaurant_menu(client, game, category):
#     user = User.objects.create(username='grzegorz', password='1234')
#     user.save()
#     client.force_login(user=user)
#     url = f'/game/{game.id}/'
#     response = client.get(url)
#     assert response.status_code == 200
#     assert response.context['game'].title == 'DOOM'
#     assert response.context['game'].year == 2016
#     assert response.context['game'].category == category


@pytest.mark.django_db
def test_list_restaurants(client, restaurant_list):
    url = '/restaurant_list/'
    response = client.get(url)
    assert response.status_code == 200
    assert Restaurant.objects.count() == 3
    assert list(response.context['object_list']) == list(restaurant_list)

