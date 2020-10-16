import datetime
from django import forms
from django.contrib.auth.models import User
from .models import Restaurant, Table, Meal, Reservation, Review


class AddUserForm(forms.Form):
    username = forms.CharField(label='login', max_length=64)
    password = forms.CharField(label='hasło', widget=forms.PasswordInput)
    password_repeat = forms.CharField(label='powtórz hasło', widget=forms.PasswordInput)
    first_name = forms.CharField(label='imię', max_length=64)
    last_name = forms.CharField(label='nazwisko', max_length=64)
    email = forms.EmailField(label='adres e-mail', max_length=64)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            user = User.objects.filter(username=username).exists()
            if user:
                raise forms.ValidationError("Podana nazwa użytkownika jest już zajęta.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        password_repeat = self.cleaned_data.get('password_repeat')
        if password and password_repeat:
            if password != password_repeat:
                raise forms.ValidationError("Podane hasła nie są takie same.")
        return password


# class UserProfileForm(forms.Form):
#     restaurant = forms.CharField(label='restauracja')

class LoginForm(forms.Form):
    username = forms.CharField(label='login', max_length=24)
    password = forms.CharField(label='hasło', widget=forms.PasswordInput)


class AddRestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'phone', 'email', 'description', 'logo']


class AddTableForm(forms.Form):
    restaurant = forms.ModelChoiceField(Restaurant.objects.all(), label='restauracja')
    persons = forms.IntegerField(label='ilość osób przy stoliku', min_value=1)


class AddMealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['restaurant', 'category', 'name', 'description', 'price']


class AddReservationForm(forms.Form):
    meal = forms.ModelMultipleChoiceField(Meal.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Reservation
        fields = ['restaurant', 'table', 'date', 'time', 'meal']
        widgets = {'meal': forms.CheckboxSelectMultiple}

    def clean_date(self):
        date_reservation = self.cleaned_data.get('date')
        if date_reservation:
            if str(date_reservation) < str(datetime.date.today()):
                raise forms.ValidationError('Podana data jest z przeszłości')
        return date_reservation


class AddReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['restaurant', 'rate', 'review']

