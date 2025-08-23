from teams.outerteams.meal_plan_generator import meal_plan_generator
import asyncio
from models.open_ai_model_client import get_model_client
from autogen_agentchat.ui import Console



model_client = get_model_client()
meal_planner_agent = meal_plan_generator(model_client)
task = '''
"Hi, I’m 32 years old, male, height 5’9”, weight 82 kg. I want to lose about 5–6 kg in the next 2 months.
I work in an office so I’m mostly sitting, but I go for a 30-minute walk 4 times a week.I eat chicken and fish but no beef or pork. I’m lactose intolerant, and I like rice, paneer, eggs, and apples.
generate me a meal plan for 2 months.
'''

stream = meal_planner_agent.run_stream(task=task)

async def main():
    
    
    await Console(stream)


if (__name__ == '__main__'):
    asyncio.run(main()) 