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
meal_planner_agent = meal_plan_generator(model_client)

task = '''
"Hi, I’m 32 years old, male, height 5’9 inc”, weight 82 kg. I want to lose about 5–6 kg in the next 2 months.
I work in an office so I’m mostly sitting, but I go for a 30-minute walk 4 times a week so slightly moderate activity.I eat chicken and fish but no beef or pork.
I’m lactose intolerant, and I like rice, paneer, eggs, and apples.

'''
# I work in an office so I’m mostly sitting, but I go for a 30-minute walk 4 times a week so slightly moderate activity.I eat chicken and fish but no beef or pork. I’m lactose intolerant, and I like rice, paneer, eggs, and apples.
#I work in an office so I’m mostly sitting, but I go for a 30-minute walk 4 times a week so slightly moderate activity.I eat chicken and fish but no beef or pork. I’m lactose intolerant, and I like rice, paneer, eggs, and apples.

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

task3 ='''**Summarized Meal Plan:**

**Breakfast:**
1. Scrambled Eggs with Spinach and Whole-Wheat Toast
2. Avocado Toast with Poached Egg on Whole-Grain Bread
3. Greek Yogurt (dairy-free) with Berries and Chia Seeds
4. Oatmeal with Apples, Cinnamon, and Almond Butter
5. Smoked Salmon with Avocado on Rye Bread

**Lunch:**
1. Grilled Chicken Salad with Quinoa and Mixed Greens
2. Lentil Soup with Whole-Grain Crackers
3. Turkey and Avocado Wrap with Whole-Wheat Tortilla
4. Tuna Salad with Mixed Greens and Olive Oil Dressing
5. Chickpea and Vegetable Stir-fry with Brown Rice

**Dinner:**
1. Baked Fish with Roasted Vegetables and Quinoa
2. Chicken and Vegetable Curry with Brown Rice
3. Grilled Shrimp with Zucchini Noodles and Pesto
4. Vegetarian Chili with Brown Rice
5. Stir-fried Tofu with Broccoli and Cashews

**Snacks:**
1. Apple Slices with Almond Butter
2. Handful of Almonds or Walnuts
3. Greek Yogurt (dairy-free) with Fresh Fruit
4. Hard-Boiled Eggs
5. Mixed Vegetables with Hummus

This meal plan is designed to maintain weight and improve overall health, aligning with a moderate activity level and a calorie goal of 2000-2200 calories per day. It includes a balanced distribution of macronutrients and adheres to dietary preferences and restrictions.'''

# stream = meal_planner_agent.run_stream(task=task)
task = TextMessage(content=task,source='User')
async def main():
    # async for message in meal_planner_agent.run_stream(task=task):
    #         print(message.source)
    #         print(message.content)
    # await Console(stream)
    
    
    # result = await meal_planner_agent.run(task=task)

    # for each_agent_message in result.messages:
    #     print(f'{((each_agent_message))} ' )
    #     print('\n \n')
    await Console(meal_planner_agent.run_stream(task=task),output_stats=True)


if (__name__ == '__main__'):
    asyncio.run(main()) 