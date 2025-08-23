import streamlit as st
import asyncio
import os
from teams.outerteams.meal_plan_generator import meal_plan_generator
from models.open_ai_model_client import get_model_client
from autogen_agentchat.messages import TextMessage


st.title('MEAL PLAN GENERATOR') 
openai_model_client = get_model_client()

if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'autogen_team_state' not in st.session_state:
    st.session_state.autogen_team_state = None


task = st.chat_input("Enter your  weight loass goal and basic daily activity goal and any preference We can design you a meal plan")


async def run_analyser_gpt(openai_model_client,task):
    try:
        # await start_docker_container(docker)
        team =  meal_plan_generator(openai_model_client)

        if st.session_state.autogen_team_state is not None:
            await team.load_state(st.session_state.autogen_team_state)

        async for message in team.run_stream(task=task):
            print(message)
            print(message.source,"_---------__-----")
            if isinstance(message,TextMessage):
                if message.source.startswith('user'):
                    with st.chat_message('user',avatar='👤'):
                        st.markdown(message.content)

                elif message.source.startswith('UserProxyageb'):
                    with st.chat_message('user',avatar  ='👤'):
                        inputs = st.chat_input("Enter your  weight loass goal and basic daily activity goal and any preference We can design you a meal plan")

                        st.markdown(inputs)
                    st.session_state.messages.append(inputs)
                    
                else:
                     with st.chat_message('Plan Gnerator Analyzer',avatar='🤖'):
                        st.markdown(message.content)

           
                st.session_state.messages.append(message.content)
                # st.markdown(f"{message.content}")
            else: # isinstance(message,TaskResult):
                st.markdown(f'Stop Reason :{message.stop_reason}')

                st.session_state.messages.append(message.stop_reason)

        st.session_state.autogen_team_state = await team.save_state()
            
        return None
    except Exception as e:
        st.error(f"Error: {e}")
        return e
    finally:   
        pass


async def do_something_big():
    await asyncio.sleep(1)  # Simulate a long-running task

if st.session_state.messages:
    for msg in st.session_state.messages:
        st.markdown(msg)

if task:
   

        error = asyncio.run(run_analyser_gpt(openai_model_client,task))

        if error:
            st.error(f'An error occured: {error}')

     


else:
    st.warning('Please provide the task')