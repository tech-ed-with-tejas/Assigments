
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableMap,RunnableLambda
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()

os.environ['GOOGLE_API_KEY'] = os.getenv("GOOGLE_API_KEY")

model=ChatGoogleGenerativeAI(model='gemini-1.5-flash')
from src.retriver.retrive_fromdb import ProcessQuery

query = ProcessQuery(collectionimages="DietImages",collectiontext="DietTextdata",dir="diet_pdf_database")
model=ChatGoogleGenerativeAI(model='gemini-1.5-flash')
def load_data(question):
    result = query.get_similar_data(question)  # or use it however needed
    return {
        "context": result["text"],
        "table": result.get("table", []),
        "images": result.get("images", []),
        "question": question  # preserve it for prompt
    }
template =""""You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question.take help of the context dont completly depend on that. If you don't know the answer, just say that you don't know.Eplain about 2 paragraph.\nQuestion: {question} \nContext: {context} \nAnswer:"
"""

prompt = PromptTemplate(
    template=template,
    input_variables=["question","context"])

# Step 1: Load data from question
load_chain = RunnableLambda(lambda x: load_data(x["question"]))

# Step 2: Map context, table, images, and question for next stage
map_chain = RunnableLambda(lambda x: {
    "context": x["context"],
    "table": x["table"],
    "images": x["images"],
    "question": x.get("question")
})

# Step 3: Prepare the final chain
llm_chain = RunnableLambda(lambda x: prompt.invoke({
    "context": x["context"],
    "question": x["question"]
})) | model | StrOutputParser()

# Combine all into one chain
chain = load_chain | map_chain | RunnableMap({
    "llm_answer": llm_chain,
    "table": lambda x: x["table"],
    "images": lambda x: x["images"]
})



# === Main function to call in loop ===
def generate_text_and_images(query):
    # try:
    result = chain.invoke({"question" :query})
    return result  # {'text_answer': ..., 'images': [...]}
    # except Exception as e:
    #     print(f"[Query Error] {e}")
    #     return {"text_answer": "Error generating response.", "images": []}