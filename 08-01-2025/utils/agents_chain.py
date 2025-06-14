
from langchain_core.output_parsers import StrOutputParser,PydanticOutputParser
from utils.pydantic_validators import SupervisorOutputparser,ValidationResult
from utils.CONSTANT import SUPERVISE_NODE_TEMPLATE,LLM_NODE_TEMPLATE,RAG_LLM_TEMPLATE,WEB_SEARCH_TEMPLATE,VALIDATION_PROMPT
from utils.utils import Agent,search_for_web


superive_node_output_parser = PydanticOutputParser(pydantic_object = SupervisorOutputparser)
validtion_output_parser = PydanticOutputParser(pydantic_object=ValidationResult)

Supervisor_agent = Agent(
    prompt_template=SUPERVISE_NODE_TEMPLATE,
    output_parser=superive_node_output_parser,
    input_variables=["user_query"],
    partial_variables={"format_instructions": superive_node_output_parser.get_format_instructions() }
)

llm_agent = Agent(
    prompt_template=LLM_NODE_TEMPLATE,
    output_parser=StrOutputParser(),
    input_variables=["user_query"],
)

rag_agent = Agent(
    prompt_template=RAG_LLM_TEMPLATE,
    output_parser=StrOutputParser(),
    input_variables=["user_query","context"],
)

web_crawl_agent = Agent(
    prompt_template=WEB_SEARCH_TEMPLATE,
    output_parser=StrOutputParser(),
    input_variables=["user_query","context"],
)

validation_decision_agent = Agent(prompt_template=VALIDATION_PROMPT,input_variables=['user_query',"llm_output"],output_parser=validtion_output_parser,
                                      partial_variables={"format_instructions": validtion_output_parser.get_format_instructions() }
)

def decide_model(user_query: str) -> dict:
    """
    Decides which model to use based on the user's query.
    """
    invoke_dict = {"user_query": user_query}
    response = Supervisor_agent.decide(invoke_dict=invoke_dict)
    return response

def llm_decision(user_query: str) -> dict:
    """
    Processes the user's query using the LLM agent.
    """
    invoke_dict = {"user_query": user_query}

    response = llm_agent.decide(invoke_dict=invoke_dict)
    return response
def rag_decision(user_query: str) -> dict:
    """Processes the user's query using the RAG agent with additional context.
    """
    context ='Please answere on your own. We dont have any context'  # Placeholder for context retrieval logic
    invoke_dict = {"user_query": user_query, "context": context}
    response = rag_agent.decide(invoke_dict=invoke_dict)
    return response

def web_search_decision(user_query: str) -> dict:
    """
    Processes the user's query using the web search agent with additional context.
    """
    
    context,url = search_for_web(user_query)
   
    invoke_dict = {"user_query": user_query, "context": context}

    response = web_crawl_agent.decide(invoke_dict=invoke_dict)
  
    return response,url


def validation_decision(user_query: str,llm_resposne:str) -> dict:
    """
    Validates the user's query.
    """
    invoke_dict = {"user_query": user_query, "llm_output": llm_resposne}
    response = validation_decision_agent.decide(invoke_dict=invoke_dict)
    return response


if __name__ == "__main__":
    user_query = "Give me a diet plan i am 25 years old?"
    decision = decide_model(user_query)
    print(decision.decision)
    if decision.decision == 'Web Search':
        response, urls = web_search_decision(user_query)    
    elif decision.decision == 'RAG': 
        response = rag_decision(user_query)            
    else:       
        response = llm_decision(user_query)                 
    print(f"Decision: {decision.decision}")
    print(f"Response: {response}")
    print(f"URLs: {urls if 'urls' in locals() else 'N/A'}")
    validation_response = validation_decision(user_query, response)         
    print(f"Validation Result: {validation_response.is_valid}")
    print(f"Confidence Score: {validation_response.confidence_score}")
    print(f"Issues: {validation_response.issues}")
    print(f"Suggestion: {validation_response.suggestion}")
#     print(f"Decision: {decision['decision']}")
#     print(f"Reason: {decision['reason']}")
