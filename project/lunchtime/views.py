from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User

from .models import Restaurant, Table, Meal, Reservation, Review
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, View, UpdateView, CreateView, DeleteView
from .forms import AddUserForm, AddRestaurantForm, AddTableForm, AddMealForm, AddReservationForm, AddReviewForm, \
    LoginForm


# Create your views here.


class LandingPageView(View):
    template = 'base.html'

    def get(self, request):
        return render(request, self.template, {})


class ContactPageView(View):
    template = 'contact.html'

    def get(self, request):
        return render(request, self.template, {})


class AddUserView(FormView):
    template_name = 'add_user.html'
    form_class = AddUserForm
    success_url = reverse_lazy('main-page')

    def form_valid(self, form):
        User.objects.create_user(username=form.cleaned_data['username'],
                                 password=form.cleaned_data['password'],
                                 first_name=form.cleaned_data['first_name'],
                                 last_name=form.cleaned_data['last_name'],
                                 email=form.cleaned_data['email'])
        return super(AddUserView, self).form_valid(form)


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            try:
                login(self.request, user)
            except ValueError:
                form.add_error('username', 'Niepoprawny użytkownik')
                return self.form_invalid(form)
            # return HttpResponse("Niepoprawny użytkownik")
        return super(LoginView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, 'base.html')


class AddRestaurantView(PermissionRequiredMixin, CreateView):
    model = Restaurant
    fields = ['name', 'address', 'phone', 'email', 'description', 'logo']
    success_url = reverse_lazy('restaurants-list')
    permission_required = 'lunchtime.add_restaurant'


class ModifyRestaurantView(PermissionRequiredMixin, UpdateView):
    model = Restaurant
    fields = ['name', 'address', 'phone', 'email', 'description', 'logo']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('restaurants-list')
    permission_required = 'lunchtime.change_restaurant'


class DeleteRestaurantView(PermissionRequiredMixin, DeleteView):
    template_name = 'lunchtime/restaurant_confirm_delete.html'
    model = Restaurant
    success_url = '/'
    permission_required = 'lunchtime.delete_restaurant'


class ListRestaurantView(ListView):
    template_name = 'restaurant_list.html'
    model = Restaurant


class RestaurantView(View):
    template = 'restaurant_view.html'

    def get(self, request, restaurant_id):
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        menu_breakfast = Meal.objects.filter(restaurant_id=restaurant_id, category=1)
        menu_lunch = Meal.objects.filter(restaurant_id=restaurant_id, category=2)
        menu_dinner = Meal.objects.filter(restaurant_id=restaurant_id, category=3)
        reviews = Review.objects.filter(restaurant_id=restaurant_id)
        tables = Table.objects.filter(restaurant_id=restaurant_id)
        reservations = Reservation.objects.filter(restaurant_id=restaurant_id)
        return render(request, self.template, {'restaurant': restaurant,
                                               'menu_breakfast': menu_breakfast,
                                               'menu_lunch': menu_lunch,
                                               'menu_dinner': menu_dinner,
                                               'reviews': reviews,
                                               'tables': tables,
                                               'reservations': reservations})


class ListTableView(View):
    template = 'table_list.html'

    def get(self, request, restaurant_id):
        tables = Table.objects.filter(restaurant_id=restaurant_id)
        return render(request, self.template, {'tables': tables})


class AddTableView(PermissionRequiredMixin, FormView):
    template_name = 'add_table.html'
    form_class = AddTableForm
    success_url = reverse_lazy('tables-list')
    permission_required = 'lunchtime.add_table'

    def form_valid(self, form):
        Table.objects.create(restaurant=form.cleaned_data['restaurant'], persons=form.cleaned_data['persons'])
        return super(AddTableView, self).form_valid(form)


class DeleteTableView(PermissionRequiredMixin, DeleteView):
    template_name = 'lunchtime/table_confirm_delete.html'
    model = Table
    success_url = reverse_lazy('tables-list')
    permission_required = 'lunchtime.delete_table'


class AddMealView(PermissionRequiredMixin, CreateView):
    model = Meal
    fields = ['restaurant', 'category', 'name', 'description', 'price']
    permission_required = 'lunchtime.add_meal'


class ModifyMealView(PermissionRequiredMixin, UpdateView):
    model = Meal
    fields = ['restaurant', 'category', 'name', 'description', 'price']
    template_name_suffix = '_update_form'
    permission_required = 'lunchtime.change_meal'


class DeleteMealView(PermissionRequiredMixin, DeleteView):
    template_name = 'lunchtime/restaurant_confirm_delete.html'
    model = Restaurant
    permission_required = 'lunchtime.delete_meal'


class ListReservationView(LoginRequiredMixin, ListView):
    template_name = 'lunchtime/reservations_list.html'
    model = Reservation

    def get_queryset(self):
        user = self.request.user
        return Reservation.objects.filter(user=user)


class AddReservationView(LoginRequiredMixin, CreateView):
    model = Reservation
    template_name = 'lunchtime/reservation_form.html'
    fields = ['restaurant', 'table', 'date', 'time', 'meal']
    success_url = reverse_lazy('reservations-list')

    def form_valid(self, form):
        try:
            form.instance.user = self.request.user
            return super().form_valid(form)
        except IntegrityError:
            form.add_error('table', 'Stolik jest już zajęty, wybierz inny, lub zmień godzinę')
            return self.form_invalid(form)


class ModifyReservationView(LoginRequiredMixin, UpdateView):
    model = Reservation
    fields = ['restaurant', 'table', 'date', 'time', 'meal']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('reservations-list')


class DeleteReservationView(LoginRequiredMixin, DeleteView):
    template_name = 'lunchtime/reservation_confirm_delete.html'
    model = Reservation
    success_url = reverse_lazy('reservations-list')


class ListReviewsView(LoginRequiredMixin, ListView):
    template_name = 'lunchtime/reviews_list.html'
    model = Review

    def get_queryset(self):
        user = self.request.user
        return Review.objects.filter(user=user)


class AddReviewView(LoginRequiredMixin, CreateView):
    model = Review
    template_name = 'lunchtime/review_form.html'
    fields = ['restaurant', 'rate', 'review']
    success_url = reverse_lazy('reviews-list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddReviewView, self).form_valid(form)


class DeleteReviewView(LoginRequiredMixin, DeleteView):
    template_name = 'lunchtime/review_confirm_delete.html'
    model = Review
    success_url = reverse_lazy('reviews-list')


