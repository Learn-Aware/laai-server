import os
from typing import Dict, List, Optional
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

from dotenv import load_dotenv

load_dotenv()


class GeminiAPI:

    def __init__(
        self,
        model: str = "learnlm-1.5-pro-experimental",
        tools: Optional[str] = None,
        safety_settings: Optional[Dict[HarmCategory, HarmBlockThreshold]] = None,
        #  tool_metadata: List[Dict] = None,
        use_tools: bool = False,
    ):

        self.api_key = os.environ["GEMINI_API_KEY"]
        self.genai = genai.configure(api_key=self.api_key)

        self.model = self.genai.GenerativeModel(model)

    def generate_completion():
        response = model.generate_content("How does AI work?")
        print(response.text)
