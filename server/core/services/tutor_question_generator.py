from core.prompt.tutor_question_generator import TutorQuestionGeneratorPrompt
from core.utils.api_utils import APIUtils


class TutorQuestionGenerator:
    """
    Class to generate questions in a tutor-like tone.
    """

    def __init__(self, model_name: str = "phi3-mini", api_type: str = "openrouter"):
        """
        Initialize the TutorQuestionGenerator with a specific model.
        :param model_name: The name of the model to use for generating questions.
        """
        self.api_utils = APIUtils(model_name=model_name, api_type=api_type)

    def ask_question(self, question: str) -> str:
        """
        Generate a question in a concise, tutor-like tone.

        """
        prompt = TutorQuestionGeneratorPrompt.construct(question)
        response = self.api_utils.generate_response(
            [{"role": "user", "content": prompt}]
        )
        return response.message.content.strip()
