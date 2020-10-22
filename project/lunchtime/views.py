from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .models import Restaurant, Table, Meal, Reservation, Review
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, View, UpdateView, CreateView, DeleteView
from .forms import AddUserForm, AddTableForm, LoginForm, SelectRestaurantForm, SelectDateAndTimeForm


# Create your views here.


class LandingPageView(View):
    """Display main page of application."""
    template = 'base.html'

    def get(self, request):
        return render(request, self.template, {})


class ContactPageView(View):
    """Display contact page to owner of application."""
    template = 'contact.html'

    def get(self, request):
        return render(request, self.template, {})


class AddUserView(FormView):
    """Add new user to database."""
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
    """Allows user to log in to application."""
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('main-page')

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            try:
                login(self.request, user)
            except ValueError:
                form.add_error('username', 'Niepoprawny użytkownik')
                return self.form_invalid(form)
        return super(LoginView, self).form_valid(form)


class LogoutView(View):
    """Allows user to log out from application"""
    def get(self, request):
        logout(request)
        return render(request, 'base.html')


class AddRestaurantView(PermissionRequiredMixin, CreateView):
    """Add restaurant to database."""
    model = Restaurant
    fields = ['name', 'address', 'phone', 'email', 'description', 'logo']
    permission_required = 'lunchtime.add_restaurant'


class ModifyRestaurantView(PermissionRequiredMixin, UpdateView):
    """Modify restaurant details."""
    model = Restaurant
    fields = ['name', 'address', 'phone', 'email', 'description', 'logo']
    template_name_suffix = '_update_form'
    permission_required = 'lunchtime.change_restaurant'


class DeleteRestaurantView(PermissionRequiredMixin, DeleteView):
    """Delete restaurant from database."""
    template_name = 'lunchtime/restaurant_confirm_delete.html'
    model = Restaurant
    success_url = reverse_lazy('restaurants-list')
    permission_required = 'lunchtime.delete_restaurant'


class ListRestaurantView(ListView):
    """Display list of restaurants."""
    template_name = 'restaurant_list.html'
    model = Restaurant


class RestaurantView(View):
    """Display details about restaurant."""
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


class AddTableView(PermissionRequiredMixin, CreateView):
    """Add table to database."""
    template_name = 'lunchtime/table_form.html'
    form_class = AddTableForm
    permission_required = 'lunchtime.add_table'

    # def form_valid(self, form):
    #     Table.objects.create(restaurant=form.cleaned_data['restaurant'], persons=form.cleaned_data['persons'])
    #     return super(AddTableView, self).form_valid(form)


class DeleteTableView(PermissionRequiredMixin, DeleteView):
    """Delete table from database."""
    template_name = 'lunchtime/table_confirm_delete.html'
    model = Table
    permission_required = 'lunchtime.delete_table'


class AddMealView(PermissionRequiredMixin, CreateView):
    """Add meal to database."""
    model = Meal
    fields = ['restaurant', 'category', 'name', 'description', 'price']
    permission_required = 'lunchtime.add_meal'


class ModifyMealView(PermissionRequiredMixin, UpdateView):
    """Modify meal details."""
    model = Meal
    fields = ['restaurant', 'category', 'name', 'description', 'price']
    template_name_suffix = '_update_form'
    permission_required = 'lunchtime.change_meal'


class DeleteMealView(PermissionRequiredMixin, DeleteView):
    """Delete meal from database."""
    template_name = 'lunchtime/restaurant_confirm_delete.html'
    model = Restaurant
    permission_required = 'lunchtime.delete_meal'


class ListReservationView(LoginRequiredMixin, ListView):
    """Display list of user's reservations"""
    template_name = 'lunchtime/reservations_list.html'
    model = Reservation

    def get_queryset(self):
        """Return list of user's reservation."""
        user = self.request.user
        return Reservation.objects.filter(user=user)


