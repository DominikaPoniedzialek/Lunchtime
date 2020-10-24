import pytest
import datetime

from django.contrib.auth.models import User, Permission

from lunchtime.forms import SelectDateAndTimeForm
from lunchtime.models import Restaurant, Meal, Review, Reservation, Table


@pytest.mark.django_db
def test_landing_page(client):
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
    response = client.post(url, {'username': 'new_user_1', 'password1': 'password123', 'password2': 'password123',
                                 'first_name': 'Dominika', 'last_name': 'Poniedzialek', 'email': 'new_user@example.com'})
    assert User.objects.count() == 1
    assert response.status_code == 302
    new_user = User.objects.get(username='new_user_1')
    assert new_user.email == 'new_user@example.com'


@pytest.mark.django_db
def test_user_exist(client, user):
    url = '/add_user/'
    assert User.objects.count() == 1
    response = client.post(url, {'username': 'username4', 'password1': 'password123', 'password2': 'password123',
                                 'first_name': 'Dominika', 'last_name': 'Poniedzialek', 'email': 'user4@example.com'})
    assert response.status_code == 200
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_different_password(client):
    assert User.objects.count() == 0
    url = '/add_user/'
    response = client.post(url, {'username': 'username5', 'password1': 'password12', 'password2': 'password34',
                                 'first_name': 'Dominika', 'last_name': 'Poniedzialek', 'email': 'user5@example.com'}, follow=True)
    assert response.status_code == 200
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_login(client):
    user = User.objects.create(username='dominika123', password='password123')
    user.save()
    url = '/login/'
    response = client.post(url, {'username': 'dominika123', 'password': 'password123'})
    client.login(user=user)
    assert response.status_code == 302


@pytest.mark.django_db
def test_logout(client, user):
    client.login(username='dominika123', password='password123')
    url = '/logout/'
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_restaurant_in_db(client, restaurant):
    assert Restaurant.objects.count() == 1


@pytest.mark.django_db
def test_restaurant_details(client, restaurant, menu_breakfast):
    url = f'/restaurant/{restaurant.id}/'
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['restaurant'].name == 'La Trattoria'
    assert response.context['restaurant'].address == 'Dąbrowskiego 3'
    assert response.context['restaurant'].phone == '124568765'
    assert response.context['restaurant'].email == 'trattoria@krakow.pl'
    assert response.context['restaurant'].description == 'Wspaniałe makarony!'
    assert response.context['restaurant'].logo == '/home/desktop/logo.jpg'


@pytest.mark.django_db
def test_restaurant_menu_breakfast(client, menu_breakfast, restaurant):
    url = f'/restaurant/{restaurant.id}/'
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['menu_breakfast'][0].name == 'sałatka owocowa'
    assert response.context['menu_breakfast'][0].description == 'sałatka ze świeżych owoców'
    assert response.context['menu_breakfast'][0].price == 12.00
    assert response.context['menu_breakfast'][0].category == 1


@pytest.mark.django_db
def test_restaurant_menu_lunch(client, menu_lunch, restaurant):
    url = f'/restaurant/{restaurant.id}/'
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['menu_lunch'][0].name == 'pizza'
    assert response.context['menu_lunch'][0].description == 'parma'
    assert response.context['menu_lunch'][0].price == 26.00
    assert response.context['menu_lunch'][0].category == 2


@pytest.mark.django_db
def test_restaurant_menu_dinner(client, menu_dinner, restaurant):
    url = f'/restaurant/{restaurant.id}/'
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['menu_dinner'][0].name == 'pieczeń z jagnięciny'
    assert response.context['menu_dinner'][0].description == 'pieczeń w sosie własnym'
    assert response.context['menu_dinner'][0].price == 52.00
    assert response.context['menu_dinner'][0].category == 3


@pytest.mark.django_db
def test_restaurant_reviews(client, review, restaurant):
    url = f'/restaurant/{restaurant.id}/'
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['reviews'][0].rate == 5
    assert response.context['reviews'][0].review == "Pysznie!"


@pytest.mark.django_db
def test_restaurant_reservations(client, reservation, restaurant, table):
    url = f'/restaurant/{restaurant.id}/'
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['reservations'][0].date == datetime.date.today()
    assert response.context['reservations'][0].time == datetime.time(10, 30)
    assert response.context['reservations'][0].table == table


