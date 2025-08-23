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
   streamlit run streamlit_app.py
   ```
   Or run the CLI:
   ```sh
   python main.py
   ```

## Customization

- Add new agents in `agents/inneragents/` for specialized tasks.
- Modify team logic in `teams/` for different orchestration strategies.
- Update model clients in `models/` to use other LLM providers.

