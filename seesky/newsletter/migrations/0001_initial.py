# Generated by Django 3.2.9 on 2021-12-02 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('place', models.TextField()),
                ('lat', models.DecimalField(decimal_places=7, max_digits=12)),
                ('lon', models.DecimalField(decimal_places=7, max_digits=12)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('token', models.CharField(max_length=24)),
                ('s_time', models.DateTimeField(auto_now_add=True)),
                ('email_time', models.TimeField(default='16:00:00')),
            ],
        ),
        migrations.CreateModel(
            name='SpaceObjects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('short', models.CharField(max_length=20)),
                ('exp_time', models.DateTimeField()),
            ],
        ),
    ]
