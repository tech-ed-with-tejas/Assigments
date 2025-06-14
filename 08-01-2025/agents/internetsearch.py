from langchain_community.tools.tavily_search import TavilySearchResults
import os
from dotenv import load_dotenv
load_dotenv()


TAVILY_API_KEY=os.getenv("TAVILY_API_KEY")


tool=TavilySearchResults(tavily_api_key=TAVILY_API_KEY,max_results=3,include_images=False,include_image_descriptions=False,
                         days=30,)


def search_for_web(query):

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