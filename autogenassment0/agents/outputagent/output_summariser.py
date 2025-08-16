from autogen_agentchat.agents import AssistantAgent
from agents.outputagent.PROMPT import OUTPUT_SUMMARISER_PROMPT

def summariser_agent(model_client):
    summariser_agent_instance = AssistantAgent(
        name='Summariser_Agent',
        model_client=model_client,
        description='An agent designed to summarize the output of diet plan needs and meal planner inputs into a concise and actionable summary.',
        system_message=OUTPUT_SUMMARISER_PROMPT
    )
    return summariser_agent_instance