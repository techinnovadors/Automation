from fastapi import APIRouter

from app.api.endpoints.financial_document_analysis import financial_document_analysis
from app.api.endpoints.company_websearch import company_websearch

api_router = APIRouter()

api_router.include_router(
    financial_document_analysis.router,
    prefix="/fsa",
    tags=["Financial Document Analysis"],
)


api_router.include_router(
    company_websearch.router,
    prefix="/company_websearch",
    tags=["Company Websearch"],
)