import datetime
from django import forms
from django.contrib.auth.models import User
from .models import Restaurant, Meal, Reservation, Review, Table


class AddUserForm(forms.Form):
    """Add new user to database."""
    username = forms.CharField(label='login', max_length=64)
    password1 = forms.CharField(label='hasło', widget=forms.PasswordInput)
    password2 = forms.CharField(label='powtórz hasło', widget=forms.PasswordInput)
    first_name = forms.CharField(label='imię', max_length=64)
    last_name = forms.CharField(label='nazwisko', max_length=64)
    email = forms.EmailField(label='adres e-mail', max_length=64)

    def clean_username(self):
        """Check if username already exists in database. Return unique username."""
        username = self.cleaned_data.get('username')
        if username:
            user = User.objects.filter(username=username).exists()
            if user:
                raise forms.ValidationError("Podana nazwa użytkownika jest już zajęta.")
        return username

    def clean_password1(self):
        """Check if passwords provided by user are the same. Return correct password."""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Podane hasła nie są takie same.")
        return password1


class LoginForm(forms.Form):
    """Login user to application."""
    username = forms.CharField(label='login', max_length=24)
    password = forms.CharField(label='hasło', widget=forms.PasswordInput)


class AddRestaurantForm(forms.ModelForm):
    """Add new restaurant to database."""
    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'phone', 'email', 'description', 'logo']


class AddTableForm(forms.ModelForm):
    """Add new table to database."""
    restaurant = forms.ModelChoiceField(Restaurant.objects.all(), label='restauracja')
    persons = forms.IntegerField(label='ilość osób przy stoliku', min_value=1)

    class Meta:
        model = Table
        fields = ['restaurant', 'persons']


class AddMealForm(forms.ModelForm):
    """Add meal to database."""
    class Meta:
        model = Meal
        fields = ['restaurant', 'category', 'name', 'description', 'price']


class SelectRestaurantForm(forms.Form):
    """Select restaurant for reservation."""
    restaurant = forms.ModelChoiceField(Restaurant.objects.all(), label='Restauracja')


class SelectDateAndTimeForm(forms.ModelForm):
    """Select date and time of reservation."""
    class Meta:
        model = Reservation
        fields = ['date', 'time']

    def clean_date(self):
        """Check if date is not from the past. Return correct date."""
        date_reservation = self.cleaned_data.get('date')
        if date_reservation:
            if date_reservation < datetime.date.today():
                raise forms.ValidationError('Podana data jest z przeszłości')
        return date_reservation


class AddReviewForm(forms.ModelForm):
    """Add review to database."""
    class Meta:
        model = Review
        fields = ['restaurant', 'rate', 'review']

