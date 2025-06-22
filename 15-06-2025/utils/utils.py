import requests
from dotenv import load_dotenv
load_dotenv()
import os
from langchain_core.tools import tool
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from utils.validators import AgentRequirement
os.environ['GROQ_API_KEY']=os.getenv("GROQ_API_KEY")
from langchain.tools import tool

llm = ChatGroq(
    model_name="deepseek-r1-distill-llama-70b",
    temperature=0
)

API_KEY = os.getenv("CURRENCY_API_KEY") # Replace with your actual API Key

def convert_currency( from_currency, to_currency):
    """
    Function to convert currency using the ExchangeRate-API.

    Args:
        from_currency (str): The currency code to convert from (e.g., 'EUR').
        to_currency (str): The currency code to convert to (e.g., 'GBP').

    Returns:
        float: The conversion rate from the source currency to the target currency.
        None: If the API call fails or an error occurs.
    """
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{from_currency}/{to_currency}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        data = response.json()
        if data.get("result") == "success":
            return data.get("conversion_rate")
        else:
            print(f"Error: {data.get('error-type', 'Unknown error')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
@tool
def convert_cost(cost, from_currency, to_currency):
    """
    Function to convert a cost from one currency to another.

    Args:
        cost (float): The cost in the source currency.
        from_currency (str): The currency code of the source currency (e.g., 'EUR').
        to_currency (str): The currency code of the target currency (e.g., 'GBP').

    Returns:
        float: The cost in the target currency.
        None: If the conversion rate could not be retrieved.
    """
    conversion_rate = convert_currency( "EUR", "GBP")

    conversion_rate = convert_currency(from_currency, to_currency)
    if conversion_rate:
        return cost * conversion_rate
    else:
        print("Failed to retrieve conversion rate.")
        return None

@tool
def add(*args):
    """
    Function to add multiple numbers.

    Args:
        *args: A variable number of arguments to add.

    Returns:
        float: The sum of the numbers.
    """
    return sum(args)

@tool
def multiply(*args):
    """
    Function to multiply multiple numbers.

    Args:
        *args: A variable number of arguments to multiply.

    Returns:
        float: The product of the numbers.
    """
    result = 1
    for num in args:
        result *= num
    return result

@tool
def calculate_total_cost(costs):
    """
    Function to calculate the total cost from a list of costs.

    Args:
        costs (list): A list of costs.

    Returns:
        float: The total cost.
    """
    return sum(costs)

@tool
def calculate_daily_budget(total_cost, days):
    """
    Function to calculate the daily budget.

    Args:
        total_cost (float): The total cost.
        days (int): The number of days.

    Returns:
        float: The daily budget.
    """
    if days <= 0:
        raise ValueError("Number of days must be greater than zero.")
    return total_cost / days
class Agent:
    def __init__(self, prompt_template,input_variables:list[str],partial_variables:dict[str, str]={},tools=[],output_parser=None):
        """
        Initializes the decider agent with a prompt and parser.
        """
        self.prompt = PromptTemplate(
            template=prompt_template,
            input_variables=input_variables,
            partial_variables=partial_variables
        )
        if  len(tools)>0:
            model = llm.bind_tools(tools)
        else:
            model =llm
        if output_parser:
            self.parser = output_parser
            self.chain = self.prompt | model | self.parser
        else:
            self.chain = self.prompt | model 


    def decide(self, invoke_dict:dict[str,str]) -> dict:
        """
        Executes the decision logic based on the user's query.
        """
        response = self.chain.invoke(invoke_dict)
        
        return response
    

if __name__ == "__main__":
    # cost_in_gbp = convert_cost(100, "EUR", "GBP")
    # if cost_in_gbp:
    #     print(f"Cost in GBP: {cost_in_gbp}")

    
    # Example usage of the Calculator class
    pass