@pytest.mark.django_db
def test_restaurant_tables(client, restaurant, table):
    url = f'/restaurant/{restaurant.id}/'
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['tables'][0].persons == 2


@pytest.mark.django_db
def test_add_restaurant(client):
    user = User.objects.create(username='dominika123', password='password123')
    user.save()
    user.user_permissions.add(Permission.objects.get(codename='add_restaurant'))
    client.force_login(user=user)
    url = '/add_restaurant/'
    assert Restaurant.objects.count() == 0
    response = client.post(url, {'name': 'La Trattoria', 'address': 'Dąbrowskiego 3', 'phone': '124568765',
                                 'email': 'trattoria@krakow.pl', 'description': 'Wspaniałe makarony!',
                                 'logo': 'home/desktop/logo.png'})
    assert Restaurant.objects.count() == 1
    assert response.status_code == 302
    new_restaurant = Restaurant.objects.get(name='La Trattoria')
    assert new_restaurant.address == 'Dąbrowskiego 3'


@pytest.mark.django_db
def test_update_restaurant(client, restaurant):
    user = User.objects.create(username='dominika123', password='password123')
    user.save()
    user.user_permissions.add(Permission.objects.get(codename='change_restaurant'))
    client.force_login(user=user)
    restaurant_first = Restaurant.objects.first()
    restaurant.phone = '999888777'
    restaurant.address = 'Krakowska 54'
    restaurant.save()
    url = f'/modify_restaurant/{restaurant_first.id}/'
    response = client.post(f'{url}', {'phone': restaurant.phone, 'address': restaurant.address}, follow=True)
    assert response.status_code == 200
    restaurant_obj = Restaurant.objects.get(id=restaurant_first.id)
    assert restaurant_obj.phone == '999888777'
    assert restaurant_obj.address == 'Krakowska 54'


@pytest.mark.django_db
def test_delete_restaurant(client, restaurant):
    user = User.objects.create(username='dominika123', password='password123')
    user.save()
    user.user_permissions.add(Permission.objects.get(codename='delete_restaurant'))
    client.force_login(user=user)
    restaurant_first = Restaurant.objects.first()
    response = client.delete(f"/delete_restaurant/{restaurant_first.id}/")
    assert response.status_code == 302
    restaurants_ids = [restaurant.id for restaurant in Restaurant.objects.all()]
    assert restaurant_first.id not in restaurants_ids


@pytest.mark.django_db
def test_list_restaurants(client, restaurant_list):
    url = '/restaurant_list/'
    response = client.get(url)
    assert response.status_code == 200
    assert Restaurant.objects.count() == 3
    assert list(response.context['object_list']) == list(restaurant_list)


@pytest.mark.django_db
def test_add_review(client, restaurant, user):
    client.force_login(user=user)
    url = '/add_review/'
    assert Review.objects.count() == 0
    response = client.post(url, {'rate': 5, 'review': 'Przyjemna, włoska knajpka', 'date': datetime.datetime.now(),
                                 'restaurant': restaurant.id, 'user': user.id})
    assert Review.objects.count() == 1
    assert response.status_code == 302
    new_review = Review.objects.get(rate=5)
    assert new_review.review == 'Przyjemna, włoska knajpka'


@pytest.mark.django_db
def test_list_reviews(client, review_list, user):
    client.force_login(user=user)
    url = '/review_list/'
    response = client.get(url)
    assert response.status_code == 200
    assert Review.objects.count() == 3
    assert list(response.context['object_list']) == list(review_list)


@pytest.mark.django_db
def test_delete_review(client, review, user):
    client.force_login(user=user)
    review_first = Review.objects.first()
    response = client.delete(f"/delete_review/{review_first.id}/")
    assert response.status_code == 302
    review_ids = [review.id for review in Review.objects.all()]
    assert review_first.id not in review_ids


@pytest.mark.django_db
def test_list_reservations(client, reservation_list, user):
    client.force_login(user=user)
    url = '/reservation_list/'
    response = client.get(url)
    assert response.status_code == 200
    assert Reservation.objects.count() == 3
    assert list(response.context['object_list']) == list(reservation_list)


@pytest.mark.django_db
def test_reservation_date_in_past(client):
    date = datetime.date.today() - datetime.timedelta(days=1)
    form = SelectDateAndTimeForm(data={'date': date})
    assert (form.is_valid()) == False


