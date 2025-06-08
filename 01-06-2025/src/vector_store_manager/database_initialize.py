import os
import chromadb


class LocalChromaDBManager:
    def __init__(self, collection_name:str,persist_directory: str = "local_croma_db"):
        self.db_path = persist_directory    
        os.makedirs(self.db_path, exist_ok=True) # Ensure the directory exists
        self.collection_name =collection_name
        self.initilize_client()
  
    def initilize_client(self):
        self.client = chromadb.PersistentClient(path=self.db_path)


    def initilize_collection(self,embedding_function=None):
        if embedding_function is not None:
            self.collection = self.client.get_or_create_collection(
                        name=self.collection_name,embedding_function=embedding_function
                    )
        else:
            self.collection = self.client.get_or_create_collection(
                        name=self.collection_name,
                    )

    def update_vector_store(self,docs:list,meta_data:list,ids:int,embeddings=None):
        if embeddings is not None:

            self.collection.add(
            documents=docs,
            metadatas=meta_data,
            embeddings=embeddings,
            ids =ids
            )
        else:

            self.collection.add(
            documents=docs,
            metadatas=meta_data,
            ids =ids
            )
    def delete_collection(self,collection_name:str):
        self.client.delete_collection(name=collection_name)
        print(f"Collection deleted succesfully name:{collection_name}")

    def list_collections(self):
            return   self.client.list_collections()
    
    def get_elements_ftom_db(self,num_elements:int=10):
        return self.collection.get(
                limit=num_elements,
                include=['documents', 'metadatas', 'embeddings']
            )
    def query_store_by_embedding(self,query:str,num_results:int=5):
        return self.collection.query(
            query_embeddings=query,  
            n_results=num_results,    
            include=['documents', 'metadatas', 'distances'] 
        )
    def query_store_by_text(self,query:str,num_results:int=5):
        return self.collection.query(
            query_text=query,  
            n_results=num_results,    
            include=['documents', 'metadatas', 'distances'] 
        )



    