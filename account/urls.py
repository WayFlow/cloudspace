from django.urls import path

from .views import SignInView, SignUpView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView

)


urlpatterns = [
    path("sign-up", SignUpView.as_view(), name="signup"),
    path("sign-in", SignInView.as_view(), name="signin"),
    path("token/refresh", TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify', TokenVerifyView.as_view(), name='token_verify'),
]
