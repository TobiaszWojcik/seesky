# Generated by Django 3.2.9 on 2021-12-11 17:45

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0010_alter_newsletter_s_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='s_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 11, 17, 45, 24, 192784, tzinfo=utc)),
        ),
    ]
