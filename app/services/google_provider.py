import logging
import json
from google import genai
from google.genai.types import GenerateContentConfig, UploadFileConfig, ContentListUnion, ContentListUnionDict
from google.genai.errors import ServerError, ClientError, APIError

from app.core.config import settings
from app.services.models import GeminiRequestParams, GeminiResponseParams

logger = logging.getLogger("uvicorn")

class GoogleProviderClient:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GOOGLE_API_KEY)

    def _handle_error(self, e: Exception, error_message: str) -> GeminiResponseParams:
        logger.exception(f"Error: {e}", exc_info=True)
        return GeminiResponseParams(
            is_error=True,
            error_message=error_message,
            provider_response=error_message,
            response=None
        )

    def _get_config(self, req: GeminiRequestParams) -> GenerateContentConfig:
        config = GenerateContentConfig(
            system_instruction=req.system_prompt,
            temperature=0.1,
        )
        if req.is_json:
            config.response_mime_type = "application/json"
        return config

    def _get_contents(self, req: GeminiRequestParams) -> ContentListUnion | ContentListUnionDict:
        if req.file:
            file_config = UploadFileConfig(
                mime_type=req.file.content_type
            )
            file_to_process = self.client.files.upload(
                file=req.file.file,
                config=file_config
            )
            return [req.user_prompt, file_to_process]
        return [req.user_prompt]

    async def generate_content(self, req: GeminiRequestParams) -> GeminiResponseParams:

        try:
            response = await self.client.aio.models.generate_content(
                model=req.model,
                contents=self._get_contents(req),
                config=self._get_config(req)
            )

            logger.info(f"Response: {response.text}, metadata: {response.usage_metadata}")

            if req.is_json:
                try:
                    response_json = json.loads(response.text)
                    return GeminiResponseParams(
                        response=response_json,
                        is_error=False,
                        error_message="",
                        provider_response=response
                    )
                except json.JSONDecodeError as e:
                    logger.error(f"Error: {e}")
                    return self._handle_error(e, "Error converting response to JSON")
                except Exception as e:
                    logger.error(f"Error: {e}")
                    return self._handle_error(e, "Error converting response to JSON")
            else:
                return GeminiResponseParams(
                    response=response.text,
                    is_error=False,
                    error_message="",
                    provider_response=response
                )

        except ClientError as e:
            message = f"Client error: {e}"
            if e.code == 429:
                message = "Rate limit exceeded"
            return self._handle_error(e, message)
        except ServerError as e:
            return self._handle_error(e, "Server error")
        except APIError as e:
            return self._handle_error(e, "API error")
        except Exception as e:
            return self._handle_error(e, "Unknown error")


async def call_google_provider(req: GeminiRequestParams) -> GeminiResponseParams:
    google_provider = GoogleProviderClient()
    return await google_provider.generate_content(req)

