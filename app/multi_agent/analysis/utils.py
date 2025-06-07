import os
import json
import logging
import re
from typing import Optional, Dict, Any

from google.adk import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

logger = logging.getLogger(__name__)

APP_NAME = "MultiAgentCompetitiveAnalysis"
MODEL = "gemini-2.5-flash-preview-05-20"
MAX_CONCURRENT_PROFILES = 2


def save_json_to_file(data: Any, filename: str, output_dir: str):
    """Saves serializable data to a JSON file in a specified directory."""
    try:
        os.makedirs(output_dir, exist_ok=True)

        # Sanitize filename to be safe for file paths
        safe_filename = "".join(
            c for c in filename if c.isalnum() or c in ("_", "-", ".")
        ).rstrip()
        file_path = os.path.join(output_dir, safe_filename)

        def convert_to_dict(obj: Any) -> Any:
            """Recursively convert Pydantic models to dicts."""
            if hasattr(obj, "model_dump"):
                return obj.model_dump()
            if isinstance(obj, list):
                return [convert_to_dict(i) for i in obj]
            if isinstance(obj, dict):
                return {k: convert_to_dict(v) for k, v in obj.items()}
            return obj

        data_to_save = convert_to_dict(data)

        with open(file_path, "w") as f:
            json.dump(data_to_save, f, indent=4)
        logger.info(f"Saved data to {file_path}")
    except Exception as e:
        logger.error(
            f"Failed to save '{filename}' to JSON in '{output_dir}': {e}",
            exc_info=True,
        )


def clean_json_from_text(text: str) -> str:
    """
    Extracts a JSON string from a text that might contain markdown code fences.
    Handles both JSON objects ({...}) and JSON arrays ([...]).
    """
    json_start_index = text.find("{")
    array_start_index = text.find("[")

    # Determine the actual start index
    if json_start_index == -1 and array_start_index == -1:
        return text  # No JSON object or array found
    elif json_start_index == -1:  # Only array found
        start_index = array_start_index
    elif array_start_index == -1:  # Only JSON object found
        start_index = json_start_index
    else:  # Both found, pick the earliest one
        start_index = min(json_start_index, array_start_index)

    json_end_index = text.rfind("}")
    array_end_index = text.rfind("]")

    # Determine the actual end index
    if json_end_index == -1 and array_end_index == -1:
        return text  # No JSON object or array end found
    elif json_end_index == -1:  # Only array end found
        end_index = array_end_index
    elif array_end_index == -1:  # Only JSON object end found
        end_index = json_end_index
    else:  # Both found, pick the latest one
        end_index = max(json_end_index, array_end_index)

    return text[start_index : end_index + 1]


# def remove_markdown_code_fences(text: str) -> str:
#     """
#     Removes markdown code fences like ```json ... ``` or ``` ... ``` from a text.
#     Returns the raw inner content.
#     """
#     # Match fenced code blocks (optionally with a language tag)
#     pattern = r"```(?:json|JSON)?\s*([\s\S]*?)\s*```"
#     match = re.search(pattern, text, re.IGNORECASE)

#     if match:
#         return match.group(1).strip()  # Return the content inside the code block

#     return text.strip()  # If no match, return as-is (stripped)


async def call_single_agent(
    agent_instance: Agent,
    user_id: str,
    session_id: str,
    prompt_text: str,
    input_data: Optional[Dict[str, Any]] = None,
) -> Any:
    """
    Helper function to call a single agent, manage its session, and parse its JSON output.
    """
    logger.info(f"Calling agent '{agent_instance.name}'")
    session_service = InMemorySessionService()

    runner = Runner(
        agent=agent_instance, app_name=APP_NAME, session_service=session_service
    )

    full_prompt = prompt_text
    if input_data:
        # Embed input_data as JSON for the agent to process
        full_prompt += f"\n\nHere is the input data:\n```json\n{json.dumps(input_data, indent=2)}\n```"

    content = types.Content(parts=[types.Part(text=full_prompt)], role="user")
    raw_response = ""
    try:
        await session_service.create_session(
            app_name=APP_NAME, user_id=user_id, session_id=session_id
        )
        async for event in runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content
        ):
            # Check for final response containing content
            if event.is_final_response() and event.content and event.content.parts:
                raw_response = event.content.parts[0].text
                break
            # Handle potential agent escalations (errors)
            elif event.actions and event.actions.escalate:
                logger.error(
                    f"Agent '{agent_instance.name}' escalation: {event.actions.escalate}"
                )
                raise Exception(
                    f"Agent '{agent_instance.name}' escalation: {event.actions.escalate}"
                )
    except Exception as e:
        logger.error(f"Error running agent '{agent_instance.name}': {e}", exc_info=True)
        raise  # Re-raise the exception after logging
    finally:
        # Ensure the session is always deleted
        await session_service.delete_session(
            app_name=APP_NAME, user_id=user_id, session_id=session_id
        )

    if not raw_response:
        raise Exception(f"Agent '{agent_instance.name}' returned no content.")

    try:
        cleaned_json_str = clean_json_from_text(raw_response)
        if not cleaned_json_str:
            raise ValueError(f"Could not extract JSON from response: {raw_response}")

        return json.loads(cleaned_json_str)
    except json.JSONDecodeError as e:
        logger.error(
            f"JSON decode error from agent '{agent_instance.name}' response: {e}\nRaw response: {raw_response}",
            exc_info=True,
        )
        raise ValueError(
            f"Invalid JSON response from agent '{agent_instance.name}'. Raw: {raw_response}"
        ) from e
    except ValueError as e:
        logger.error(
            f"Validation error from agent '{agent_instance.name}' response: {e}\nRaw response: {raw_response}",
            exc_info=True,
        )
        raise
