import logging
import json
from google import genai
from google.genai.types import (
    GenerateContentConfig,
    UploadFileConfig,
    ContentListUnion,
    ContentListUnionDict,
)
from google.genai.errors import ServerError, ClientError, APIError

from app.core.config import settings
from app.services.models import GeminiRequestParams, GeminiResponseParams

logger = logging.getLogger(__name__)


class GoogleProviderClient:
    def __init__(self):
        logger.info("Initializing GoogleProviderClient")
        self.client = genai.Client(api_key=settings.GOOGLE_API_KEY)
        logger.info("GoogleProviderClient initialized successfully")

    def _handle_error(self, e: Exception, error_message: str) -> GeminiResponseParams:
        logger.exception(f"Error occurred: {e}", exc_info=True)
        logger.error(f"Error message: {error_message}")
        return GeminiResponseParams(
            is_error=True,
            error_message=error_message,
            provider_response=error_message,
            response=None,
        )

    def _get_config(self, req: GeminiRequestParams) -> GenerateContentConfig:
        logger.debug(f"Creating config with system prompt: {req.system_prompt}")
        config = GenerateContentConfig(
            system_instruction=req.system_prompt,
            temperature=0.1,
        )
        if req.is_json:
            logger.debug("Setting response MIME type to application/json")
            config.response_mime_type = "application/json"
        return config

    def _get_contents(
        self, req: GeminiRequestParams
    ) -> ContentListUnion | ContentListUnionDict:
        if req.file:
            logger.info(f"Processing file with content type: {req.file.content_type}")
            file_config = UploadFileConfig(mime_type=req.file.content_type)
            file_to_process = self.client.files.upload(
                file=req.file.file, config=file_config
            )
            logger.info("File uploaded successfully")
            return [req.user_prompt, file_to_process]
        logger.debug("No file provided, using only user prompt")
        return [req.user_prompt]

    async def generate_content(self, req: GeminiRequestParams) -> GeminiResponseParams:
        logger.info(f"Generating content with model: {req.model}")
        logger.debug(f"User prompt: {req.user_prompt}")

        try:
            logger.debug("Preparing request configuration")
            config = self._get_config(req)
            contents = self._get_contents(req)

            logger.info("Sending request to Google AI model")
            response = await self.client.aio.models.generate_content(
                model=req.model,
                contents=contents,
                config=config,
            )

            logger.info(f"Response received successfully")
            logger.debug(f"Response text: {response.text}")
            logger.info(f"Usage metadata: {response.usage_metadata}")
            provider_response = response if req.pass_provider_response else None

            if req.is_json:
                logger.debug("Processing JSON response")
                try:
                    response_json = json.loads(response.text)
                    logger.info("Successfully parsed JSON response")
                    return GeminiResponseParams(
                        response=response_json,
                        is_error=False,
                        error_message="",
                        provider_response=provider_response,
                    )
                except json.JSONDecodeError as e:
                    logger.error(f"JSON parsing error: {e}")
                    return self._handle_error(e, "Error converting response to JSON")
                except Exception as e:
                    logger.error(f"Unexpected error during JSON processing: {e}")
                    return self._handle_error(e, "Error converting response to JSON")
            else:
                logger.info("Returning text response")
                return GeminiResponseParams(
                    response=response.text,
                    is_error=False,
                    error_message="",
                    provider_response=provider_response,
                )

        except ClientError as e:
            logger.error(f"Client error occurred: {e}")
            message = f"Client error: {e}"
            if e.code == 429:
                message = "Rate limit exceeded"
                logger.warning("Rate limit exceeded")
            return self._handle_error(e, message)
        except ServerError as e:
            logger.error(f"Server error occurred: {e}")
            return self._handle_error(e, "Server error")
        except APIError as e:
            logger.error(f"API error occurred: {e}")
            return self._handle_error(e, "API error")
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}")
            return self._handle_error(e, "Unknown error")


async def call_google_provider(req: GeminiRequestParams) -> GeminiResponseParams:
    logger.info("Calling Google provider")
    google_provider = GoogleProviderClient()
    response = await google_provider.generate_content(req)
    logger.info("Google provider call completed")
    return response
