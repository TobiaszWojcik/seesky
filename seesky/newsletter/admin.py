from django.contrib import admin
from .models import SpaceObjects, Newsletter, SOPositions, Positions

admin.site.register(SpaceObjects)
admin.site.register(Newsletter)
admin.site.register(Positions)
admin.site.register(SOPositions)
