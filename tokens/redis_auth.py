from django.core.cache import cache
from utils.time import get_timestamp


class RedisAuthService:

    def __init__(self, token):
        self.token = token

    def create_auth(self):
        cache.set(self.token.jti, self.token.user_id, get_timestamp(self.token.exp))

    def delete_auth(self):
        cache.delete(self.token.jti)

    def fetch_auth(self):
        return cache.get(self.token.jti)
