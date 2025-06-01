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

""" Angent to Extract PDF Data """
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Part, Blob, Content, GenerateContentConfig

from fastapi import UploadFile

from . import prompt
import logging

logger = logging.getLogger(__name__)

MODEL = "gemini-2.5-flash-preview-05-20" 

root_agent = Agent(
    name="pdf_extractor",
    model=MODEL,
    description=(
        "Extract text from a PDF file"
    ),
    instruction=prompt.PDF_EXTRACTOR_PROMPT,
    generate_content_config=GenerateContentConfig(
        response_mime_type="application/json"
    )
)



class PDFExtractorAgent:
    def __init__(self):
        self.agent = root_agent
        self.session_service = InMemorySessionService()
        self.runner = InMemoryRunner(self.agent, app_name="PDFExtractorAgent")

    @staticmethod
    def _get_file_content(file: UploadFile) -> Part:
        contents = file.file.read()
        mime_type = file.content_type
        return Part(inline_data=Blob(contents=contents, mime_type=mime_type))

    async def call_agent(self, file: UploadFile, user_id, session_id) -> str:
        file_content = self._get_file_content(file)

        content = Content(parts=[file_content], role="user")
        try:
            async for event in self.runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=content
            ):
                is_final = event.is_final_response()
                logger.info("[Event] Author: %s, Type: %s, Final: %s, Content: %s", 
                            event.author, 
                            type(event).__name__, 
                            is_final, 
                            event.content)
                if is_final:
                    return event.content.parts[0].text
        except Exception as e:
            logger.error(f"Error calling agent: {e}")
