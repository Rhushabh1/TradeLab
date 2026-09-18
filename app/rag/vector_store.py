import faiss
import numpy as np 

from app.rag.embedder import embed


index = faiss.IndexFlatL2(384)

documents = []


def add_document(text):
	vector = embed(text)
	index.add(np.array([vector]).astype("float32"))
	documents.append(text)


def search(question, k = 5):
	query = embed(question)
	_, ids = index.search(np.array([query]).astype("float32"), k)
	return [documents[i] for i in ids[0] if i!=-1]