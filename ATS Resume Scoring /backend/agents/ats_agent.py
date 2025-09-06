
from autogen_agentchat.agents import AssistantAgent
from backend.prompts import ATS_AGENT_PROMPTE
from backend.utils.pydantic_validator import ATSVisualizationScore
from backend.utils.autogen_rag_chroma import get_chroma_db_for_agents

db= get_chroma_db_for_agents()

def ats_agent(model_client):
    goal_agent_instance = AssistantAgent(
        name='ATS_SCORING_AGENT',
        model_client=model_client,
        description="Agent that help in scoring the resume againish JD",
        system_message=ATS_AGENT_PROMPTE ,
        output_content_type=ATSVisualizationScore,
        memory=[db]
    )
    return goal_agent_instance