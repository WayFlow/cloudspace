import json
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import update_last_login


from utils.constants import ResponseDataKey as RSP_KEY
from tokens.token import TokenService, AccessToken
from utils.constants import ResponseMessage as RSP_MSG
from utils.time import get_timestamp

from .serializers import AccountSerializer, AccountDataSerializer

Account = get_user_model()


def cred_builder(access_token: AccessToken):
    # TODO: encrypt the access token
    data = {
        "access_token": access_token.token,
        "at_expires": get_timestamp(access_token.exp),
        "user_id": access_token.user_id,
    }
    return json.dumps(data)


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        data["username"] = data["email"]
        account = Account.objects.filter(email=data["email"]).first()
        if account:
            return Response(
                {RSP_KEY.ERROR_KEY: "Email already registered"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            update_last_login(None, account)
            ts = TokenService(account)
            access = ts.create_access_token()
            response = Response(
                {
                    RSP_KEY.MESSAGE_KEY: RSP_MSG.SUCCESSFULL_ACCOUNT_CREATED,
                    RSP_KEY.USER_ID: account.id,
                    RSP_KEY.ACCESS_TOKEN_EXPIRES: get_timestamp(access.exp),
                },
                status=status.HTTP_201_CREATED,
            )
            response.set_cookie(
                key="cred",
                value=cred_builder(access),
                httponly=True,
                secure=False,  # TODO: Ensure this is True in production
                samesite="lax",
                max_age=24 * 60 * 60,
            )

            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

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
                update_last_login(None, user)
                ts = TokenService(user)
                access = ts.create_access_token()
                response = Response(
                    {
                        RSP_KEY.MESSAGE_KEY: RSP_MSG.ACCOUNT_SIGNIN_SUCCESS,
                        RSP_KEY.USER_ID: user.id,
                        RSP_KEY.ACCESS_TOKEN_EXPIRES: get_timestamp(access.exp),
                    },
                    status=status.HTTP_200_OK,
                )
                response.set_cookie(
                    key="cred",
                    value=cred_builder(access),
                    httponly=True,
                    secure=False,  # TODO: Ensure this is True in production
                    samesite="lax",
                    max_age=24 * 60 * 60,
                )

                return response
            return Response(
                {RSP_KEY.ERROR_KEY: _(RSP_MSG.USER_ACCOUNT_DISABLED_MESSAGE)},
                status=status.HTTP_403_FORBIDDEN,
            )
        return Response(
            {RSP_KEY.ERROR_KEY: _(RSP_MSG.INVALID_EMAIL_AND_PASS_MESSAGE)},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class LogoutView(APIView):

    def post(self, request: Request, *args, **kwargs):
        token: AccessToken | None = request.token
        if not token:
            return Response(
                {"detail": "No token provided"}, status=status.HTTP_401_UNAUTHORIZED
            )
        response = Response(
            {RSP_KEY.MESSAGE_KEY: "Logged out successfully."}, status=status.HTTP_200_OK
        )
        token.remove_access_token()
        response.delete_cookie("cred")
        return response


class AccountView(APIView):

    def get(self, request: Request, *args, **kwargs):
        serializer = AccountDataSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
