"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from lunchtime.views import LandingPageView, AddUserView, AddRestaurantView, ModifyRestaurantView, ListRestaurantView, \
    DeleteRestaurantView, RestaurantView, AddTableView, DeleteTableView, AddMealView, ModifyMealView, \
    DeleteMealView, SelectRestaurantView, AddReservationView, ListReservationView, ModifyReservationView, \
    DeleteReservationView, ListReviewsView, AddReviewView, DeleteReviewView, ContactPageView, LoginView, LogoutView, \
    SelectDateAndTimeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name='main-page'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('add_user/', AddUserView.as_view(), name='add-user'),
    path('login/', LoginView.as_view(), name='login-user'),
    path('logout/', LogoutView.as_view(), name='logout-user'),
    path('restaurant_list/', ListRestaurantView.as_view(), name='restaurants-list'),
    path('add_restaurant/', AddRestaurantView.as_view(), name='add-restaurant'),
    path('modify_restaurant/<int:pk>/', ModifyRestaurantView.as_view(), name='modify-restaurant'),
    path('delete_restaurant/<int:pk>/', DeleteRestaurantView.as_view(), name='delete-restaurant'),
    path('restaurant/<int:restaurant_id>/', RestaurantView.as_view(), name='restaurant-detail'),
    path('add_table/', AddTableView.as_view(), name='add-table'),
    path('delete_table/<int:pk>/', DeleteTableView.as_view(), name='delete-table'),
    path('add_meal/', AddMealView.as_view(), name='add-meal'),
    path('modify_meal/<int:pk>/', ModifyMealView.as_view(), name='modify-meal'),
    path('delete_meal/<int:pk>/', DeleteMealView.as_view(), name='delete-meal'),
    path('reservation_list/', ListReservationView.as_view(), name='reservations-list'),
    path('select_date_time', SelectDateAndTimeView.as_view(), name='select-date-time'),
    re_path(r'select_restaurant/(?P<date>[0-9]{4}-?[0-9]{2}-?[0-9]{2})/(?P<time>[0-9]{2}:?[0-9]{2}:?[0-9]{2})/', SelectRestaurantView.as_view(), name='select-restaurant'),
    re_path(r'add_reservation/(?P<date>[0-9]{4}-?[0-9]{2}-?[0-9]{2})/(?P<time>[0-9]{2}:?[0-9]{2}:?[0-9]{2})/(?P<restaurant_id>\d+)/', AddReservationView.as_view(), name='add-reservation'),
    path('modify_reservation/<int:pk>/', ModifyReservationView.as_view(), name='modify-reservation'),
    path('delete_reservation/<int:pk>/', DeleteReservationView.as_view(), name='delete-reservation'),
    path('review_list/', ListReviewsView.as_view(), name='reviews-list'),
    path('add_review/', AddReviewView.as_view(), name='add-review'),
    path('delete_review/<int:pk>/', DeleteReviewView.as_view(), name='delete-review'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
