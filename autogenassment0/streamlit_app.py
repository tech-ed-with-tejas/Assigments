import streamlit as st
import asyncio
import os
from teams.outerteams.meal_plan_generator import meal_plan_generator
from models.open_ai_model_client import get_model_client
from autogen_agentchat.messages import TextMessage,UserInputRequestedEvent


st.title('MEAL PLAN GENERATOR') 

@st.cache_resource
def load_team():
     openai_model_client = get_model_client()
     team =  meal_plan_generator(openai_model_client)
     return team,openai_model_client
team,openai_model_client = load_team()








if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'autogen_team_state' not in st.session_state:
    st.session_state.autogen_team_state = None



if "pending_user_text" not in st.session_state:
    st.session_state.pending_user_text = None



if st.session_state.get('pending_user_text', None) is None:
    st.session_state.pending_user_text = None

if "pending_text" not in st.session_state:
    st.session_state.pending_text = None
if "awaiting_user_input" not in st.session_state:
    st.session_state.awaiting_user_input = False

st.write(st.session_state)
async def run_analyser_gpt(task,team):
    print("inside run analyser")
    try:
        
        

        if st.session_state.autogen_team_state is not None:
            await team.load_state(st.session_state.autogen_team_state)

        async for message in team.run_stream(task=task ):
            print(message)
            
            if isinstance(message,TextMessage):
                with st.chat_message('message',avatar='👤'):
                    st.markdown(message.content)
        
        
                st.session_state.messages.append(message.content)

            elif isinstance(message,UserInputRequestedEvent):

                with st.chat_message('user',avatar  ='👤'):

                    st.markdown(st.session_state.get('pending_user_text', "None"))
                st.session_state.messages.append(st.session_state.get('pending_user_text', "None"))
                print("hello")
                break
                # st.markdow    n(f"{message.content}")
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

state =  team.save_state()
import json
print(state)
async def do_something_big():
    await asyncio.sleep(1)  # Simulate a long-running task
# --- Input handling ---
if st.session_state.awaiting_user_input:
    followup = st.chat_input("Provide more details")
    if followup:
        st.session_state.pending_text = followup
        asyncio.run(run_analyser_gpt(task=None,team=team))
        st.session_state.autogen_team_state =  team.save_state()
        st.stop()
else:
    user_text = st.chat_input("Say something about ursefl")
    if user_text:
        asyncio.run(run_analyser_gpt(task=user_text,team=team))
        st.session_state.autogen_team_state =  team.save_state()
        st.stop()