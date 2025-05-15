class TutorQuestionGeneratorPrompt:
    """
    Class for constructing the tutor question generator prompt.
    """

    @staticmethod
    def construct(question: str) -> str:
        """
        Construct the prompt for the LLM.
        """
        return f"""
            You are a helpful tutor. Ask the following question in a concise, teacher-like tone, encouraging them to think critically but keeping the question short:

            The question is: "{question}"

            Make sure the phrasing is supportive, but the question is brief and to the point.
        """