class SelectDateAndTimeView(LoginRequiredMixin, View):
    """Allows user to select date and time of reservation."""
    def get(self, request):
        """Return form to select date and time."""
        form = SelectDateAndTimeForm()
        return render(request, 'lunchtime/reservation_form.html', {'form': form})

    def post(self, request):
        """Save data about selected date and time and redirect to select restaurant form."""
        form = SelectDateAndTimeForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            return redirect(f'/select_restaurant/{date}/{time}/')
        return render(request, 'lunchtime/reservation_form.html', {'form': form})


class SelectRestaurantView(LoginRequiredMixin, View):
    """Allows user to select restaurant for reservation."""

    def get(self, request, date, time):
        """Return form to select restaurant."""
        form = SelectRestaurantForm()
        return render(request, 'select_restaurant.html', {'form': form})

    def post(self, request, date, time):
        """Save data about selected restaurant and redirect to reservation table form."""
        form = SelectRestaurantForm(request.POST)
        if form.is_valid():
            restaurant = Restaurant.objects.get(pk=form.cleaned_data['restaurant'].id)
            return redirect(f'/add_reservation/{date}/{time}/{restaurant.id}')
        return render(request, 'select_restaurant.html', {'form': form})


class AddReservationView(LoginRequiredMixin, View):
    template_name = 'lunchtime/reservation_table.html'

    def get(self, request, date, time, restaurant_id):
        available_tables = Table.objects.filter(restaurant_id=restaurant_id, reserved=False)
        restaurant_menu = Meal.objects.filter(restaurant_id=restaurant_id)
        if available_tables:
            return render(request, self.template_name, {'available_tables': available_tables,
                                                        'menu': restaurant_menu})
        message = 'Brak wolnych stolików. Zmień datę lub godzinę.'
        return render(request, self.template_name, {'message': message})

    def post(self, request, date, time, restaurant_id):
        table_id = request.POST.get('table_id')
        meals = Meal.objects.filter(id__in=request.POST.getlist('meals'))
        user = self.request.user
        new_reservation = Reservation.objects.create(restaurant_id=restaurant_id, table_id=table_id, date=date,
                                                     time=time, user=user)
        new_reservation.meal.set(meals)
        table = Table.objects.get(pk=table_id)
        table.reserved = True
        table.save()
        return redirect('/reservation_list')


# class AddReservationView(LoginRequiredMixin, CreateView):
#     # model = Reservation
#     form_class = AddReservationForm
#     template_name = 'lunchtime/reservation_form.html'
#     # fields = ['restaurant', 'table', 'date', 'time', 'meal']
#     success_url = reverse_lazy('reservations-list')
#
#     def form_valid(self, form):
#         try:
#             form.instance.user = self.request.user
#             return super().form_valid(form)
#         except IntegrityError:
#             form.add_error('table', 'Stolik jest już zajęty, wybierz inny, lub zmień godzinę')
#             return self.form_invalid(form)


# class ModifyReservationView(LoginRequiredMixin, UpdateView):
#     """Modify reservation details."""
#     model = Reservation
#     fields = ['restaurant', 'table', 'date', 'time', 'meal']
#     template_name_suffix = '_update_form'
#     success_url = reverse_lazy('reservations-list')


class DeleteReservationView(LoginRequiredMixin, DeleteView):
    """Delete reservation from database."""
    template_name = 'lunchtime/reservation_confirm_delete.html'
    model = Reservation
    success_url = reverse_lazy('reservations-list')


class ListReviewsView(LoginRequiredMixin, ListView):
    """Display list of user's review."""
    template_name = 'lunchtime/reviews_list.html'
    model = Review

    def get_queryset(self):
        """Return list of user's review."""
        user = self.request.user
        return Review.objects.filter(user=user)


class AddReviewView(LoginRequiredMixin, CreateView):
    """Add review to database."""
    model = Review
    template_name = 'lunchtime/review_form.html'
    fields = ['restaurant', 'rate', 'review']
    success_url = reverse_lazy('reviews-list')
    
    def form_valid(self, form):
        """Save data and add review to database."""
        form.instance.user = self.request.user
        return super(AddReviewView, self).form_valid(form)


class DeleteReviewView(LoginRequiredMixin, DeleteView):
    """Delete review from database."""
    template_name = 'lunchtime/review_confirm_delete.html'
    model = Review
    success_url = reverse_lazy('reviews-list')


