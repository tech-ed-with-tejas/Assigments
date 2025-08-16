from autogen_agentchat.agents import AssistantAgent
from agents.inneragents.prompt_template import ACTIVITY_AGENT_PROMPT

def activity_agent(model_client):
    activity_agent_instance = AssistantAgent(
        name='Activity_Agent',
        model_client=model_client,
        description="Your role is to act as an activity tracker and fitness advisor for the user. like exersize and walking.",
        system_message=ACTIVITY_AGENT_PROMPT
    )
    return activity_agent_instance