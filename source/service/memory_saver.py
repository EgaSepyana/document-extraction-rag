from db.redis_cache import RedisService
import orjson

# from api.config.base import settings


class Memory:
    def __init__(self):
        self.redis = RedisService()
        self.MAX_MEMORY = 10

    def save_message(self, chatId: str, role: str, content: str):
        key = f"chat:{chatId}:history"
        msg = orjson.dumps({"role": role, "content": content}).decode()
        self.redis.rpush(key, msg)
        self.redis.ltrim(key, -self.MAX_MEMORY, -1)

    def load_memory(self, chatId: str):
        key = f"chat:{chatId}:history"
        raw = self.redis.lrange(key, 0, -1)
        if not raw:
            return []
        return [orjson.loads(x) for x in raw]
