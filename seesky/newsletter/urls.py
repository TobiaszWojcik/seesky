from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page),
    path('newsletter/', views.newsletter_page),
    path('show/', views.show_page),
    path('actual/', views.actualizacja),

]