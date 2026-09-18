import json

from app.cache.redis_client import client 


# abstracting the main redis client via service layer
# better than using decorators (easier to explain too -> get/set)

# caching is part of business logic -> hence business layer
# whereas routes only orchestrate HTTP requests
class CacheService:
	def get(self, key: str):
		value = client.get(key)
		# cache miss
		if value is None:
			return None
		# cache hit
		return json.loads(value)

	# TTL = time to live (for automatic cache invalidation)
	# stock prices -> short TTL (5-10 mins)
	# AI summaries/company profiles -> long TTL
	def set(self, key: str, value, ttl: int = 300):
		client.setex(key, ttl, json.dumps(value))

	def delete(self, key: str):
		return client.delete(key)

	# removes matching cache entries that have no expiration
	def cleanup_keys_without_ttl(self, pattern: str = "stock:*") -> int:
		deleted = 0
		for key in client.scan_iter(match = pattern, count = 500):
			if client.ttl(key) == -1:
				deleted += client.delete(key)
		return deleted


cache = CacheService()