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

**Rules of Engagement:**

- Always follow the order: **Dietary_Needs_SOM → Meals_SOM → Summariser_Agent**.
- Interact with only **one agent at a time**.
- Once an agent returns `Task Status: Done`, go to the nect agent.
- While calling the summarising agent pass the input from the Dietary_Needs_SOMs and the Meals_SOM.
- Only after all three tasks are marked complete, present a consolidated summary to the user.Once Done end the Conversation with APPROVE

---


**Completion Criteria:**

Once all agents have completed their tasks:
- Present a summary of the collected information.
- Conclude the process with the keyword: **APPROVE**.

---

Inputs:
- Roles: {roles}
- Conversation history: {history}
- Participants/Agents: {participants}


"""
termination_condition = TextMentionTermination(text="TERMINATE") | MaxMessageTermination(max_messages=6)
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