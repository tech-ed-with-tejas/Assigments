
from langchain_community.tools.tavily_search import TavilySearchResults
import os
from dotenv import load_dotenv
load_dotenv()
from typing import List, Dict, Any, Literal,TypedDict


from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableMap,RunnableLambda
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

os.environ['GOOGLE_API_KEY'] = os.getenv("GOOGLE_API_KEY")

model=ChatGoogleGenerativeAI(model='gemini-1.5-flash')
TAVILY_API_KEY=os.getenv("TAVILY_API_KEY")


tool=TavilySearchResults(tavily_api_key=TAVILY_API_KEY,max_results=3,include_images=False,include_image_descriptions=False,
                         days=30,)


def search_for_web(query):
    """BAsed on input query search the internet and return the response of tope 3 matches"""

    results = tool.invoke({"query":query})
    url = []
    content = ""
    for  i in results:
        # print(i)÷
        # print(i['title'])
        content += i['title'] + "\n"
        url.append(i['url'])
        content += i['content'] + "\n\n\n"
    return content,url

supervisior_template =  ""
llm_template =""
rag_template =""
internet_search_template =""



class AgentState(TypedDict):
    message : str
    validation_attempts :int
    current_step:int
    final_answer:str

def supervisor_node():
    pass

prompt = PromptTemplate(
    template ="",
    input_variables = ['query']

)
