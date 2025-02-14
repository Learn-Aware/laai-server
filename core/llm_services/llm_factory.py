# from mistral_api import MistralAPI
from typing import List, Dict
from .mistral_api import MistralAPI
from .openrouter_api import OpenRouterAPI

class LLMFactory:
    """
    Factory to create instances of different LLM APIs.
    """

    @staticmethod
    def get_llm(api_type: str, 
                config: dict = None,
                model: str = "mistral-large-latest", 
                tool_metadata: List[Dict] = None,
                use_tools: bool = False):
        """
        Return the appropriate LLM instance based on `api_type`.
        """
        print(api_type)
        if api_type == "mistral":
            print(api_type)
            return MistralAPI(model = model,
                              tool_metadata=tool_metadata, 
                              use_tools=use_tools)
        elif api_type == "openrouter":
            if not config or "name" not in config:
                raise ValueError("OpenAI requires a configuration dictionary.")
            return OpenRouterAPI(
                model_name=config["name"]
            )
        else:
            raise ValueError(f"Unsupported API type: {api_type}")
