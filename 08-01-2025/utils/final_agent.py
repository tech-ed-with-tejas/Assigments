from langgraph.graph import StateGraph,END
from utils.agents_chain import llm_decision,rag_decision,web_search_decision,decide_model,validation_decision
from typing import TypedDict, Annotated, Sequence,List
from langchain_core.messages import BaseMessage
import operator


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    urls: Annotated[List[str], operator.add]
    validation_flag :Annotated[bool, operator.or_]
    attempts: Annotated[int, operator.add]  
    final_message: Annotated[str, operator.add]


def supervisor_model(state:AgentState) -> AgentState:
    """
    Supervisor model to decide which model to use based on the user's query.
    """
    
    user_query = state['messages'][-1]
    decision = decide_model(user_query)
    state['messages'].append(decision.decision)
    return state

def routuer_node(state:AgentState) -> str:
    """Router node to route the query to the appropriate model based on the decision."""
    value = state['messages'][-1]

    print("Outout of supervisior node is ",value)
    if value == "Web Search":
        return "Web Search"
 
    if value == "RAG":
        return "RAG"
   
    return "LLM"
   
    
       
def rag_node(state:AgentState) -> AgentState:
    """RAG node to process the user's query with additional context."""
    user_query = state['messages'][0]
    response = rag_decision(user_query)
    state['messages'].append(response)
    return state

def llm_node(state:AgentState) -> AgentState:
    """LLM node to process the user's query."""
    user_query = state['messages'][0]
    response = llm_decision(user_query)
    state['messages'].append(response)
    return state
def web_search_node(state:AgentState) -> AgentState:
    """Web search node to process the user's query using web search."""
    user_query = state['messages'][0]
    response, urls = web_search_decision(user_query)
    state['messages'].append(response)
    if isinstance(urls, list):
        state['urls'].extend(urls)
    else:
        state['urls'].append(urls)
    return state

def validation_node(state:AgentState) -> AgentState:
    """Validation node to validate the response from the LLM."""
    user_query = state['messages'][0]
    llm_output = state['messages'][-1]  
    validation_response = validation_decision(user_query, llm_output)
    state['validation_flag'] = validation_response.is_valid
    state['attempts'] += 1
    
    return state

def validation_route(state:AgentState) -> str:
    """Route based on validation result."""
    validation_response = state['validation_flag']
    if validation_response:
        return "complete"
    else:
        
        print(state['attempts'])
        if state['attempts'] >= 3:
            return "complete"
    return "retry_supervisor"  
def final_node(state:AgentState) -> AgentState:
    """Final node to return the final response."""
    # print(state['messages'][-1])
    state['final_message'] = state['messages'][-1]
    return state

agent = StateGraph(AgentState)
agent.add_node("supervisor", supervisor_model)
agent.add_node("llm_node", llm_node)
agent.add_node("rag_node", rag_node)
agent.add_node("web_crawler", web_search_node)
agent.add_node("validation_node", validation_node)
agent.add_node("final_node", final_node)
agent.add_conditional_edges("supervisor", routuer_node,{"LLM": "llm_node", "RAG": "rag_node", "Web Search": "web_crawler"})
agent.add_conditional_edges("validation_node", validation_route, {"complete": "final_node", "retry_supervisor":"supervisor",})
agent.set_entry_point( "supervisor")
agent.add_edge("llm_node", "validation_node")
agent.add_edge("rag_node", "validation_node")
agent.add_edge("web_crawler", "validation_node")
agent.add_edge("validation_node", "final_node")
agent.set_finish_point("final_node")

app = agent.compile()

state =         {"messages":["what is the protien?"],"validation_flag":False, "attempts":0,"urls":[],"final_message":""}
png_bytes = app.get_graph().draw_mermaid_png()

# Save to file
# with open("graph_output.png", "wb") as f:
#     f.write(png_bytes)

# print("Saved graph_output.png")

def get_app():
    return app
if __name__ =="__main__":
    
    # app = agent.compile()
    # app.get_graph().print_ascii()
    # result = app.invoke(state
    # )

    # print(result['final_message'])
    # print(result['urls'])
  

    pass