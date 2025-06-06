from fastapi import APIRouter

from app.api.endpoints.company_websearch import company_websearch

api_router = APIRouter()


api_router.include_router(
    company_websearch.router,
    prefix="/company_websearch",
    tags=["Company Websearch"],
)
