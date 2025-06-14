
import os
from dotenv import load_dotenv, find_dotenv
import sys
from collections import defaultdict
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
dotenv_path = find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path)
else:
    print("Warning: .env file not found. Ensure it's in the project root.")
from langchain_huggingface import HuggingFaceEmbeddings #type :ignore
os.environ['HF_TOKEN']=os.getenv("HF_TOKEN")
import base64
from io import BytesIO
from PIL import Image

from transformers import CLIPProcessor, CLIPModel



class Embeddings():
    def __init__(self):
        pass
    def text_embeddings(self):
        self.embeddings =HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    
    def image_embeddings_load_model(self):
        model_name = "openai/clip-vit-large-patch14"
        self.processor = CLIPProcessor.from_pretrained(model_name)
        self.model = CLIPModel.from_pretrained(model_name)
    def base64_to_pil_image(self,base64_str):
        image_data = base64.b64decode(base64_str)
        return Image.open(BytesIO(image_data)).convert("RGB")
    def embed_image(self,base64_image_str):
        image = self.base64_to_pil_image(base64_image_str)
        inputs = self.processor(images=image, return_tensors="pt")
        image_features = self.model.get_image_features(**inputs)
        return image_features.squeeze().tolist()
    def embed_text(self,text):
        inputs = self.processor(text=[text], return_tensors="pt", padding=True, truncation=True)
        features = self.model.get_text_features(**inputs)
        return features.squeeze().tolist()





