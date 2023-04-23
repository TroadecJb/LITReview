from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
    path("", LoginView.as_view(
        template_name="authentication/home.html",
        redirect_authenticated_user=True),
        name="home"
        ),
    path("signup/", views.signup_page, name="signup"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
