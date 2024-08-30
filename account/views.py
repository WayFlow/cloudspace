import json
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


from utils.constants import ResponseDataKey as RSP_KEY
from tokens.token import TokenService, AccessToken
from utils.constants import ResponseMessage as RSP_MSG
from utils.time import get_timestamp

from .serializers import AccountSerializer

Account = get_user_model()

def cred_builder(access_token : AccessToken):
    data = {
        'access_token': access_token.token,
        'exp': get_timestamp(access_token.exp),
        'user_id': access_token.user_id
    }
    return json.dumps(data)


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            ts = TokenService(account)
            access = ts.create_access_token()
            response = Response({
                RSP_KEY.MESSAGE_KEY: RSP_MSG.SUCCESSFULL_ACCOUNT_CREATED,
                RSP_KEY.USER_ID: account.id,
                RSP_KEY.ACCESS_TOKEN_EXPIRES: get_timestamp(access.exp),
            }, status=status.HTTP_201_CREATED)
            response.set_cookie(
                key='cred',
                value=cred_builder(access),
                httponly=True,
                secure=False,  # TODO: Ensure this is True in production
                samesite='Strict',
                max_age=24 * 60 * 60
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
                ts = TokenService(user)
                access = ts.create_access_token()
                response = Response({
                    RSP_KEY.MESSAGE_KEY: RSP_MSG.ACCOUNT_SIGNIN_SUCCESS,
                    RSP_KEY.USER_ID: user.id,
                    RSP_KEY.ACCESS_TOKEN_EXPIRES: get_timestamp(access.exp),
                }, status=status.HTTP_200_OK)
                response.set_cookie(
                    key='cred',
                    value=cred_builder(access),
                    httponly=True,
                    secure=False,  #TODO: Ensure this is True in production
                    samesite='Strict',
                    max_age=24 * 60 * 60
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

    def post(self, request : Request, *args, **kwargs):
        token : AccessToken = request.token
        if not token:
            return Response({"detail": "No token provided"}, status=status.HTTP_401_UNAUTHORIZED)
        response = Response({
            RSP_KEY.MESSAGE_KEY: "Logged out successfully."
        }, status=status.HTTP_200_OK)
        token.remove_access_token()
        response.delete_cookie('cred')
        return response