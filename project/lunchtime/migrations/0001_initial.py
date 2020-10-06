# Generated by Django 3.0.7 on 2020-10-03 15:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('photo', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('address', models.CharField(max_length=256)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=64)),
                ('description', models.TextField()),
                ('staff', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('restaurant', models.CharField(blank=True, default='', max_length=64)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('persons', models.IntegerField()),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lunchtime.Restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.IntegerField(choices=[(5, '*****'), (4, '****'), (3, '***'), (2, '**'), (1, '*')])),
                ('review', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lunchtime.Restaurant')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lunchtime.Meal')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lunchtime.Restaurant')),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lunchtime.Table')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='meal',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lunchtime.Restaurant'),
        ),
    ]
