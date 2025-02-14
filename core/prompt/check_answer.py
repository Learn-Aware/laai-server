class CheckAnswerPrompt:
    """
    Class for constructing the answer check prompt.
    """

    @staticmethod
    def construct(question: str, expected_answer: str, user_answer: str) -> str:
        """
        Construct the prompt for the LLM.
        """
        return f"""
            You are an AI that checks answers for correctness.

            - The question is: "{question}"
            - The expected answer is: "{expected_answer}"
            - The user's answer is: "{user_answer}"

            Based on the user's answer compared to the expected answer, determine if the user's answer is **correct** or **incorrect**.

            Output only in valid JSON format like this:

            {{
                "result": "correct"  # or "incorrect"
            }}
            """
