import json
import chromadb
from chromadb.config import Settings
import glob
import os
import uuid

# Generate a list of 100 unique UUIDs


# --- CONFIGURATION ---
DB_PATH = "./chroma_db"
COLLECTION_NAME = "resumeknowldgebase"

# --- INITIALIZE CHROMADB ---
client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)

# --- LOAD JSON DATA FROM ALL FILES IN embeddings FOLDER ---
chunks = []



with open("./RAG/embeddings/all_nomic_embed_v1.json", "r", encoding="utf-8") as f:
    file_chunks = json.load(f)  # expects a list of chunks
    chunks.extend(file_chunks)

# --- UPSERT CHUNKS INTO CHROMADB ---
# ids = []
documents = []
embeddings = []
metadatas = []
ids = [str(uuid.uuid4()) for _ in range(len(chunks))]
for chunk in chunks:
    # ids.append(f"chunk_{chunk['chunk_index']}")
    if len(chunk["embedding"]) <1:
        print(chunk)
        continue
        
    documents.append(chunk["text"])
    embeddings.append(chunk["embedding"])  # use precomputed embeddings
    metadatas.append({
        "chunk_index": chunk["chunk_index"],
        "len": chunk.get("len", len(chunk["text"]))
    })
collection.upsert(
    documents=documents,
    embeddings=embeddings,
    ids=ids,
    metadatas=metadatas
)

print(f"Inserted {len(chunks)} chunks into ChromaDB!")
