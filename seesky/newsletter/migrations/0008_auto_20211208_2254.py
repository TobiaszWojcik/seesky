# Generated by Django 3.2.9 on 2021-12-08 22:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0007_alter_newsletter_s_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsletter',
            name='valid',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='s_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 8, 22, 54, 28, 44233)),
        ),
    ]
