import redis

from app.config import settings


# main redis client (handling cache hit/miss/update/delete)
client = redis.Redist.from_url(settings.REDIS_URL,
								decode_responses = True)