@pytest.mark.django_db
def test_select_date_time(client, user):
    client.force_login(user=user)
    url = '/select_date_time/'
    response = client.get(url, {'date': datetime.date.today(), 'time': datetime.time(12, 30)}, follow=True)
    assert response.status_code == 200


@pytest.mark.django_db
def test_select_restaurant(client, user, restaurant):
    client.force_login(user=user)
    date = datetime.date.today()
    time = datetime.time(12, 30)
    url = f'/select_restaurant/{date}/{time}/'
    response = client.post(f'{url}', {'restaurant': restaurant.id}, follow=True)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_reservation(client, user, restaurant, table, meal):
    client.force_login(user=user)
    date = datetime.date.today()
    time = datetime.time(12, 30)
    url = f'/add_reservation/{date}/{time}/{restaurant.id}/'
    response = client.get(f'{url}', {'table': table.id, 'meal': meal.id}, follow=True)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_reservation(client, reservation, user):
    client.force_login(user=user)
    reservation_first = Reservation.objects.first()
    response = client.delete(f"/delete_reservation/{reservation_first.id}/")
    assert response.status_code == 302
    reservation_ids = [reservation.id for reservation in Reservation.objects.all()]
    assert reservation_first.id not in reservation_ids


@pytest.mark.django_db
def test_add_meal(client, restaurant):
    user = User.objects.create(username='dominika123', password='password123')
    user.save()
    user.user_permissions.add(Permission.objects.get(codename='add_meal'))
    client.force_login(user=user)
    url = '/add_meal/'
    assert Meal.objects.count() == 0
    response = client.post(url, {'category': 2, 'name': 'pizza parma', 'description': 'pizza',
                                 'restaurant': restaurant.id, 'price': 25.00})
    assert Meal.objects.count() == 1
    assert response.status_code == 302
    new_meal = Meal.objects.get(category=2)
    assert new_meal.name == 'pizza parma'


@pytest.mark.django_db
def test_update_meal(client, meal):
    user = User.objects.create(username='dominika123', password='password123')
    user.save()
    user.user_permissions.add(Permission.objects.get(codename='change_meal'))
    client.force_login(user=user)
    meal_first = Meal.objects.first()
    meal.price = 30.00
    meal.name = 'pizza średnia hawajska'
    meal.save()
    url = f'/modify_meal/{meal_first.id}/'
    response = client.post(f'{url}', {'price': meal.price, 'name': meal.name}, follow=True)
    assert response.status_code == 200
    meal_obj = Meal.objects.get(id=meal_first.id)
    assert meal_obj.price == 30.00
    assert meal_obj.name == 'pizza średnia hawajska'


@pytest.mark.django_db
def test_delete_meal(client, meal):
    user = User.objects.create(username='dominika123', password='password123')
    user.save()
    user.user_permissions.add(Permission.objects.get(codename='delete_meal'))
    client.force_login(user=user)
    meal_first = Meal.objects.first()
    response = client.delete(f"/delete_meal/{meal_first.id}/")
    assert response.status_code == 302
    meal_ids = [meal.id for meal in Meal.objects.all()]
    assert meal_first.id not in meal_ids


@pytest.mark.django_db
def test_add_table(client, restaurant):
    user = User.objects.create(username='dominika123', password='password123')
    user.save()
    user.user_permissions.add(Permission.objects.get(codename='add_table'))
    client.force_login(user=user)
    url = '/add_table/'
    assert Table.objects.count() == 0
    response = client.post(url, {'persons': 2, 'reserved': False, 'restaurant': restaurant.id})
    assert Table.objects.count() == 1
    assert response.status_code == 302
    new_table = Table.objects.get(persons=2)
    assert new_table.reserved == False


@pytest.mark.django_db
def test_delete_table(client, table):
    user = User.objects.create(username='dominika123', password='password123')
    user.save()
    user.user_permissions.add(Permission.objects.get(codename='delete_table'))
    client.force_login(user=user)
    table_first = Table.objects.first()
    response = client.delete(f"/delete_table/{table_first.id}/")
    assert response.status_code == 302
    table_ids = [table.id for table in Table.objects.all()]
    assert table_first.id not in table_ids
