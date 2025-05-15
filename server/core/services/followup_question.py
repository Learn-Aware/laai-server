from core.utils.api_utils import APIUtils
from core.prompt.followup_prompt import FollowUpPrompt


class FollowUpQuestionGenerator:
    """
    Main class for generating follow-up questions.
    """

    def __init__(self, model_name: str = "gemini", api_type: str = "openrouter"):
        """
        Initialize the FollowUpQuestionGenerator with a model.
        :param model_name: The name of the model to use (default: gemini).
        """
        self.api_utils = APIUtils(model_name=model_name, api_type=api_type)

    def generate(self, student_question: str, max_questions: int = 10):
        """
        Generate follow-up questions for a given student question.
        """
        # Step 1: Construct the prompt
        prompt = FollowUpPrompt.construct(student_question, max_questions)

        # Step 2: Get the response from the selected model
        response = self.api_utils.generate_response(
            [{"role": "user", "content": prompt}]
        )

        print(response)
        # Step 3: Parse the response into JSON
        return self.api_utils.parse_json_response(response)
