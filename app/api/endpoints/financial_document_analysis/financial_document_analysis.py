from fastapi import APIRouter, UploadFile, File
from app.services.google_provider import call_google_provider
from app.services.models import GeminiRequestParams

from .prompts import FinancialDocumentAnalysisPrompts

router = APIRouter()

# @router.post("/test_google_provider")
# async def test_google_provider():
#     response = await call_google_provider(
#         GeminiRequestParams(
#             user_prompt="Who are you?",
#             system_prompt="",
#             model="gemini-1.5-flash",
#             is_json=False
#         )
#     )
#     return response.response


@router.post("/financial_document_analysis")
async def financial_document_analysis(file: UploadFile = File(...)):
    return await call_google_provider(
        GeminiRequestParams(
            user_prompt="Analyse the financial document and provide the answer in a tabular format with 3 columns.",
            system_prompt=FinancialDocumentAnalysisPrompts.FINANCIAL_DOCUMENT_ANALYSIS_v2.value,
            model="gemini-2.0-flash",
            is_json=False,
            file=file
        )
    )

