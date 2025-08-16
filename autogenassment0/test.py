from som.dietryneedssom import diertery_som
from som.mealssom import meal_plan_som
from agents.inneragents.ActivityAgent import activity_agent
from agents.inneragents.GoalAgent import goal_agent
from agents.inneragents.PreferenceAgent import preference_agent
from agents.inneragents.user_proxy_agent import user_proxy_agent
from teams.innerteams.MealPlanCreationTeam import meal_planning_agent
from teams.innerteams.DietaryNeedsteam import dietry_team
from teams.outerteams.meal_plan_generator import meal_plan_generator
import asyncio
from models.open_ai_model_client import get_model_client
from autogen_agentchat.ui import Console
from autogen_agentchat.messages import TextMessage


model_client = get_model_client()
meal_planner_agent = dietry_team(model_client)

task = '''
"Hi, I’m 32 years old, male, height 5’9 inc”, weight 82 kg. I want to lose about 5–6 kg in the next 2 months.
I work in an office so I’m mostly sitting, but I go for a 30-minute walk 4 times a week so slightly moderate activity.I eat chicken and fish but no beef or pork. I’m lactose intolerant, and I like rice, paneer, eggs, and apples.

'''
# I work in an office so I’m mostly sitting, but I go for a 30-minute walk 4 times a week so slightly moderate activity.I eat chicken and fish but no beef or pork. I’m lactose intolerant, and I like rice, paneer, eggs, and apples.

task1 ='''- **Weight Loss Goal**: Lose 5–6 kg in two months. 
- **Calorie Target**: Approximately 2,293 kcal/day to achieve a moderate calorie deficit.
- **Dietary Preferences**:
  - Includes: Chicken, fish, rice, paneer, eggs, apples.
  - Excludes: Beef, pork, dairy due to lactose intolerance.
- **Dietary Restrictions**: Lactose intolerance; avoid beef and pork.
- **Activity Level**: Lightly active due to office work, with walking 30 minutes, four times a week.
- **Activity Adjustments**:
  - Frequency of walks increased to 5 times a week.
  - Addition of brisk walking, light jogging, or cycling for 30–45 minutes per session.
  - Incorporate strength training 2–3 times weekly with bodyweight exercises or light weights.'''
#I work in an office so I’m mostly sitting, but I go for a 30-minute walk 4 times a week.I eat chicken and fish but no beef or pork. I’m lactose intolerant, and I like rice, paneer, eggs, and apples.

task3 ='''**Meal Plan Summary:**

**Breakfast:**

* Scrambled Eggs with Spinach and whole-wheat toast
* Chicken and Vegetable Stir-fry with brown rice
* Greek Yogurt (dairy-free) with Berries and Nuts
* Oatmeal with Apples and Cinnamon
* Fish (Salmon or Tuna) with a side salad

**Lunch:**

* Chicken Salad Sandwich on Whole-Wheat Bread
* Lentil Soup with whole-grain crackers
* Leftover Chicken and Vegetable Stir-fry
* Tuna Salad with mixed greens and avocado
* Paneer and Vegetable Curry with brown rice

**Dinner:**

* Baked Fish with Roasted Vegetables
* Chicken and Vegetable Curry with Brown Rice
* Shrimp Scampi with zucchini noodles
* Vegetarian Chili with Brown Rice
* Egg Fried Rice

**Snacks:**

* Apple slices with peanut butter (ensure allergy-free)
* Handful of almonds or walnuts
* Greek Yogurt (dairy-free) with fruit
* Hard-boiled eggs
* Mixed vegetables with hummus (ensure allergy-free)'''

stream = meal_planner_agent.run_stream(task=task)
task = TextMessage(content=task,source='User')
async def main():
    # async for message in meal_planner_agent.run_stream(task=task):
    #         print(message.source)
    #         print(message.content)
    await Console(stream)
    
    
    # result = await meal_planner_agent.run(task=task)

    # for each_agent_message in result.messages:
    #     print(f'{((each_agent_message))} ' )
    #     print('\n \n')


if (__name__ == '__main__'):
    asyncio.run(main()) 