from autogen_agentchat.agents import AssistantAgent
from agents.inneragents.prompt_template import NUTRITION_BALANCE_AGENT_PROMPT

def nutrition_balance_agent(model_client):
    nutrition_balance_agent_instance = AssistantAgent(
        name='Nutrition_Balance_Agent',
        model_client=model_client,
        description='An agent designed to ensure meals are nutritionally balanced based on user goals and preferences.',
        system_message=NUTRITION_BALANCE_AGENT_PROMPT
    )
    return nutrition_balance_agent_instance