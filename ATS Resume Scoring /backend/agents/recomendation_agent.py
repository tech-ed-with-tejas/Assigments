from autogen_agentchat.agents import AssistantAgent
from backend.prompts import RECOMENDATION_AGENT_PROMPT
# from backend.utils.pydantic_validator import Resume
from backend.utils.autogen_rag_chroma import get_chroma_db_for_agents

db= get_chroma_db_for_agents()

def recomendation_agent(model_client):
    goal_agent_instance = AssistantAgent(
        name='Recomendation_Agent',
        model_client=model_client,
        description="You Would be given with Job description and user resume and ats scoring.Please provide recomendation to improve the resume to get better ats score.",
        system_message= RECOMENDATION_AGENT_PROMPT,
        memory=[db]
    )
    return goal_agent_instance  