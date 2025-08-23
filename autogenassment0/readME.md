# Autogenassment0 - Multi-Agent Dietary Planning System

This project is a modular, agent-based system for generating, reviewing, and optimizing personalized meal plans and dietary recommendations using advanced language models.


## About the Project

- **Intelligent Nutrition & Meal Planning**: Designed to create personalized nutrition and meal plans, specifically tailored foreach  individuals.
- **Multi-Agent Collaboration**: The system utilizes multiple specialized agents that work together to analyze user goals, dietary preferences, and nutritional requirements.
- **Advanced Language Models**: By leveraging state-of-the-art language models, the platform generates accurate and relevant dietary recommendations.
- **Personalized Dietary Recommendations**: Users receive meal suggestions and nutrition plans that are customized to their unique health objectives and lifestyle.
- **Meal Plan Optimization**: Agents continuously review and refine meal plans to ensure nutritional balance and support effective weight loss.
- **User-Centric Approach**: The platform is built to help users efficiently achieve their health and weight loss goals through actionable, data-driven guidance.
- **Extensible & Modular Architecture**: The system is modular, allowing for easy integration of new agents, features, or workflows to adapt to evolving dietary science and user needs.


## Block Diagram

![Image](./assets/pic1.svg)

## Flow Diagram

![Image](./assets/pic2.svg)

## Directory Structure

