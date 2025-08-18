from autogen_agentchat.teams import  RoundRobinGroupChat, SelectorGroupChat
from autogen_agentchat.messages import BaseAgentEvent, BaseChatMessage

from autogen_agentchat.conditions import TextMentionTermination,MaxMessageTermination
from agents.inneragents.ActivityAgent import activity_agent
from agents.inneragents.GoalAgent import goal_agent
from agents.inneragents.PreferenceAgent import preference_agent
from agents.inneragents.user_proxy_agent import user_proxy_agent
combined_termination = TextMentionTermination(text="APPROVE") | MaxMessageTermination(max_messages=10)
from typing import Sequence

SELECTOR_PRMPT = """
You are the Task Selector Agent, an orchestration layer for a nutritional planning system.

Your primary objective is to gather comprehensive information from the user to build a personalized nutrition plan. This process requires sequential interaction with specialized agents and the user.

**Execution Flow:**

1.  **Goal_Agent:** Determine the user's calorie target.
2.  **Activity_Agent:** Assess the user's activity level and exercise habits to adjust the calorie target.
3.  **Preference_Agent:** Collect the user's specific dietary type and any restrictions.

**Rules:**

* Follow the execution flow strictly: Goal → Activity → Preference.
* Engage with only **one agent at a time.**
* If an agent's response indicates `Task Status: Incomplete`,invoke the `UserProxyAgent` to request the required information from the user.(Call user agent if task status is incompletly only)
* Once an agent reports `Task Status: Done`, **do not call the same agent again.** .Move to the next agent in the loop.
* Present a summary of findings to the user for confirmation only after all three tasks are complete.

**Completion Criteria:**

When all three agents have completed their tasks, summarize the findings for the user and conclude with the final keyword: **APPROVE**.
Inputs:
- Roles: {roles}
- Conversation history: {history}
- Participants/Agents: {participants}

"""


def dietry_team(model_client):
    activity_agent_instance = activity_agent(model_client)
    goal_agent_instance = goal_agent(model_client)
    preference_agent_instance = preference_agent(model_client)
    user_proxy_agent_instance=user_proxy_agent()
    def selector_func_with_user_proxy(messages: Sequence[BaseAgentEvent | BaseChatMessage]) -> str | None:
        print(messages[-1].source, "hellow")
        if messages[-1].source != goal_agent_instance.name and messages[-1].source != user_proxy_agent_instance.name:
            # Planning agent should be the first to engage when given a new task, or check progress.
            return goal_agent_instance.name
        if messages[-1].source == goal_agent_instance.name:
            if messages[-2].source == user_proxy_agent_instance.name and "APPROVE" in messages[-1].content.upper():  # type: ignore
                # User has approved the plan, proceed to the next agent.
                return None
            # Use the user proxy agent to get the user's approval to proceed.
            return user_proxy_agent_instance.name
        if messages[-1].source == user_proxy_agent_instance.name:
            # If the user does not approve, return to the planning agent.
            if "APPROVE" not in messages[-1].content.upper():  # type: ignore
                return goal_agent_instance.name
        return None


    selector_team = SelectorGroupChat(
        participants=[goal_agent_instance,activity_agent_instance,preference_agent_instance,user_proxy_agent_instance],
        model_client=model_client,
        termination_condition=combined_termination,
        selector_prompt=SELECTOR_PRMPT,
        selector_func=selector_func_with_user_proxy,

        allow_repeated_speaker=False)
    
    return selector_team