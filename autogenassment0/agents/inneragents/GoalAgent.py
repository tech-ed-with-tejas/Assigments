from autogen_agentchat.agents import AssistantAgent
from agents.inneragents.prompt_template import GOAL_AGENT_PROMPT

def goal_agent(model_client):
    goal_agent_instance = AssistantAgent(
        name='Goal_Agent',
        model_client=model_client,
        description="Your task is to determine the user's target daily calorie intake based on their personal details and weight goal.",
        system_message=GOAL_AGENT_PROMPT
    )
    return goal_agent_instance