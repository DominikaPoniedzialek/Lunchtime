from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver

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


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    restaurant = models.CharField(max_length=64, default='', blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()


class Restaurant(models.Model):
    name = models.CharField(max_length=64)
    address = models.CharField(max_length=256)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=64)
    description = models.TextField()
    staff = models.ManyToManyField(User)

    def __str__(self):
        return self.name


class Table(models.Model):
    persons = models.IntegerField(null=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.persons}-osobowy'


class Meal(models.Model):
    category = models.IntegerField(choices=CATEGORIES)
    name = models.CharField(max_length=64)
    description = models.TextField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        ordering = ['category']

    def __str__(self):
        return self.name


class Reservation(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']


class Review(models.Model):
    rate = models.IntegerField(choices=STARS)
    review = models.TextField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

