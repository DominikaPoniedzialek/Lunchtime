import pytest
import datetime
from django.contrib.auth.models import User


from lunchtime.forms import SelectDateAndTimeForm
from lunchtime.models import Restaurant, Meal, Review, Reservation


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


@pytest.mark.django_db
def test_different_password(client):
    url = '/add_user/'
    response = client.post(url, {'username': 'username5', 'password': 'password12', 'password_repeat': 'password34',
                                 'first_name': 'Dominika', 'last_name': 'Poniedzialek', 'email': 'user5@example.com'})
    assert response.status_code == 200
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_login(client):
    user = User.objects.create(username='dominika123', password='password123')
    user.save()
    url = '/login/'
    response = client.get(url)
    client.login(user=user)
    assert response.status_code == 302


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
def test_restaurant_review(client, review, restaurant):
    url = f'/restaurant/{restaurant.id}/'
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['reviews'][0].rate == 5
    assert response.context['reviews'][0].review == "Pysznie!"


@pytest.mark.django_db
def test_add_restaurant(client):
    user = User.objects.create(username='dominika12', password='password1234')
    user.save()
    client.force_login(user=user)
    url = '/add_restaurant/'
    assert Restaurant.objects.count() == 0
    response = client.post(url, {'name': 'La Trattoria', 'address': 'Dąbrowskiego 3', 'phone': '124568765',
                                 'email': 'trattoria@krakow.pl', 'description': 'Wspaniałe makarony!', 'owner': user,
                                 'logo': '/home/desktop/logo.jpg'})
    assert Restaurant.objects.count() == 1
    assert response.status_code == 302
    new_restaurant = Restaurant.objects.get(name='La Trattoria')
    assert new_restaurant.address == 'Dąbrowskiego 3'


@pytest.mark.django_db
def test_list_restaurants(client, restaurant_list):
    url = '/restaurant_list/'
    response = client.get(url)
    assert response.status_code == 200
    assert Restaurant.objects.count() == 3
    assert list(response.context['object_list']) == list(restaurant_list)


@pytest.mark.django_db
def test_add_review(client, restaurant, user):
    # user = User.objects.create(username='dominika12', password='password1234')
    # user.save()
    client.force_login(user=user)
    url = '/add_review/'
    assert Review.objects.count() == 0
    response = client.post(url, {'rate': 5, 'review': 'Przyjemna, włoska knajpka', 'date': datetime.datetime.now(),
                                 'restaurant': restaurant, 'user': user})
    assert Review.objects.count() == 1
    assert response.status_code == 302
    new_review = Review.objects.get(pk=1)
    assert new_review.rate == 5


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
    response = client.delete(f"/delete_review/{review.id}/")
    assert response.status_code == 302
    review_ids = [review.id for review in Review.objects.all()]
    assert review.id not in review_ids


@pytest.mark.django_db
def test_delete_reservation(client, reservation, user):
    client.force_login(user=user)
    reservation_first = Reservation.objects.first()
    response = client.delete(f"/delete_reservation/{reservation.id}/")
    assert response.status_code == 302
    reservation_ids = [reservation.id for reservation in Reservation.objects.all()]
    assert reservation.id not in reservation_ids


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
def select_date_time(client, user):
    client.force_login(user=user)
    url = '/select_date_time/'
    response = client.post(url, {'date': datetime.datetime.today(), 'time': '13:30:00'})
    assert response.status_code == 302


@pytest.mark.django_db
def select_restaurant(client, user, restaurant):
    client.force_login(user=user)
    url = '/select_restaurant/(?P<date>[0-9]{4}-?[0-9]{2}-?[0-9]{2})/(?P<time>[0-9]{2}:?[0-9]{2}:?[0-9]{2})/'
    response = client.post(url, {'restaurant': restaurant})
    assert response.status_code == 302

