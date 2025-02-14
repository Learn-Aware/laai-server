from typing import Dict, List
from models.model_registry import ModelRegistry
import json
from core.llm_services.llm_factory import LLMFactory


class APIUtils:
    """
    Utility class for interacting with different LLM APIs.
    """

    def __init__(
        self,
        model_name: str = None,
        api_type: str = None,
        tool_metadata: Dict = None,
        use_tools: bool = False,
    ):
        """
        Initialize APIUtils for a specific model.
        """

        self.api_type = api_type
        self.tool_metadata = tool_metadata
        self.use_tools = use_tools
        self.model_name = model_name
        self.model_config = (
            ModelRegistry.get_model_config(model_name)
            if self.api_type == "openrouter"
            else None
        )

    def generate_response(
        self,
        messages: List[Dict],
    ) -> str:
        """
        Call the LLM API to get a response for the given prompt.
        """
        # response = openai.ChatCompletion.create(
        #     model=self.model_config["name"],
        #     messages=[{"role": "user", "content": prompt}]
        # )
        llm = LLMFactory.get_llm(
            api_type=self.api_type,
            config=self.model_config if self.api_type == "openrouter" else None,
            model=self.model_name,
            tool_metadata=self.tool_metadata,
            use_tools=self.use_tools,
        )
        response = llm.generate_completion(messages=messages)
        return response

    @staticmethod
    def parse_json_response(response: str) -> Dict:
        """
        Extract and parse the JSON from the response.
        """
        try:
            start_index = response.find("{")
            end_index = response.rfind("}") + 1
            json_text = response[start_index:end_index]
            return json.loads(json_text)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON: {e}")
