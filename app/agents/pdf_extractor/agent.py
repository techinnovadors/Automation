"""Angent to Extract PDF Data"""

import logging
import json
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Part, Blob, Content, GenerateContentConfig

from fastapi import UploadFile, HTTPException

from app.services.pdf_processor import process_uploaded_pdf

from .prompt import PDF_EXTRACTOR_DESCRIPTION
from .models import FinancialAnalysisSchema

logger = logging.getLogger(__name__)

MODEL = "gemini-2.5-flash-preview-05-20"

APP_NAME = "PDFExtractorAgent"


class PDFExtractorAgent:
    def __init__(self, prompt: str):
        root_agent = Agent(
            name="pdf_extractor",
            model=MODEL,
            description=PDF_EXTRACTOR_DESCRIPTION,
            instruction=prompt,
            generate_content_config=GenerateContentConfig(
                response_mime_type="application/json",
            ),
        )

        self.session_service = InMemorySessionService()

        self.runner = Runner(
            agent=root_agent,
            app_name=APP_NAME,
            session_service=self.session_service,
        )

    @staticmethod
    def _get_file_content(file: UploadFile) -> Part:
        contents = file.file.read()
        mime_type = file.content_type
        return Part(inline_data=Blob(data=contents, mime_type=mime_type))

    async def call_agent(
        self, file: UploadFile, user_id, session_id, is_rich_text: bool = False
    ):
        if is_rich_text:
            file_content = self._get_file_content(file)
        else:
            text = await process_uploaded_pdf(file)
            file_content = Part(text=text)

        await self.session_service.create_session(
            app_name=APP_NAME, user_id=user_id, session_id=session_id
        )

        content = Content(parts=[file_content], role="user")
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
                if event.content and event.content.parts:
                    raw_json = event.content.parts[0].text
                    try:
                        logger.info("Validating JSON against schema")
                        # Directly validate the JSON against the Pydantic schema
                        data = FinancialAnalysisSchema.model_validate_json(raw_json)
                        if data.financial_analysis:
                            return data
                        else:
                            return json.loads(raw_json)
                    except (
                        Exception
                    ) as e:  # Catch Pydantic's ValidationError specifically or a broader Exception
                        logger.error(
                            f"Error validating JSON against schema: {e}", exc_info=True
                        )
                        # You might want to return the raw_json even on validation error for debugging
                        return json.loads(raw_json)
                elif event.actions and event.actions.escalate:
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
