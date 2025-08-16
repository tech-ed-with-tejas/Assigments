from autogen_agentchat.agents import AssistantAgent
from agents.inneragents.prompt_template import PREFERENCE_AGENT_PROMPT

def preference_agent(model_client):
    preference_agent_instance = AssistantAgent(
        name='Preference_Agent',
        model_client=model_client,
        description="Your task is to collect and apply the user's dietary preferences and restrictions.",
        system_message=PREFERENCE_AGENT_PROMPT
    )
    return preference_agent_instance