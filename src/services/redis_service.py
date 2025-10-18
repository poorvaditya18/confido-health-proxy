import redis
import logging
from configs.config import Config
logger = logging.getLogger("redis_service")

class RedisService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        try:
            self.client = redis.Redis(
                host=Config.REDIS_HOST,
                port=int(Config.REDIS_PORT),
                password=Config.REDIS_PASSWORD,
                decode_responses=True
            )
            self.client.ping()
            logger.info("successfully connected to Redis")
        except Exception as e:
            logger.exception("failed to connect to Redis. err: %s", e)
            raise e 

    def get(self, key: str):
        try:
            return self.client.get(key)
        except Exception as e:
            logger.exception("failed to get redis-key: %s, err: %s", key, e)
            return None

    def set(self, key: str, value: str, ttl: int = None):
        try:
            if ttl:
                self.client.setex(name=key, time=ttl, value=value)
            else:
                self.client.set(name=key, value=value)
            return True
        except Exception as e:
            logger.exception("Failed to set Redis key '%s': %s", key, e)
            return False

    def delete(self, key: str):
        try:
            self.client.delete(key)
        except Exception as e:
            logger.exception("failed to delete redis-key: %s, err: %s", key, e)

    def ttl(self, key: str):
        try:
            ttl_value = self.client.ttl(key)
            return None if ttl_value is None or ttl_value < 0 else ttl_value
        except Exception as e:
            logger.exception("failed to get ttl value of redis-key '%s': %s", key, e)
            return None

    def exists(self, key: str):
        try:
            return self.client.exists(key) == 1
        except Exception as e:
            logger.exception("failed to check existence of redis-key '%s': %s", key, e)
            return False