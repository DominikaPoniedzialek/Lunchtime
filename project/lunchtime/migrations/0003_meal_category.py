# Generated by Django 3.0.7 on 2020-10-05 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lunchtime', '0002_meal_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='category',
            field=models.IntegerField(choices=[(1, 'śniadanie'), (2, 'lunch'), (3, 'kolacja')], default=0),
            preserve_default=False,
        ),
    ]
