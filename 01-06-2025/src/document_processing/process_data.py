from src.data_ingestion.pdf_loader import ProcessPDF
import base64
from PIL import Image
from io import BytesIO
from langchain.text_splitter import RecursiveCharacterTextSplitter
import uuid
from src.embeddings.embedder import Embeddings

class DataProcessor(ProcessPDF,Embeddings):
    def __init__(self):
        super().__init__()

        

    def base64_to_pil_image(self,base64_str):
        image_data = base64.b64decode(base64_str)
        return Image.open(BytesIO(image_data)).convert("RGB")
    
    def handle_image_data(self):
        image_elements = self.get_elements_based_on_category("Image")
        meta_data =[]
        embeddings= []
        document = []
        for el in image_elements:
            data = el.metadata.to_dict()

            for i in ['detection_class_prob', 'coordinates', 'last_modified', 'filetype', 'languages',  'file_directory']:
                if i in data:
                    del data[i]
            data['type'] = "image"
            document.append( el.text if len(el.text)>0 else "image")
            meta_data.append(data)
            embeddings.append(self.embed_image(data['image_base64']))
        ids_to_add = [str(uuid.uuid4()) for _ in range(len(meta_data))]
        return embeddings,meta_data,document,ids_to_add
    
    def handle_table_data(self):
        table_elements = self.get_elements_based_on_category("Table")
        text =[]
        meta_data =[]
        
        for el in table_elements:
            data = el.metadata.to_dict()
            for i in ['detection_class_prob', 'coordinates', 'last_modified', 'filetype', 'languages', 'file_directory']:
                if i in data:
                    del data[i]
            data['type'] ="table"
            text.append(el.text)
            meta_data.append(data)
        ids_to_add = [str(uuid.uuid4()) for _ in range(len(meta_data))]
        embeddings = self.embeddings.embed_documents(text)
        return embeddings,meta_data,text,ids_to_add
    

    def handle_text_data(self):
        text =[]
        meta_data =[]
        embeddings= []
        for element_type in self.data_types:
            if element_type != "Image" and element_type!= "Table":
               elements = self.get_elements_based_on_category(element_type)
               for el in elements:
                    data = el.metadata.to_dict()
                    for chunk_text in self.conditional_chunk(el.text):
                        text.append(chunk_text)
                        for i  in ['detection_class_prob', 'coordinates', 'last_modified', 'filetype', 'languages', 'file_directory']:
                            if i in data:
                                del data[i]
                        data['type'] ="text"
                        data['category'] =el.category
                        
                        meta_data.append(data)
        ids_to_add = [str(uuid.uuid4()) for _ in range(len(text))]
        embeddings = self.embeddings.embed_documents(text)
               
        return embeddings,meta_data,text,ids_to_add
    
    def conditional_chunk(self,text, min_length=1000, chunk_size=1000, chunk_overlap=100):

        if len(text) <= min_length:
            return [text]  # No chunking needed
        else:
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                separators=["\n\n", "\n", ".", " ", ""]
            )
            return splitter.split_text(text)
    def cleanup(self):
        super().cleanup()
        for attr in list(self.__dict__.keys()):
            delattr(self, attr)
if __name__ == "__main__":
    loaded_pdf = DataProcessor(pdf_path="../data/chapter12.pdf")
    loaded_pdf.get_data_from_pdf()
    loaded_pdf.segergate_data()
    loaded_pdf.get_cout_for_each_data_category()
            




