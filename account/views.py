from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


from utils.constants import ResponseDataKey as RSP_KEY
from tokens.token import TokenService
from utils.constants import ResponseMessage as RSP_MSG
from utils.time import get_timestamp

from .serializers import AccountSerializer

Account = get_user_model()


class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            refresh = TokenService.refresh(account)
            access = TokenService.access(account)
            creds = {
                RSP_KEY.MESSAGE_KEY: RSP_MSG.SUCCESSFULL_ACCOUNT_CREATED,
                RSP_KEY.REFRESH_TOKEN_KEY: refresh.token,
                RSP_KEY.ACCESS_TOKEN_KEY: access.token,
                RSP_KEY.ACCESS_TOKEN_EXPIRES: get_timestamp(access.exp),
                RSP_KEY.REFRESH_TOKEN_EXPIRES: get_timestamp(refresh.exp),
                RSP_KEY.USER_ID: account.id
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
                refresh = TokenService.refresh(user)
                access = TokenService.access(user)
                creds = {
                    RSP_KEY.MESSAGE_KEY: RSP_MSG.ACCOUNT_SIGNIN_SUCCESS,
                    RSP_KEY.REFRESH_TOKEN_KEY: refresh.token,
                    RSP_KEY.ACCESS_TOKEN_KEY: access.token,
                    RSP_KEY.ACCESS_TOKEN_EXPIRES: get_timestamp(access.exp),
                    RSP_KEY.REFRESH_TOKEN_EXPIRES: get_timestamp(refresh.exp),
                    RSP_KEY.USER_ID: user.id,
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
