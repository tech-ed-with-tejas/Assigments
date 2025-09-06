# utils.py
import os
import chromadb
from sentence_transformers import SentenceTransformer

import os

# Load your embedding model
model_name = "nomic-ai/nomic-embed-text-v1"
model = SentenceTransformer(model_name, trust_remote_code=True)

app_env = os.getenv("APP_ENV","local")
os.environ["TOKENIZERS_PARALLELISM"] = "false"
if app_env == "local":
    # CHROMA_PATH = r"C:\Users\Asus02\Desktop\git cloned\saiwell-vectorbase\chromadb"
    CHROMA_PATH = "./chroma_db"
else:
    CHROMA_PATH = "/mnt/data/chromadb"  # Persistent path for Cloud Run

print(CHROMA_PATH)
# Initialize ChromaDB client
client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_collection(name="resumeknowldgebase")


def preproceess(base_results):
    docs = base_results["documents"][0]
    content =''
    for doc in docs:
      
        content  += "\n"+  "Refrence Content: "+ str(doc) +" \n"
    
    return content

def query(query_text:str,k:int=3):
    embedding = model.encode(query_text).tolist()
    base_results = collection.query(query_embeddings=[embedding], n_results=k)
    Content = preproceess(base_results)
    for meta in base_results["metadatas"][0]:
        chunk_id = meta.get("chunk_index")
        print("---------------------------------------------------------",chunk_id)
 
        query_result_greater = collection.query(
                query_embeddings=[embedding],       # You can leave empty if not querying by vectors
                n_results=2,         # Number of results to return
                where={"chunk_index": str(int(chunk_id)+1)}  # Metadata filter: match documents with name 'John Doe'
            )
        query_result_lesser = collection.query(
                query_embeddings=[embedding],      # You can leave empty if not querying by vectors
                n_results=2,         # Number of results to return
                 where={"chunk_index": str(int(chunk_id)-1)} # Metadata filter: match documents with name 'John Doe'
            )
        
        Content += preproceess(query_result_greater) +" \n"
        Content += preproceess(query_result_lesser) +" \n"
            # seen_chunks.add(chunk_id)
        print("3---------------------------------------------------------",chunk_id)

    return Content






if __name__ == "__main__":
    print(query(query_text="Best resume practice for better ats score"))

