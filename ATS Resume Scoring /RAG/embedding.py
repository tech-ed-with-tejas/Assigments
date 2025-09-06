import json
import glob
import os
from pathlib import Path
from sentence_transformers import SentenceTransformer
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load your embedding model
model_name = "all-MiniLM-L6-v2"
model = SentenceTransformer(model_name, trust_remote_code=True)

def read_full_text(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    cleaned_lines = [
        line for line in content.splitlines()
        if not line.strip().startswith("=== Page")
    ]
    return "\n".join(cleaned_lines).strip()

def chunk_text_by_chars(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""],
    )
    chunks = splitter.split_text(text)
    return [chunk.strip() for chunk in chunks if chunk.strip()]

def generate_embeddings(chunks: List[str]):
    vecs = model.encode(chunks, normalize_embeddings=True)
    return vecs

if __name__ == "__main__":
    input_folder = "./RAG/clead_data/"
    output_file = "./embeddings/all_nomic_embed_v1.json"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    all_data = []
    chunk_id = 0

    for input_txt in glob.glob(input_folder + "*.txt"):
        print(f"Processing: {input_txt}")
        full_text = read_full_text(input_txt)
        chunks = chunk_text_by_chars(full_text, chunk_size=1000, overlap=200)
        embeddings = generate_embeddings(chunks)
        for idx, (chunk, vec) in enumerate(zip(chunks, embeddings)):
            all_data.append({
                "chunk_index": chunk_id,
                "file": os.path.basename(input_txt),
                "len": len(chunk),
                "text": chunk,
                "embedding": vec.tolist()
            })
            chunk_id += 1

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    print(f"All embeddings saved to: {output_file}")
