# Generated by Django 3.2.9 on 2021-12-04 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0004_delete_sopositions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spaceobjects',
            name='exp_time',
        ),
    ]
