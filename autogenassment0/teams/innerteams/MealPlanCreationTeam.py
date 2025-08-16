from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination,MaxMessageTermination
from agents.inneragents.MealSuggestionAgent import meal_suggestion_agent
from agents.inneragents.NutritionBalanceAgent import nutrition_balance_agent
from agents.inneragents.user_proxy_agent import user_proxy_agent

termination_condition = TextMentionTermination(text="APPROVE") | MaxMessageTermination(max_messages=6)



def meal_planning_agent(model_client):

    meal_suggestion_agent_instance = meal_suggestion_agent(model_client)
    nutrition_balance_agent_instance = nutrition_balance_agent(model_client)
    user_proxy_agent_instance = user_proxy_agent()
    meal_planning_team = RoundRobinGroupChat(
        participants=[meal_suggestion_agent_instance, nutrition_balance_agent_instance,user_proxy_agent_instance],
        termination_condition=termination_condition,
    )

    return meal_planning_team