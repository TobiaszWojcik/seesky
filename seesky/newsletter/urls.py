from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('newsletter/', views.newsletter_page, name='newsletter_page'),
    path('lista/', views.actualizacja, name='list_page'),
    path('validate/<email>/<token>/', views.validate),
    path('show/', views.show_page),
    path('contact/', views.contact_page, name='contact_page'),
    path('about/', views.about_page, name='about_page')
]
