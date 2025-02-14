class TutorGuidanceGeneratorPrompt:
    """
    Class for constructing the tutor question generator prompt.
    """

    @staticmethod
    def construct(correct_answer: str, student_answer: str) -> str:
        """
        Construct the prompt for generating step-by-step guidance.
        """
        return f"""
            The correct answer is: '{correct_answer}'. The student's answer is: '{student_answer}', which is incorrect.

            Based on the student's answer and its correctness, provide steps to guide them to the correct answer.

            Use a friendly, encouraging tone in your responses. Make sure to keep your response short and clear.
            """
