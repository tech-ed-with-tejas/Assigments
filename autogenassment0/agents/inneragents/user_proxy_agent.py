from autogen_agentchat.agents import  UserProxyAgent


def user_proxy_agent():
    user_proxy_agent = UserProxyAgent(
    name ='UserProxyageb',
    description='Agent that acts as a proxy for the user, providing input and feedback to other agents.',
    input_func=input
)

    return user_proxy_agent