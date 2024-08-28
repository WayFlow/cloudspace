import hashlib
import time
import uuid
import jwt

from django.utils import timezone
from cloudspace.settings import SECRET_KEY

from .redis_auth import RedisAuthService

from datetime import timedelta

from account.models import Account


class Token:
    token_type = None

    def __init__(self, user_id, iat, exp, jti, type=None):
        self.user_id = user_id
        self.iat = iat
        self.exp = exp
        self.type = type or self.token_type
        self.jti = jti

    @property
    def token(self):
        payload = self.__dict__
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return token

    @classmethod
    def verify(cls, token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithm="HS256")
            return cls(**payload)
        except Exception as e:
            raise e


class RefreshToken(Token):
    token_type = "refresh"


class AccessToken(Token):
    token_type = "access"


class TokenService:

    def __init__(self, user: Account):
        """
        creates a new token service with same JTI
        """
        self.user = user
        self.jti = self._generate_jti_id()

    @classmethod
    def _get_utc_time(self):
        return timezone.now()

    @classmethod
    def _generate_jti_id(self):
        app_id = str(uuid.uuid4())
        current_time = str(int(time.time()))
        combined_string = app_id + current_time
        jti_id = hashlib.md5(combined_string.encode()).hexdigest()
        return jti_id

    def create_refresh_token(self, lifetime=timedelta(days=30)) -> RefreshToken:
        iat = self._get_utc_time()
        data = {
            "user_id": str(self.user.id),
            "iat": iat,
            "exp": iat + lifetime,
            "jti": self.jti,
        }
        token = RefreshToken(**data)
        redis_auth = RedisAuthService(token)
        redis_auth.create_auth()
        return token

    def create_access_token(self, lifetime=timedelta(minutes=5)) -> AccessToken:
        iat = self._get_utc_time()
        data = {
            "user_id": str(self.user.id),
            "iat": iat,
            "exp": iat + lifetime,
            "jti": self.jti,
        }
        token = AccessToken(**data)
        return token

    @classmethod
    def verify_refresh(self, token) -> RefreshToken:
        try:
            refresh: RefreshToken = RefreshToken.verify(token)
            if refresh.type != RefreshToken.token_type:
                raise Exception("Token type is not valid")
            redis_auth = RedisAuthService(refresh)
            auth = redis_auth.fetch_auth()
            if not auth:
                raise Exception("Token Expired")
            if auth != refresh.user_id:
                raise Exception("user not matching.")
            return refresh
        except Exception as e:
            raise e

    @classmethod
    def verify_access(self, token) -> AccessToken:
        try:
            access: AccessToken = AccessToken.verify(token)
            if access.type != AccessToken.token_type:
                raise Exception("Token type is not valid")
            redis_auth = RedisAuthService(access)
            auth = redis_auth.fetch_auth()
            if not auth:
                raise Exception("Token Expired")
            if auth != access.user_id:
                raise Exception("user not matching.")
            return access
        except Exception as e:
            raise e
