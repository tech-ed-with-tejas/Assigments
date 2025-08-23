from autogen_agentchat.agents import  SocietyOfMindAgent

from teams.innerteams.MealPlanCreationTeam import meal_planning_agent
SOM_MEAL_PLANNER = """
Take the outputs from the NutritionBalanceAgent and MealSuggestionAgent, 
and compile a summarized meal plan that aligns with the user’s activity level and calorie goals.
The plan should list meal names only (no recipes).
Please Rutern :TASK Status Done once you task is Completed.

"""

def meal_plan_som(model_client):
    dietary_needs_team_instance = meal_planning_agent(model_client)
    dietary_needs_som = SocietyOfMindAgent(
        name="Meals_SOM",
        team=dietary_needs_team_instance,
        model_client=model_client,
        instruction=SOM_MEAL_PLANNER
    )
    return dietary_needs_som