- **main.py** / **streamlit_app.py**: Entry points for running the system (CLI and Streamlit UI).
- **agents/**: Contains agent logic.
  - **inneragents/**: Specialized agents for user goals, preferences, nutrition balance, meal suggestions, and reviews.
  - **outputagent/**: Summarizes and formats agent outputs.
- **config/**: Utility functions and configuration.
- **models/**: Language model client wrappers (e.g., OpenAI).
- **som/**: Society of Mind modules for dietary needs and meal reasoning.
- **teams/**: Team-based orchestration for meal plan creation.
  - **innerteams/**: Teams for dietary needs and meal planning.
  - **outerteams/**: High-level orchestration (e.g., meal plan generator).

## Features

- **Multi-Agent Collaboration**: Agents work together to analyze user goals, preferences, and nutritional needs.
- **Meal Plan Generation**: Automated creation of meal plans tailored to user input.
- **Review & Optimization**: Agents review and refine meal suggestions for nutritional balance.
- **Extensible Architecture**: Easily add new agents or teams for custom workflows.
- **Streamlit UI**: Interactive interface for user queries and meal plan visualization.

## Getting Started

1. Clone the repository.
2. Install dependencies (see `.env` and requirements in your environment).
3. Run the Streamlit app:
   ```sh
   streamlit run streamlit_app.py TDB
   ```
   Or run the CLI:
   ```sh
   python main.py
   ```


## SAMPLE OUTPUT 

  *USER* : "Hi, I’m 32 years old, male, height 5’9”, weight 82 kg. I want to lose about 5–6 kg in the next 1 months.
I work in an office so I’m mostly sitting, but I go for a 30-minute walk 4 times a week.I eat chicken and fish but no beef or pork. I’m lactose intolerant, and I like rice, paneer, eggs, and apples.
generate me a meal plan for 1 month."



## OUTPUT 
**4-Week Eating Schedule**

**Week 1:**

| Day       | Meal Time | Meal Description                                      |
|-----------|-----------|-------------------------------------------------------|
| Monday    | Breakfast | Scrambled eggs with spinach and tomatoes, whole-grain toast, apple slices |
|           | Lunch     | Grilled chicken salad with mixed greens, cherry tomatoes, cucumbers, vinaigrette |
|           | Dinner    | Baked salmon with steamed asparagus and quinoa        |
|           | Snack     | Apple slices with almond butter                       |
| Tuesday   | Breakfast | Oatmeal with almond milk, sliced apples, cinnamon     |
|           | Lunch     | Quinoa bowl with chickpeas, roasted vegetables, lemon-tahini dressing |
|           | Dinner    | Grilled chicken breast with roasted sweet potatoes, green beans |
|           | Snack     | Carrot sticks with hummus                             |
| Wednesday | Breakfast | Paneer and vegetable stir-fry with brown rice         |
|           | Lunch     | Tuna salad with lettuce, cherry tomatoes, olives, balsamic vinaigrette |
|           | Dinner    | Paneer tikka with brown rice, cucumber salad          |
|           | Snack     | Mixed nuts (almonds, walnuts, cashews)                |
| Thursday  | Breakfast | Avocado toast with poached egg, apple slices          |
|           | Lunch     | Stir-fried tofu with broccoli, carrots, jasmine rice  |
|           | Dinner    | Fish curry with basmati rice, sautéed spinach         |
|           | Snack     | Rice cakes with avocado, cherry tomatoes              |
| Friday    | Breakfast | Smoothie with almond milk, banana, spinach, plant-based protein powder |
|           | Lunch     | Lentil soup with whole-grain bread                    |
|           | Dinner    | Vegetable stir-fry with tofu over brown rice          |
|           | Snack     | Hard-boiled eggs with salt and pepper                 |
| Saturday  | Breakfast | Scrambled eggs with spinach and tomatoes, whole-grain toast, apple slices |
|           | Lunch     | Grilled chicken salad with mixed greens, cherry tomatoes, cucumbers, vinaigrette |
|           | Dinner    | Baked salmon with steamed asparagus and quinoa        |
|           | Snack     | Apple slices with almond butter                       |

**Week 2:**

| Day       | Meal Time | Meal Description                                      |
|-----------|-----------|-------------------------------------------------------|
| Monday    | Breakfast | Oatmeal with almond milk, sliced apples, cinnamon     |
|           | Lunch     | Quinoa bowl with chickpeas, roasted vegetables, lemon-tahini dressing |
|           | Dinner    | Grilled chicken breast with roasted sweet potatoes, green beans |
|           | Snack     | Carrot sticks with hummus                             |
| Tuesday   | Breakfast | Paneer and vegetable stir-fry with brown rice         |
|           | Lunch     | Tuna salad with lettuce, cherry tomatoes, olives, balsamic vinaigrette |
|           | Dinner    | Paneer tikka with brown rice, cucumber salad          |
|           | Snack     | Mixed nuts (almonds, walnuts, cashews)                |
| Wednesday | Breakfast | Avocado toast with poached egg, apple slices          |
|           | Lunch     | Stir-fried tofu with broccoli, carrots, jasmine rice  |
|           | Dinner    | Fish curry with basmati rice, sautéed spinach         |
|           | Snack     | Rice cakes with avocado, cherry tomatoes              |
| Thursday  | Breakfast | Smoothie with almond milk, banana, spinach, plant-based protein powder |
|           | Lunch     | Lentil soup with whole-grain bread                    |
|           | Dinner    | Vegetable stir-fry with tofu over brown rice          |
|           | Snack     | Hard-boiled eggs with salt and pepper                 |
| Friday    | Breakfast | Scrambled eggs with spinach and tomatoes, whole-grain toast, apple slices |
|           | Lunch     | Grilled chicken salad with mixed greens, cherry tomatoes, cucumbers, vinaigrette |
|           | Dinner    | Baked salmon with steamed asparagus and quinoa        |
|           | Snack     | Apple slices with almond butter                       |
| Saturday  | Breakfast | Oatmeal with almond milk, sliced apples, cinnamon     |
|           | Lunch     | Quinoa bowl with chickpeas, roasted vegetables, lemon-tahini dressing |
|           | Dinner    | Grilled chicken breast with roasted sweet potatoes, green beans |
|           | Snack     | Carrot sticks with hummus                             |

**Week 3:**

| Day       | Meal Time | Meal Description                                      |
|-----------|-----------|-------------------------------------------------------|
| Monday    | Breakfast | Paneer and vegetable stir-fry with brown rice         |
|           | Lunch     | Tuna salad with lettuce, cherry tomatoes, olives, balsamic vinaigrette |
|           | Dinner    | Paneer tikka with brown rice, cucumber salad          |
|           | Snack     | Mixed nuts (almonds, walnuts, cashews)                |
| Tuesday   | Breakfast | Avocado toast with poached egg, apple slices          |
|           | Lunch     | Stir-fried tofu with broccoli, carrots, jasmine rice  |
|           | Dinner    | Fish curry with basmati rice, sautéed spinach         |
|           | Snack     | Rice cakes with avocado, cherry tomatoes              |
| Wednesday | Breakfast | Smoothie with almond milk, banana, spinach, plant-based protein powder |
|           | Lunch     | Lentil soup with whole-grain bread                    |
|           | Dinner    | Vegetable stir-fry with tofu over brown rice          |
|           | Snack     | Hard-boiled eggs with salt and pepper                 |
| Thursday  | Breakfast | Scrambled eggs with spinach and tomatoes, whole-grain toast, apple slices |
|           | Lunch     | Grilled chicken salad with mixed greens, cherry tomatoes, cucumbers, vinaigrette |
|           | Dinner    | Baked salmon with steamed asparagus and quinoa        |
|           | Snack     | Apple slices with almond butter                       |
| Friday    | Breakfast | Oatmeal with almond milk, sliced apples, cinnamon     |
|           | Lunch     | Quinoa bowl with chickpeas, roasted vegetables, lemon-tahini dressing |
|           | Dinner    | Grilled chicken breast with roasted sweet potatoes, green beans |
|           | Snack     | Carrot sticks with hummus                             |
| Saturday  | Breakfast | Paneer and vegetable stir-fry with brown rice         |
|           | Lunch     | Tuna salad with lettuce, cherry tomatoes, olives, balsamic vinaigrette |
|           | Dinner    | Paneer tikka with brown rice, cucumber salad          |
|           | Snack     | Mixed nuts (almonds, walnuts, cashews)                |

**Week 4:**

| Day       | Meal Time | Meal Description                                      |
|-----------|-----------|-------------------------------------------------------|
| Monday    | Breakfast | Avocado toast with poached egg, apple slices          |
|           | Lunch     | Stir-fried tofu with broccoli, carrots, jasmine rice  |
|           | Dinner    | Fish curry with basmati rice, sautéed spinach         |
|           | Snack     | Rice cakes with avocado, cherry tomatoes              |
| Tuesday   | Breakfast | Smoothie with almond milk, banana, spinach, plant-based protein powder |
|           | Lunch     | Lentil soup with whole-grain bread                    |
|           | Dinner    | Vegetable stir-fry with tofu over brown rice          |
|           | Snack     | Hard-boiled eggs with salt and pepper                 |
| Wednesday | Breakfast | Scrambled eggs with spinach and tomatoes, whole-grain toast, apple slices |
|           | Lunch     | Grilled chicken salad with mixed greens, cherry tomatoes, cucumbers, vinaigrette |
|           | Dinner    | Baked salmon with steamed asparagus and quinoa        |
|           | Snack     | Apple slices with almond butter                       |
| Thursday  | Breakfast | Oatmeal with almond milk, sliced apples, cinnamon     |
|           | Lunch     | Quinoa bowl with chickpeas, roasted vegetables, lemon-tahini dressing |
|           | Dinner    | Grilled chicken breast with roasted sweet potatoes, green beans |
|           | Snack     | Carrot sticks with hummus                             |
| Friday    | Breakfast | Paneer and vegetable stir-fry with brown rice         |
|           | Lunch     | Tuna salad with lettuce, cherry tomatoes, olives, balsamic vinaigrette |
|           | Dinner    | Paneer tikka with brown rice, cucumber salad          |
|           | Snack     | Mixed nuts (almonds, walnuts, cashews)                |
| Saturday  | Breakfast | Avocado toast with poached egg, apple slices          |
|           | Lunch     | Stir-fried tofu with broccoli, carrots, jasmine rice  |
|           | Dinner    | Fish curry with basmati rice, sautéed spinach         |
|           | Snack     | Rice cakes with avocado, cherry tomatoes              |

## Customization

- Add new agents in `agents/inneragents/` for specialized tasks.
- Modify team logic in `teams/` for different orchestration strategies.
- Update model clients in `models/` to use other LLM providers.
