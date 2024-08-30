from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
import jwt
from .token import TokenService

Account = get_user_model()

"""
 TODO: this class should be implemented in a way such that
 my other services can implement it and change its payload and authentication
 key for time domain.

 e.g Suppose user have to create a api for fetching user data 
 and need it has to authenticate with the JWT with their own claims.
 so faciliate the user to create custom authentication flow.
"""


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        token = request.COOKIES.get("access_token")
        if not token:
            return None

        try:
            access_token = TokenService.verify_access(token)
            account = Account.objects.filter(id=access_token.user_id).first()
            if account is None:
                raise exceptions.AuthenticationFailed("Account not found")
            request.token = access_token
            return (account, token)
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token expired!")
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed("Token signature is invalid.")
        except Exception as e:
            raise exceptions.AuthenticationFailed(str(e))
