# from mistral_api import MistralAPI
from typing import List, Dict
from .mistral_api import MistralAPI


class LLMFactory:
    """
    Factory to create instances of different LLM APIs.
    """

    @staticmethod
    def get_llm(
        api_type: str,
        config: dict = None,
        model: str = "mistral-large-latest",
        tool_metadata: List[Dict] = None,
        use_tools: bool = False,
    ):
        """
        Return the appropriate LLM instance based on `api_type`.
        """
        print(api_type)
        if api_type == "mistral":
            print(api_type)
            return MistralAPI(
                model=model, tool_metadata=tool_metadata, use_tools=use_tools
            )
        else:
            raise ValueError(f"Unsupported API type: {api_type}")
