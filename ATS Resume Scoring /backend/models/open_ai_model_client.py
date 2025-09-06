from autogen_ext.models.openai import OpenAIChatCompletionClient
import os
from dotenv import load_dotenv
from autogen_core.models import ModelInfo

load_dotenv()

# def get_model_client():
#     openai_model_client = OpenAIChatCompletionClient(
#         model="gpt-4o",
#         api_key=os.getenv('OPENAI_API_KEY'),
#         temperature=0.1,
#     )

#     return openai_model_client

from autogen_ext.models.openai import OpenAIChatCompletionClient

def get_model_client():
    """
    Returns a Gemini model client configured with the specified model and API key.
    """
    
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o",
        api_key=os.getenv('OPENAI_API_KEY'),
        temperature =0.1
    )

#     model_client = OpenAIChatCompletionClient(
#     model="gemini-2.5-pro",
#      api_key=os.getenv('GOOGLE_API_KEY'),
#          model_info=ModelInfo(vision=True, function_calling=True, json_output=True, family="unknown", structured_output=True),

#         temperature =0.1
# )
    return model_client

