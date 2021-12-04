from django.db import models


class Newsletter(models.Model):
    name = models.CharField(max_length=150)
    place = models.TextField()
    lat = models.DecimalField(max_digits=12, decimal_places=7)
    lon = models.DecimalField(max_digits=12, decimal_places=7)
    email = models.EmailField(unique=True, max_length=255)
    token = models.CharField(max_length=24)
    s_time = models.DateTimeField(auto_now_add=True)
    email_time = models.TimeField(default='16:00:00')


class SpaceObjects(models.Model):
    name = models.CharField(max_length=255)
    short = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Positions(models.Model):
    lat = models.DecimalField(max_digits=12, decimal_places=7)
    lon = models.DecimalField(max_digits=12, decimal_places=7)
    so_id = models.ForeignKey(SpaceObjects, on_delete=models.CASCADE)
    time_s = models.DateTimeField()
