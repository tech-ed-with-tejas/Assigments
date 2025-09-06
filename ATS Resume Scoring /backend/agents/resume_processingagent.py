from autogen_agentchat.agents import AssistantAgent
from backend.prompts import RESUME_PROCESSING_AGENT_PROMPT
from backend.utils.pydantic_validator import Resume


def resume_processing_agent(model_client):
    goal_agent_instance = AssistantAgent(
        name='RESUME_PROCESSING_AGENT',
        model_client=model_client,
        description="You Would be given with a resume prased to text.Your task to asses the resume and organise it",
        system_message=RESUME_PROCESSING_AGENT_PROMPT,
        output_content_type=Resume,
    )
    return goal_agent_instance