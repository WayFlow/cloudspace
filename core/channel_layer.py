from channels_redis.core import RedisChannelLayer

class CustomChannelLayer(RedisChannelLayer):
    
    async def group_exists(self, group):
        print(group)
        group_key = self._group_key(group)
        async with self.connection(self.consistent_hash(group_key)) as conn:
            return await conn.exists(group_key) > 0