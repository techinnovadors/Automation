from pydantic import BaseModel
from typing import Any, Optional
from fastapi import UploadFile

class TextGenerationRequest(BaseModel):
    model: str
    user_prompt: str
    system_prompt: str

class TextGenerationResponse(BaseModel):
    is_error: bool
    error_message: str
    provider_response: Any

class GeminiRequestParams(TextGenerationRequest):
    model: str = "gemini-2.5-flash-preview-05-20"
    file: Optional[UploadFile] = None
    is_json: bool = False
    pass_provider_response: bool = False

class GeminiResponseParams(TextGenerationResponse):
    response: Optional[Any] = None



