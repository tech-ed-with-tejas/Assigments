from som.dietryneedssom import diertery_som
from som.mealssom import meal_plan_som
from autogen_agentchat.teams import SelectorGroupChat,RoundRobinGroupChat 

from agents.inneragents.user_proxy_agent import user_proxy_agent
from autogen_agentchat.conditions import TextMentionTermination,MaxMessageTermination
from agents.outputagent.output_summariser import summariser_agent

SELECTOR_PRMPT = """
You are the Task Selector Agent.
Coordinate between agents to gather the user's dietary goals, activity, preferences, and meal plan.

Inputs:
- Roles: {roles}
- Conversation history: {history}
- Participants/Agents: {participants}

Sequence: Dietary_Needs_SOM → Meals_SOM → Summariser_Agent.
Before moving to the next step, get user approval.
Once all steps are done, compile and confirm the full plan with the user; update if needed.
Format task calls as: 1. <agent> : <task>
Rules: Call ONE agent at a time, follow sequence, don't skip steps.
"""
termination_condition = TextMentionTermination(text="APPROVE") | MaxMessageTermination(max_messages=6)
def meal_plan_generator(model_client):
    dietary_needs_som_instance = diertery_som(model_client)
    meal_suggestion_agent_instance = meal_plan_som(model_client)
    summariser_agent_instance = summariser_agent(model_client)
    user_proxy_agent_instance = user_proxy_agent()

    meal_plan_team = RoundRobinGroupChat(
        description="Meal Plan Generation Team",
        participants=[dietary_needs_som_instance, meal_suggestion_agent_instance,summariser_agent_instance],
        # model_client=model_client,
        termination_condition=termination_condition,
        # allow_repeated_speaker=True,
        # selector_prompt=SELECTOR_PRMPT,
    )

    return meal_plan_team