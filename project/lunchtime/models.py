from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


STARS = (
    (5, "*****"),
    (4, "****"),
    (3, "***"),
    (2, "**"),
    (1, "*"),
)

CATEGORIES = (
    (1, "śniadanie"),
    (2, "lunch"),
    (3, "kolacja"),
)


class Restaurant(models.Model):
    """Stores restaurant."""
    name = models.CharField(verbose_name='nazwa', max_length=64)
    address = models.CharField(verbose_name='adres', max_length=256)
    phone = models.CharField(verbose_name='telefon', max_length=20)
    email = models.EmailField(verbose_name='adres e-mail', max_length=64)
    description = models.TextField(verbose_name='opis')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='przedstawiciel restauracji', default=True)
    logo = models.ImageField(verbose_name='logo', upload_to='media/')

    def __str__(self):
        """Return name of restaurant."""
        return self.name

    def get_absolute_url(self):
        """Return url for restaurant object."""
        return reverse('restaurant-detail', kwargs={'restaurant_id': self.id})

    class Meta:
        """Display restaurants ordered by name."""
        ordering = ['name']


class Table(models.Model):
    """Stores table. Related to model Restaurant"""
    persons = models.IntegerField(verbose_name='liczba osób')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name='restauracja')
    reserved = models.BooleanField(verbose_name='zarezerwowany', default=False)

    def __str__(self):
        """Return number of persons."""
        return f'{self.persons}-osobowy'

    def get_absolute_url(self):
        return reverse('restaurant-detail', kwargs={'restaurant_id': self.restaurant.id})


class Meal(models.Model):
    """Stores meal. Related to model Restaurant."""
    category = models.IntegerField(choices=CATEGORIES, verbose_name='kategoria')
    name = models.CharField(verbose_name='nazwa', max_length=64)
    description = models.TextField(verbose_name='opis')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name='restauracja')
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='cena')

    class Meta:
        """Display meals ordered by category."""
        ordering = ['category']

    def __str__(self):
        """Return name of meal."""
        return self.name

    def get_absolute_url(self):
        return reverse('restaurant-detail', kwargs={'restaurant_id': self.restaurant.id})


class Reservation(models.Model):
    """Stores reservation. Related to models Restaurant, Table, Meal."""
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name='restauracja')
    table = models.ForeignKey(Table, on_delete=models.CASCADE, verbose_name='stolik')
    date = models.DateField(verbose_name='data rezerwacji')
    time = models.TimeField(verbose_name='godzina rezerwacji')
    meal = models.ManyToManyField(Meal, verbose_name='posiłek')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='użytkownik')

    class Meta:
        """Display reservations ordered by date."""
        ordering = ['-date']


class Review(models.Model):
    """Stores review. Related to model Restaurant"""
    rate = models.IntegerField(choices=STARS, verbose_name='ocena')
    review = models.TextField(verbose_name='recenzja')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name='restauracja')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='użytkownik')
    date = models.DateTimeField(auto_now_add=True, verbose_name='data')

    class Meta:
        """Display reviews ordered by date."""
        ordering = ['-date']

