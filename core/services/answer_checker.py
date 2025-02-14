from core.prompt.check_answer import CheckAnswerPrompt
from core.utils.api_utils import APIUtils


class AnswerChecker:
    """
    Class to check if a user's answer is correct compared to the expected answer.
    """

    def __init__(self, model_name: str = "mistral-7b", api_type: str = "openrouter"):
        """
        Initialize the AnswerChecker with the specified model.
        """
        self.api_utils = APIUtils(model_name=model_name, api_type=api_type)

    def check_answer(self, question: str, expected_answer: str, user_answer: str):
        """
        Check if the user's answer is correct compared to the expected answer.
        """
        prompt = CheckAnswerPrompt.construct(question, expected_answer, user_answer)
        response = self.api_utils.generate_response(
            [{"role": "user", "content": prompt}]
        )
        return self.api_utils.parse_json_response(response)
