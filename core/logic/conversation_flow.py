from http.client import HTTPException
import uuid
import json
from mistralai import Optional

from core.utils.api_utils import APIUtils
from core.logic.socratic_tutor_logic import start_tutoring_session, submit_tutor_answer
from schemas.socratic_tutor_schemas import QuestionResponse

socratic_tutor_description = "Act as a Socratic tutor"

socratic_tutor_properties = {
    "student_question": {
        "type": "string",
        "description": "Student question which is need to be acted as a Socratic tutor",
    }
}

tool_metadata = [
    {
        "type": "function",
        "function": {
            "name": "socratic_tutor",
            "description": socratic_tutor_description,
            "parameters": {
                "type": "object",
                "properties": socratic_tutor_properties,
                "required": ["student_question"],
            },
        },
    },
]

system_prompt = (
    "You are an Educational Tutor called LAAI. You must either call "
    "tools (socratic_tutor) or write a response to the user. Do not take the same actions "
    "multiple times! When a student asks a math-related question, always call the "
    "Socratic_tutor tool."
)


def save_session_data(session_file, sessions):
    with open(session_file, "w") as f:
        json.dump(sessions, f)


def main_chat_flow(
    user_request: str, session_file: str, session_id: Optional[str] = None
):
    with open(session_file, "r") as f:
        sessions = json.load(f)

    if session_id and session_id in sessions:
        session_data = sessions[session_id]
        flow_status = session_data["flow_status"]
    else:
        session_id = str(uuid.uuid4())
        sessions[session_id] = {"flow_status": "general"}
        session_data = sessions[session_id]
        flow_status = "general"

    if "conversation_flow" not in session_data:
        session_data["conversation_flow"] = []

    session_data["conversation_flow"].append({"role": "user", "content": user_request})

    save_session_data(session_file, sessions)

    if flow_status == "general":
        messages = [{"role": "system", "content": system_prompt}]
        messages.append({"role": "user", "content": user_request})

        model_name = "mistral-large-latest"
        api_type = "mistral"
        api_utils = APIUtils(
            model_name=model_name,
            api_type=api_type,
            tool_metadata=tool_metadata,
            use_tools=True,
        )

        response = api_utils.generate_response(messages=messages)

        if response.message.tool_calls:

            tool_call = response.message.tool_calls[0]
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            if tool_name == "socratic_tutor":
                session_response = start_tutoring_session(
                    arguments["student_question"], sessions, session_id
                )
                first_question = session_response.question
                flow_status = "socratic"

                sessions[session_id]["flow_status"] = flow_status
                session_data["conversation_flow"].append(
                    {"role": "assistant", "content": first_question}
                )
                save_session_data(session_file, sessions)

                return QuestionResponse(
                    session_id=session_id,
                    question=first_question,
                )
            else:
                raise HTTPException(
                    status_code=400, detail=f"Unknown tool called: {tool_name}"
                )
        else:
            session_data["conversation_flow"].append(
                {"role": "assistant", "content": response.message.content}
            )
            save_session_data(session_file, sessions)

            return QuestionResponse(
                session_id=session_id, question=response.message.content
            )
    elif flow_status == "socratic":
        response = submit_tutor_answer(user_request, sessions, session_id)

        if response.correct and response.question == "Session complete!":
            flow_status = "general"
            sessions[session_id]["flow_status"] = flow_status
            session_data["conversation_flow"].append(
                {
                    "role": "assistant",
                    "content": "Nice! you successfully understand the problem, Do you have anything to ask?",
                }
            )
            save_session_data(session_file, sessions)

            return QuestionResponse(
                session_id=session_id,
                question="Nice! you successfully understand the problem, Do you have anything to ask?",
                correct=True,
            )
        else:

            session_data["conversation_flow"].append(
                {"role": "assistant", "content": response.question}
            )
            save_session_data(session_file, sessions)

            return QuestionResponse(
                session_id=session_id,
                question=response.question,
                correct=response.correct,
                guidance=response.guidance,
            )
    else:
        raise ValueError("Invalid flow status.")
