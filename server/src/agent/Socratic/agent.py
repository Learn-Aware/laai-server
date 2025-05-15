# from google.adk.agents import Agent
# from google.adk.tools import FunctionTool
import os
import google.generativeai as genai
from dotenv import load_dotenv
from .prompt import SOCRATIC_PROMPT_V0




async def socratic_agent():

    load_dotenv()
    api_key = os.environ["GEMINI_API_KEY"]
    print(f"API Key: {api_key}")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(
            "learnlm-1.5-pro-experimental", system_instruction=SOCRATIC_PROMPT_V0
        )
    return model

# root_agent = Agent(
#     model="learnlm-1.5-pro-experimental",
#     name="socratic_agent",
#     instruction=SOCRATIC_PROMPT_V0,
    # tools=[
    #     FunctionTool(
    #         func=search,
    #     ),
    #     FunctionTool(
    #         func=click,
    #     ),
    # ],
# )