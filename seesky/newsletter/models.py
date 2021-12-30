from datetime import datetime
from django.db import models
"""
Set of classes responsible for maintaining the database.
"""


class Newsletter(models.Model):
    """
    Class handling the user information database
    """
    name = models.CharField(max_length=150)
    place = models.TextField()
    lat = models.DecimalField(max_digits=12, decimal_places=7)
    lon = models.DecimalField(max_digits=12, decimal_places=7)
    email = models.EmailField(unique=True, max_length=255)
    token = models.CharField(max_length=100)
    s_time = models.DateTimeField(default=datetime.now())
    email_time = models.TimeField(default='16:00:00')
    valid = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class SpaceObjects(models.Model):
    """
    Class handling a database of information about objects currently in space.
    """
    name = models.CharField(max_length=255)
    short = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Positions(models.Model):
    """
    Class handling a database of geographic coordinates information about objects space.
    """
    lat = models.DecimalField(max_digits=12, decimal_places=7)
    lon = models.DecimalField(max_digits=12, decimal_places=7)
    short = models.CharField(max_length=100, default='null')
    time = models.DateTimeField()

    def __str__(self):
        return f'{self.short} - {self.lat} - {self.lon} - {self.time}'
