from django import forms
from django.contrib.auth.models import User
from .models import Restaurant, Table, Meal, STARS, CATEGORIES


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


class UserProfileForm(forms.Form):
    restaurant = forms.CharField(label='restauracja')


class AddRestaurantForm(forms.Form):
    name = forms.CharField(label='nazwa', max_length=64)
    address = forms.CharField(label='adres', max_length=256)
    phone = forms.CharField(label='telefon', max_length=20)
    email = forms.EmailField(label='adres e-mail')
    description = forms.CharField(label='opis', widget=forms.Textarea)


class AddTableForm(forms.Form):
    persons = forms.IntegerField(label='Ilość gości', min_value=1)
    restaurant = forms.ModelChoiceField(Restaurant.objects.all(), label='restauracja')


class AddMealForm(forms.Form):
    category = forms.TypedMultipleChoiceField(label='kategoria', choices=CATEGORIES, coerce=int)
    name = forms.CharField(label='nazwa', max_length=36)
    description = forms.CharField(label='opis dania', max_length=264, widget=forms.Textarea)
    restaurant = forms.ModelChoiceField(Restaurant.objects.all())
    price = forms.DecimalField(label='cena', min_value=0, max_digits=5, decimal_places=2)


class AddReservationForm(forms.Form):
    restaurant = forms.ModelChoiceField(Restaurant.objects.all(), label='restauracja')
    table = forms.ModelChoiceField(Table.objects.filter(restaurant__name=restaurant), label='stolik')
    date = forms.DateField(label='data', input_formats=['%d.%m.%y'], widget=forms.DateInput)
    time = forms.TimeField(label='godzina', input_formats=['%h:%m'], widget=forms.TimeInput)
    meal = forms.ModelChoiceField(Meal.objects.filter(restaurant__name=restaurant), label='posiłek')


class AddReviewForm(forms.Form):
    restaurant = forms.ModelChoiceField(Restaurant.objects.all(), label='restauracja')
    rate = forms.TypedChoiceField(label='ocena', choices=STARS, coerce=int)
    review = forms.CharField(label='recenzja', widget=forms.Textarea)
