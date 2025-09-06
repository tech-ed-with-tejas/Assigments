from autogen_agentchat.agents import AssistantAgent
from backend.prompts import JOB_DESCRIPTION_ANALYSER_PROMPT
# from backend.utils.pydantic_validator import Resume


def job_decription_processing_agent(model_client):
    goal_agent_instance = AssistantAgent(
        name='Job_Description_Analyser',
        model_client=model_client,
        description="You Would be given with Job description your job is to analyse and map it into a structured required format.",
        system_message=JOB_DESCRIPTION_ANALYSER_PROMPT 
,
        # output_content_type=Resume,
    )
    return goal_agent_instance