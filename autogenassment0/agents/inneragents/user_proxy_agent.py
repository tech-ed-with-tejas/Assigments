from autogen_agentchat.agents import  UserProxyAgent

import streamlit as st
class TrackableUserProxyAgent(UserProxyAgent):
    def _process_received_message(self, message, sender, silent):
        with st.chat_message(sender.name):
            st.markdown(message)
        return super()._process_received_message(message, sender, silent)


def user_proxy_agent():
    user_proxy_agent = TrackableUserProxyAgent(
    name ='UserProxyageb',
    description='Agent that acts as a proxy for the user, providing input and feedback to other agents.',
    input_func=input
)

    return user_proxy_agent