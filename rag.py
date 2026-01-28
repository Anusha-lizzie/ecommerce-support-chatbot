import os
from sentence_transformers import SentenceTransformer
import faiss

model = SentenceTransformer("all-MiniLM-L6-v2")

documents = []
doc_names = []

DATA_DIR = "data"

for file in os.listdir(DATA_DIR):
    with open(os.path.join(DATA_DIR, file), "r", encoding="utf-8") as f:
        text = f.read()
        documents.append(text)
        doc_names.append(file)

embeddings = model.encode(documents)

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

def retrieve_context(query, top_k=2):
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, top_k)

    context = ""
    for idx in indices[0]:
        context += documents[idx] + "\n\n"

    return context
