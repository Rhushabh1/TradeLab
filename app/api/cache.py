from fastapi import APIRouter

from app.cache.cache_service import cache 


router = APIRouter(prefix = "/cache",
					tags = ["Cache"])


@router.get("/health")
def health():
	# add to cache
	cache.set("ping",
				{
					"status": "ok"
				},
				ttl = 10)
	# fetch from cache
	return cache.get("ping")

@router.post("/{key}")
def save(key: str):
	cache.set(key,
				{
					"cached": True
				})
	return {
			"message": "stored"
			}

@router.get("/{key}")
def load(key: str):
	value = cache.get(key)
	if value is None:
		return {
				"cache": "MISS"
				}
	return {
			"cache": "HIT",
			"value": value
			}