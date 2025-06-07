# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Academic_websearch_agent for finding research papers using search tools."""

import json
import logging

from fastapi import HTTPException

from google.adk import Agent
from google.adk.tools import google_search
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

from .prompt import prompt_text, competitive_analysis_prompt_text

MODEL = "gemini-2.5-pro-preview-05-06"
APP_NAME = "CompanyWebSearchAgent"

logger = logging.getLogger(__name__)


def _clean_json_from_text(text: str) -> str:
    """Extracts a JSON string from a text that might contain markdown code fences."""
    # Find the start of the JSON object
    json_start_index = text.find("{")
    if json_start_index == -1:
        return text  # No json object found

    # Find the end of the JSON object
    json_end_index = text.rfind("}")
    if json_end_index == -1:
        return text  # No json object found

    return text[json_start_index : json_end_index + 1]


class CompanyWebSearchAgent:
    def __init__(self):
        self.prompt = competitive_analysis_prompt_text
        self.agent = Agent(
            model=MODEL,
            name="company_websearch_agent",
            instruction=self.prompt,
            tools=[google_search],
        )

        self.session_service = InMemorySessionService()
        self.runner = Runner(
            agent=self.agent,
            app_name=APP_NAME,
            session_service=self.session_service,
        )

    async def call_agent(self, company_url: str, user_id, session_id):
        prompt = f"""Identify and research the key competitors of the company at **{company_url}** and compile a detailed profile for each competitor, including:
- Competitor name and website URL  
- Founding date and headquarters  
- Core products or service lines  
- Key metrics (e.g., revenue, employee count, market share)  
- Market segments and geographic footprint  
- Unique value propositions and positioning in the industry  
- Recent developments (e.g., mergers, funding rounds, major product launches)  
Provide citations for all factual data pulled from websites or other credible sources.
"""

        await self.session_service.create_session(
            app_name=APP_NAME, user_id=user_id, session_id=session_id
        )

        content = types.Content(parts=[types.Part(text=prompt)], role="user")
        try:
            async for event in self.runner.run_async(
                user_id=user_id, session_id=session_id, new_message=content
            ):
                is_final = event.is_final_response()
                # logger.info(
                #     "[Event] Author: %s, Type: %s, Final: %s, Content: %s",
                #     event.author,
                #     type(event).__name__,
                #     is_final,
                #     event.content,
                # )
            if is_final:
                logger.info(event.content.model_dump_json())
                if event.content and event.content.parts:
                    raw_json = event.content.parts[0].text
                    try:
                        cleaned_json = _clean_json_from_text(raw_json)
                        logger.info("Validating JSON against schema")
                        # Directly validate the JSON against the Pydantic schema
                        return json.loads(cleaned_json)
                    except Exception as e:
                        logger.error(
                            f"Error validating JSON against schema: {e}", exc_info=True
                        )
                        # You might want to return the raw_json even on validation error for debugging
                        return raw_json
                if event.actions and event.actions.escalate:
                    raise HTTPException(
                        status_code=500,
                        detail=f"Error escalating: {event.actions.escalate}",
                    ) from event.error_message
        except Exception as e:
            error_message = (
                f"Error calling agent: {e}"
                if hasattr(e, "error_message")
                else f"Error calling agent: {e}"
            )
            logger.exception(error_message)
            raise HTTPException(status_code=500, detail=error_message) from e
        finally:
            await self.session_service.delete_session(
                app_name=APP_NAME, user_id=user_id, session_id=session_id
            )
