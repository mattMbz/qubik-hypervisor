'''app_auth URL Configuration'''

from django.urls import path

from . import views


urlpatterns = [
    path("login", views.signin, name="signin"),
    path("signup", views.signup, name="signup"),
    path("logout", views.logout_view, name="logout"),
]