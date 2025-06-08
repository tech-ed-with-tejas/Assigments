from src.vector_store_manager.database_initialize import LocalChromaDBManager
from src.embeddings.embedder import Embeddings





class ProcessQuery(Embeddings):
    def __init__(self,collectiontext:str,collectionimages:str,dir:str):
        super().__init__()
        self.text_embeddings()
        self.image_embeddings_load_model()
        self.data_base_image = LocalChromaDBManager(collection_name=collectionimages,persist_directory=dir)
        self.data_base_text= LocalChromaDBManager(collection_name=collectiontext,persist_directory=dir)
        self.data_base_image.initilize_collection()
        self.data_base_text.initilize_collection()

    def get_text_and_table_search(self,query:str):

        text_embed = self.embeddings.embed_query(query)
        return self.data_base_text.query_store_by_embedding(query=text_embed)

    def get_images_that_match_query(self,query):
        img_embeeed = self.embed_text(query)
        return self.data_base_image.query_store_by_embedding(query=img_embeeed,num_results=2)
    def get_images_from_db(self,image):
        base64_strs = []
        for i in range(len(image['ids'][0])):
            meta_data = image['metadatas'][0][i]
            base64_strs.append(meta_data['image_base64'])
        return base64_strs
    def get_text_table_from_db(self,text):
        text_data,table = [],[]
        for i in range(len(text['ids'][0])):
            text_from_pdf = text['documents'][0][i]
            meta_data = text['metadatas'][0][i]
            if meta_data['type'] =="table":
                table.append(meta_data['table'])
            text_data.append(text_from_pdf)
        return "\n\n".join(text_data),table
    def get_similar_data(self,query):
        text_search =self.get_text_and_table_search(query)
        image_search =self.get_images_that_match_query(query)
        text ,table = self.get_text_table_from_db(text_search)
        images = self.get_images_from_db(image_search)
        return {"text":text,"table":table,"images":images}
        # return text_search,image_search



