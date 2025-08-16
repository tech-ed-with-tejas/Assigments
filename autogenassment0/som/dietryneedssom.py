from autogen_agentchat.agents import  SocietyOfMindAgent

from teams.innerteams.DietaryNeedsteam import dietry_team

SOM_DIETARY_ANALYSIS = """
Take the output from the Dietary Needs Analysis Team and generate a bullet-point list
covering all user requirements (goals, calorie arget, preferences, restrictions, and activity adjustments).
"""

def diertery_som(model_client):
    dietary_needs_team_instance = dietry_team(model_client)
    dietary_needs_som = SocietyOfMindAgent("Dietary_Needs_SOM", team=dietary_needs_team_instance, model_client=model_client,instruction=SOM_DIETARY_ANALYSIS)
    return dietary_needs_som