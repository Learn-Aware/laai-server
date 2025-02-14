from typing import Dict, List
import openai
from dotenv import load_dotenv
import os

load_dotenv()

openrouter_api_key = os.environ["OPENROUTER_API_KEY"]

class OpenRouterAPI():
    """
    Implementation of the OpenAI API.
    """

    def __init__(self, model_name: str):
        self.api_key = openrouter_api_key
        self.base_url = "https://openrouter.ai/api/v1"
        self.model_name = model_name

        openai.api_key = self.api_key
        openai.api_base = self.base_url

    def generate_completion(self, messages: List[Dict]) -> str:
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=messages
        )
        return response.choices[0].message.content
