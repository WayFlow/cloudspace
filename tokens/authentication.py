from django.contrib.auth import get_user_model
from urllib.parse import parse_qs
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
import jwt
from .token import TokenService
import json
import re

from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from jwt import ExpiredSignatureError, DecodeError

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
    """
    Create one more authentication header to be verify genuien requet
    """

    def authenticate(self, request):
        data = request.COOKIES.get("cred")
        if not data:
            return None
        data = json.loads(data)
        try:
            token = data["access_token"]
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



class WebSocketJWTAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        try:
            query_params = parse_qs(scope.get('query_string', b'').decode())
            token = query_params.get('token', [None])[0]
            envId = query_params.get('envId', [None])[0]
            projectId = query_params.get('projectId', [None])[0]
            scope['envId'] = envId
            scope['projectId'] = projectId
            if token:
                try:
                    access_token = TokenService.verify_access(token)
                    user = await get_account(access_token.user_id)
                    scope['user'] = user if user else AnonymousUser()
                except (ExpiredSignatureError, DecodeError):
                    scope['user'] = AnonymousUser()
                except Exception as e:
                    print(f"Unexpected error during token verification: {e}")
                    scope['user'] = AnonymousUser()
            else:
                scope['user'] = AnonymousUser()

        except Exception as e:
            print(f"Error in WebSocketJWTAuthMiddleware: {e}")
            scope['user'] = AnonymousUser()
        return await super().__call__(scope, receive, send)


@database_sync_to_async
def get_account(user_id):
    try:
        return Account.objects.get(id=user_id)
    except Account.DoesNotExist:
        return None