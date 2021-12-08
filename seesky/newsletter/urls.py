from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page),
    path('newsletter/', views.newsletter_page),
    path('lista/', views.actualizacja),
]
