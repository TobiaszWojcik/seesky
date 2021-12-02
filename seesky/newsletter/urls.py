from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page),
    path('newsletter/', views.newsletter_page),
    path('show/<place>', views.show_page)
]