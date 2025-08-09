import asyncio
from autogen_agentchat.ui import Console
from autogen_agentchat.agents import AssistantAgent, SocietyOfMindAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
import os 
from pathlib import Path 
from dotenv import load_dotenv
current_script_dir = Path().parent
dotenv_file_path = Path.cwd().parent  / '.env'
dotenv_file_path = dotenv_file_path.resolve()
load_dotenv(dotenv_path=dotenv_file_path)
api_key = os.getenv('OPENAI_API_KEY')

async def main() -> None:
    model_client = OpenAIChatCompletionClient(model='gpt-4o', api_key=api_key)

    agent1 = AssistantAgent("assistant1", model_client=model_client, system_message="You are a writer, write well.")
    agent2 = AssistantAgent(
        "assistant2",
        model_client=model_client,
        system_message="You are an editor, provide critical feedback. Respond with 'APPROVE' if the text addresses all feedbacks.",
    )
    inner_termination = TextMentionTermination("APPROVE")
    inner_team = RoundRobinGroupChat([agent1, agent2], termination_condition=inner_termination)

    society_of_mind_agent = SocietyOfMindAgent("society_of_mind", team=inner_team, model_client=model_client)

    agent3 = AssistantAgent(
        "assistant3", model_client=model_client, system_message="Translate the text to Spanish."
    )
    team = RoundRobinGroupChat([society_of_mind_agent, agent3], max_turns=2)

    stream = team.run_stream(task="Write a short story with a surprising ending.")
    await Console(stream)


asyncio.run(main())
