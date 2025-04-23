import os
from typing import Dict, List
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()


class MistralAPI:
    """
    Implementation of the Mistral API.
    """

    def __init__(
        self,
        model: str = "mistral-large-latest",
        tool_metadata: List[Dict] = None,
        use_tools: bool = False,
    ):

        self.api_key = os.environ["MISTRAL_API_KEY"]
        self.client = Mistral(api_key=self.api_key)

        self.model = model

        # Tool metadata (can be empty if no tools are used)
        self.tool_metadata = tool_metadata or []

        # Flag to control tool usage
        self.use_tools = use_tools

    def generate_completion(
        self,
        messages: List[Dict],
        tool_choice: str = "auto",
        response_format: Dict = None,
    ) -> str:

        # Prepare the chat completion request
        chat_response = self.client.chat.complete(
            model=self.model,
            messages=messages,
            tools=self.tool_metadata if self.use_tools else None,
            tool_choice=tool_choice,
            response_format=response_format,
        )

        # Return the generated content
        return chat_response.choices[0]
