# Generated by Django 3.2.9 on 2021-12-11 17:35

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0009_auto_20211208_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='s_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 11, 17, 35, 17, 45813, tzinfo=utc)),
        ),
    ]
