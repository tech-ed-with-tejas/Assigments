import tempfile


from autogen_ext.memory.chromadb import (
    ChromaDBVectorMemory,
    PersistentChromaDBVectorMemoryConfig,
    SentenceTransformerEmbeddingFunctionConfig,
)
from chromadb.utils import embedding_functions

from sentence_transformers import SentenceTransformer
from chromadb.utils.embedding_functions import EmbeddingFunction
from typing import Any, Dict, List
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"


chroma_user_memory = ChromaDBVectorMemory(
    config=PersistentChromaDBVectorMemoryConfig(
        collection_name="resumeknowldgebase",
        persistence_path="./chroma_db",  
        k=5,  # Return top k results
      )
#          embedding_function_config={
#     "function_type": "sentence_transformer",
#     "model_name": "./models/nomic-embed-text-v1"  # Path to your downloaded model
# },
      
)
def get_chroma_db_for_agents():
    return chroma_user_memory