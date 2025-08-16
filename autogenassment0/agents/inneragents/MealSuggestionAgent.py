from autogen_agentchat.agents import AssistantAgent
from agents.inneragents.prompt_template import MEAL_SUGGESTION_AGENT_PROMPT

def meal_suggestion_agent(model_client):
    meal_suggestion_agent_instance = AssistantAgent(
        name='Meal_Suggestion_Agent',
        model_client=model_client,
        description='An agent designed to suggest meals based on user preferences, goals, and nutritional balance.',
        system_message=MEAL_SUGGESTION_AGENT_PROMPT
    )
    return meal_suggestion_agent_instance