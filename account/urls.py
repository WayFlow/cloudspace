from django.urls import path

from .views import LoginAPIView, RegisterAPIView, LogoutView, AccountView


urlpatterns = [
    path("register", RegisterAPIView.as_view(), name="register"),
    path("login", LoginAPIView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("me", AccountView.as_view(), name="me"),
]
