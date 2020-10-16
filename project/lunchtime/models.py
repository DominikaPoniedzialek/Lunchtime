from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

# Create your models here.
from django.urls import reverse

fs = FileSystemStorage(location='/media/photos/')


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


# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     restaurant = models.CharField(max_length=64, default='', blank=True)
#
#     @receiver(post_save, sender=User)
#     def create_user_profile(sender, instance, created, **kwargs):
#         if created:
#             UserProfile.objects.create(user=instance)
#
#     @receiver(post_save, sender=User)
#     def save_user_profile(sender, instance, **kwargs):
#         instance.userprofile.save()


class Restaurant(models.Model):
    name = models.CharField(verbose_name='nazwa', max_length=64)
    address = models.CharField(verbose_name='adres', max_length=256)
    phone = models.CharField(verbose_name='telefon', max_length=20)
    email = models.EmailField(verbose_name='adres e-mail', max_length=64)
    description = models.TextField(verbose_name='opis')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='przedstawiciel restauracji', default=True)
    logo = models.ImageField(verbose_name='logo', upload_to='media/')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Table(models.Model):
    persons = models.IntegerField(verbose_name='liczba osób')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name='restauracja')

    def __str__(self):
        return f'{self.persons}-osobowy'


class Meal(models.Model):
    category = models.IntegerField(choices=CATEGORIES, verbose_name='kategoria')
    name = models.CharField(verbose_name='nazwa', max_length=64)
    description = models.TextField(verbose_name='opis')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name='restauracja')
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='cena')

    class Meta:
        ordering = ['category']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('restaurant-detail', kwargs={'restaurant_id': self.restaurant.id})


class Reservation(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name='restauracja')
    table = models.ForeignKey(Table, on_delete=models.CASCADE, verbose_name='stolik')
    date = models.DateField(verbose_name='data rezerwacji')
    time = models.TimeField(verbose_name='godzina rezerwacji')
    meal = models.ManyToManyField(Meal, verbose_name='posiłek')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='użytkownik')

    class Meta:
        ordering = ['-date']


class Review(models.Model):
    rate = models.IntegerField(choices=STARS, verbose_name='ocena')
    review = models.TextField(verbose_name='recenzja')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name='restauracja')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='użytkownik')
    date = models.DateTimeField(auto_now_add=True, verbose_name='data')

    class Meta:
        ordering = ['-date']

