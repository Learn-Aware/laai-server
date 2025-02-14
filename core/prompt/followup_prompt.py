class FollowUpPrompt:
    """
    Class for constructing the follow-up question generation prompt.
    """

    @staticmethod
    def construct(student_question: str, max_questions: int = 10) -> str:
        """
        Construct the prompt for generating follow-up questions.
        """
        return (
            f"You are a Socratic tutor. This is the student question: '{student_question}'.\n"
            f"Please generate **an appropriate number of follow-up questions**, each with an expected answer, "
            f"to guide the student to the correct answer.\n"
            f"Only generate the number of questions and answers that are necessary, up to a maximum of {max_questions}.\n"
            f"If fewer questions are sufficient, stop at the appropriate point.\n\n"
            f"Output the follow-up questions and their expected answers in **valid JSON format** like this:\n\n"
            f"{{\n"
            f'    "questions_and_answers": [\n'
            f'        {{"question": "What is the first step in solving the equation?",\n'
            f'          "answer": "Isolate the variable by subtracting 3 from both sides."}},\n'
            f'        {{"question": "Can you identify the terms?",\n'
            f'          "answer": "The terms are 2x and 3 on the left side of the equation."}},\n'
            f"        ...\n"
            f"    ]\n"
            f"}}\n\n"
            f"Ensure the output is **valid JSON**, not truncated, and contains an appropriate number of questions "
            f"and their corresponding expected answers, based on the complexity of the student's question."
        )
