from api.config.base import settings
import redis
from redis.asyncio import Redis as AsyncRedis


class RedisService:

    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = redis.Redis(
                host=settings.REDIS_HOST,
                port=int(settings.REDIS_PORT),
                password=settings.REDIS_PASSWORD,
                decode_responses=True,
                db=int(settings.REDIS_DB),
            )
        return cls.instance
