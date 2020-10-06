from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.contrib.auth.models import User

from .models import Restaurant, Table, Meal, Reservation, Review
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, View
from .forms import AddUserForm, AddRestaurantForm, AddTableForm, AddMealForm, AddReservationForm, AddReviewForm


# Create your views here.


class LandingPageView(View):
    template = 'base.html'

    def get(self, request):
        return render(request, self.template, {})


class AddUserView(FormView):
    template_name = 'add_user.html'
    form_class = AddUserForm
    success_url = reverse_lazy('main-page')

    def form_valid(self, form):
        User.objects.create(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'],
                            first_name=form.cleaned_data['first_name'],
                            last_name=form.cleaned_data['last_name'],
                            email=form.cleaned_data['email'])
        return super(AddUserView, self).form_valid(form)


class ListRestaurantView(ListView):
    template_name = 'restaurant_list.html'
    model = Restaurant


class AddRestaurantView(FormView):
    template_name = 'add_restaurant.html'
    form_class = AddRestaurantForm
    success_url = reverse_lazy('restaurant-profile')

    def form_valid(self, form):
        Restaurant.objects.create(name=form.cleaned_data['name'],
                                  address=form.cleaned_data['address'],
                                  phone=form.cleaned_data['phone'],
                                  email=form.cleaned_data['email'],
                                  description=form.cleaned_data['description'])
        return super(AddRestaurantView, self).form_valid(form)


class ListTableView(View):
    template = 'table_list.html'

    def get(self, request, restaurant_id):
        tables = Table.objects.filter(restaurant_id=restaurant_id)
        return render(request, self.template, {'tables': tables})


class AddTableView(FormView):
    template_name = 'add_table.html'
    form_class = AddTableForm
    success_url = reverse_lazy('tables-list')

    def form_valid(self, form):
        Table.objects.create(persons=form.cleaned_data['persons'],
                             restaurant=form.cleaned_data['restaurant'])
        return super(AddTableView, self).form_valid(form)


class ListMealView(View):
    template = 'meal_list.html'

    def get(self, request, restaurant_id):
        meals = Meal.objects.filter(restaurant_id=restaurant_id)
        return render(request, self.template, {'meals': meals})


class AddMealView(FormView):
    template_name = 'add_meal.html'
    form_class = AddMealForm
    success_url = reverse_lazy('meals-list')

    def form_valid(self, form):
        Meal.objects.create(category=form.cleaned_data['category'], 
                            name=form.cleaned_data['name'],
                            description=form.cleaned_data['description'],
                            restaurant=form.cleaned_data['restaurant'],
                            price=form.cleaned_data['price'])
        return super(AddMealView, self).form_valid(form)


class ListReservationView(View):
    template = 'user_reservations.html'

    def get(self, request, user_id):
        reservations = Reservation.objects.filter(user_id=user_id)
        return render(request, self.template, {'reservations': reservations})


class AddReservationView(FormView):
    template_name = 'add_reservation.html'
    form_class = AddReservationForm
    success_url = reverse_lazy('reservations-list')

    def form_valid(self, form):
        Reservation.objects.create(restaurant=form.cleaned_data['restaurant'],
                                   table=form.cleaned_data['table'],
                                   date=form.cleaned_data['date'],
                                   time=form.cleaned_data['time'],
                                   meal=form.cleaned_data['meal'])
        return super(AddReservationView, self).form_valid(form)


def free_table(restaurant_id, table_id):
    restaurant = Restaurant.objects.filter(restaurant_id=restaurant_id)
    table = Table.objects.filter(restaurant=restaurant, table_id=table_id)
    return None


class ListReviewView(View):
    template = 'restaurant_reviews.html'

    def get(self, request, restaurant_id):
        reviews = Review.objects.filter(restaurant_id=restaurant_id)
        return render(request, self.template, {'reviews': reviews})


class AddReviewView(FormView):
    template_name = 'add_review.html'
    form_class = AddReviewForm
    success_url = reverse_lazy('restaurant-reviews')
    
    def form_valid(self, form):
        Review.objects.create(restaurant=form.cleaned_data['restaurant'],
                              rate=form.cleaned_data['rate'],
                              review=form.cleaned_data['review'])
        return super(AddReviewView, self).form_valid(form)
