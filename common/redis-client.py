import redis
import pickle

class RedisClient():
    def __init__(self, redis_host,
                        redis_port = 6379):
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_client = None

    def connectToRedis(self):
        # Todo: Add retry logic
        try:
            self.redis_client = redis.StrictRedis(host=self.redis_host, port=self.redis_port)
        except Exception as e:
            print("Error in connecting the redis " + str(e))

    def setJson(self, key, value, **kwargs):
        """Store a json value in Redis."""
        return self.redis_client.set(key, pickle.dumps(value), **kwargs)

    def getJson(self, key):
        """Retrieve a json value from Redis."""
        val = self.redis_client.get(key)
        if val:
            return pickle.loads(val)
        return None

    def set(self, key, value, **kwargs):
        """Store a value in Redis."""
        return self.redis_client.set(key, value, **kwargs)

    def get(self, key):
        """Retrieve a value from Redis."""
        val = self.redis_client.get(key)
        if val:
            return val
        return None
