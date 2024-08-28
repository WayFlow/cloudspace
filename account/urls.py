from django.urls import path

from .views import SignInView, SignUpView


urlpatterns = [
    path("sign-up", SignUpView.as_view(), name="signup"),
    path("sign-in", SignInView.as_view(), name="signin"),
]
