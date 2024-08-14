from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView

)

from utils.constants import ResponseDataKey as RSP_KEY
from utils.constants import ResponseMessage as RSP_MSG

from .serializers import AccountSerializer

Account = get_user_model()


class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            token = RefreshToken.for_user(account)
            creds = {
                RSP_KEY.MESSAGE_KEY: RSP_MSG.SUCCESSFULL_ACCOUNT_CREATED,
                RSP_KEY.REFRESH_TOKEN_KEY: str(token),
                RSP_KEY.ACCESS_TOKEN_KEY: str(token.access_token),
                RSP_KEY.DATA_KEY: serializer.data,
            }
            return Response(creds, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignInView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        if not email or not password:
            return Response(
                {RSP_KEY.ERROR_KEY: _(RSP_MSG.ERROR_EMAIL_AND_PASS_REQUIRED_MESSAGE)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.is_active:
                serializer = AccountSerializer(user)
                token = RefreshToken.for_user(user)
                creds = {
                    RSP_KEY.MESSAGE_KEY: RSP_MSG.ACCOUNT_SIGNIN_SUCCESS,
                    RSP_KEY.REFRESH_TOKEN_KEY: str(token),
                    RSP_KEY.ACCESS_TOKEN_KEY: str(token.access_token),
                    RSP_KEY.DATA_KEY: serializer.data,
                }
                return Response(creds, status=status.HTTP_200_OK)
            return Response(
                {RSP_KEY.ERROR_KEY: _(RSP_MSG.USER_ACCOUNT_DISABLED_MESSAGE)},
                status=status.HTTP_403_FORBIDDEN,
            )
        return Response(
            {RSP_KEY.ERROR_KEY: _(RSP_MSG.INVALID_EMAIL_AND_PASS_MESSAGE)},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    

class JWTTokenRefreshView(TokenRefreshView):

    def post(self, request, *args, **kwargs):
        ...


class JWTTokenVerifyView(TokenVerifyView):

    def post(self, request, *args, **kwargs):
        ...