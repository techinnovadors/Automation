from fastapi import APIRouter

from app.api.endpoints.financial_document_analysis import financial_document_analysis


api_router = APIRouter()

api_router.include_router(
    financial_document_analysis.router,
    prefix="/fsa",
    tags=["Financial Document Analysis"],
)
