# Generated by Django 3.0.7 on 2020-10-06 18:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lunchtime', '0004_remove_meal_photo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='meal',
            options={'ordering': ['category']},
        ),
    ]