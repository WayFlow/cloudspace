from django.core import cache


class RedisAuthService:

    def __init__(self, token):
        self.token = token

    def create_auth(self):
        cache.set(self.token.jti, self.token.user_id, self.token.exp)

    def delete_auth(self): ...

    def fetch_auth(self):
        return cache.get(self.token.jti)

    def has_auth(self):
        return self.fetch_auth != None
