import os
from dotenv import load_dotenv

from src.agent.Socratic.prompt import SOCRATIC_PROMPT_V0
from .Socratic.agent import socratic_agent
from google import genai
class AgentService:
    async def generate_response(self, conversation, topic_id: str, message: str) -> str:
        """
        Generate a response based on the provided prompt.
        """
        # agent = await socratic_agent()
        # response = await agent.generate_content([str(conversation["conversation"])]
        # )
        # return response.text
        # Placeholder for actual response generation logic
        # return f"This is sample llm response"

        load_dotenv()
        api_key = os.environ["GEMINI_API_KEY"]
        client = genai.Client(api_key=api_key)
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel(
                "learnlm-1.5-pro-experimental", system_instruction=SOCRATIC_PROMPT_V0
            )
        response = model.generate_content([str(conversation["conversation"])])

        return response.text