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
from django.contrib import admin
from django.urls import path
from lunchtime.views import LandingPageView, AddUserView, AddRestaurantView, ListRestaurantView, ListTableView, \
    AddTableView, ListMealView, AddMealView, AddReservationView, ListReservationView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name='main-page'),
    path('add_user/', AddUserView.as_view(), name='add-user'),
    path('restaurant_list/', ListRestaurantView.as_view(), name='restaurants-list'),
    path('add_restaurant/', AddRestaurantView.as_view(), name='add-restaurant'),
    path('table_list/<int:restaurant_id>/', ListTableView.as_view(), name='tables-list'),
    path('add_table/', AddTableView.as_view(), name='add-table'),
    path('meal_list/<int:restaurant_id>/', ListMealView.as_view(), name='meals-list'),
    path('add_meal/', AddMealView.as_view(), name='add-meal'),
    path('reservation_list/<int:user_id>/', ListReservationView.as_view(), name='meals-list'),
    path('add_reservation/', AddReservationView.as_view(), name='add-reservation'),
]
