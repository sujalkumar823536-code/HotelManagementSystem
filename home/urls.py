from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path("", views.index , name='home'),
    path("login", views.user_login , name='login'),
    path("signin", views.user_signin , name='signin'),
    path("logout", views.user_logout , name='logout'),
    path("test", views.test , name='test'),
    path("booking", views.booking , name='booking'),
    path("payment", views.payment , name='payment'),
    path("confirm_booking", views.confirm_booking, name="confirm_booking"),
]