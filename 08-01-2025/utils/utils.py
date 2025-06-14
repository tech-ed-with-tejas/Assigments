
from langchain_community.tools.tavily_search import TavilySearchResults
import os
from dotenv import load_dotenv
load_dotenv()
from utils.CONSTANT import MODEL_NAME

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
# from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
os.environ['GOOGLE_API_KEY'] = os.getenv("GOOGLE_API_KEY")
# os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
# openai_model = ChatOpenAI(model="o1-mini")

model=ChatGoogleGenerativeAI(model=MODEL_NAME)
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


class Agent:
    def __init__(self, prompt_template, output_parser,input_variables:list[str],partial_variables:dict[str, str]={}):
        """
        Initializes the decider agent with a prompt and parser.
        """
        self.prompt = PromptTemplate(
            template=prompt_template,
            input_variables=input_variables,
            partial_variables=partial_variables
        )
        self.parser = output_parser
        self.chain = self.prompt | model | self.parser

    def decide(self, invoke_dict:dict[str,str]) -> dict:
        """
        Executes the decision logic based on the user's query.
        """
        response = self.chain.invoke(invoke_dict)
        
        return response
    

if __name__ == "__main__":
    #
    class OutputSchema(BaseModel):
        decision: str = Field(..., description="The decision made by the agent.")
        reason: str = Field(..., description="The reason for the decision.")

    output_parser = PydanticOutputParser(pydantic_object=OutputSchema)

    prompt_template = """
    You are a decision-making agent. Based on the input query, provide a decision and the reason for it.{format_instructions}

    Query: {query}
    

    Decision: {{decision}}
    Reason: {{reason}}
    """

    agent = Agent(
        prompt_template=prompt_template,
        output_parser=output_parser,
        input_variables=["query"],
        partial_variables={"format_instructions": output_parser.get_format_instructions() }
    )

    # Example usage
    query = "Should I invest in renewable energy stocks?"
    response = agent.decide({"query": query})
    print(response)




