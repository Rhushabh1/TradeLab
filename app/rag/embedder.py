from functools import lru_cache
from sentence_transformers import SentenceTransformer 

from app.config import settings


# lazy loader
# add lazy load by calling get_model()
@lru_cache(maxsize = 1)
def get_model():
	return SentenceTransformer(settings.MODEL_NAME)

# normalized these embeddings
def embed(text: str):
	return get_model().encode(text, normalize_embeddings = True)

def embed_many(texts: list[str]):
	return get_model().encode(texts, normalize_embeddings = True)