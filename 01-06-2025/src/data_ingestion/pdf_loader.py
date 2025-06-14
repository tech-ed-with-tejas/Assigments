
import os
from dotenv import load_dotenv, find_dotenv
import sys
from collections import defaultdict
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
dotenv_path = find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path)
    # print(f"Environment variables loaded from: {dotenv_path}")
else:
    print("Warning: .env file not found. Ensure it's in the project root.")

from unstructured.partition.pdf import partition_pdf
os.environ["OCR_AGENT"] = "unstructured.partition.utils.ocr_models.tesseract_ocr.OCRAgentTesseract"
class ProcessPDF:
    def __init__(self,image_dir:str=None,strategy:str="hi_res",images:str=True,block_types:list[str]=["Image"],extract_image_as_payload:bool=True):
        print("initialized")
        self.strategy = strategy
        self.images = images
        self.block_types= block_types
        if image_dir :
            self.image_dir = image_dir
        
        self.image_as_payload = extract_image_as_payload

    def inialize_pdf_path(self,pdf_path:str):
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"The required file was not found: '{pdf_path}'")
        else:
            self.pdf_path = pdf_path
        # self.get_data_from_pdf()
        # self.segergate_data()
        # self.get_cout_for_each_data_category()
        
    def get_data_from_pdf(self):
        if self.image_as_payload:
            self.elements = partition_pdf(
                        filename=self.pdf_path,                  
                        strategy= self.strategy, 
                        infer_table_structure=True,   
                        languages=["eng"],                 
                                  
                        extract_images_in_pdf=self.images,                           
                    
                        extract_image_block_to_payload=True
                )
        else:
            if  not os.path.exists(self.image_dir):
                os.mkdir(self.image_dir)
            self.elements = partition_pdf(
                        filename=self.pdf_path,                  
                        strategy= self.strategy, 
                        languages=["eng"],                                  
                        extract_images_in_pdf=self.images,                           
                        extract_image_block_output_dir=self.image_dir, 
                       
                )
            
    def segergate_data(self):
        self.data_types = defaultdict(list)
        for id,el in enumerate(self.elements):
            category = el.category
            self.data_types[category].append(id)
        
    def get_cout_for_each_data_category(self):
        for i in self.data_types:
            print("Total elemnt found for data caterogry", i, " is ",len(self.data_types[i]))

    def get_element_based_onindex(self,index:int=0):
        return self.elements[index]
    def get_elements_based_on_category(self,category:str)->list:
        return list(map(lambda index: self.elements[index], self.data_types[category]))
    
    def get_images(self,indexs:list[int])->list[str]:
        images =[]
        for idx in indexs:
            meta_data = self.elements[idx].metadata.to_dict()
            if "image_base64" in meta_data:
                images.append(meta_data['image_base64'])
        return images
    def get_table(self,indexs:int)->list[str]:
        tables =[]
        for idx in indexs:
            meta_data = self.elements[idx].metadata.to_dict()
            if "text_as_html" in meta_data:
                tables.append(meta_data['text_as_html'])
        return tables
    
    def get_text(self,indexs:int)->list[str]:
        text =[]
        for idx in indexs:
            text.append(self.elements[idx].text)
        return text
    
    def cleanup(self):
        for attr in list(self.__dict__.keys()):
            delattr(self, attr)

if __name__ == "__main__":
    print(os.getcwd())
    loaded_pdf = ProcessPDF(pdf_path="../data/chapter12.pdf")
    loaded_pdf.get_data_from_pdf()
    loaded_pdf.segergate_data()
    loaded_pdf.get_cout_for_each_data_category()
