from uuid import uuid4
import logging

from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import JSONResponse

from app.agents.company_websearch.agent import CompanyWebSearchAgent

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/company_websearch")
async def company_websearch(company_url: str = Form(...)):
    try:
        company_websearch_agent = CompanyWebSearchAgent()
        content = await company_websearch_agent.call_agent(
            company_url=company_url, user_id=str(uuid4()), session_id=str(uuid4())
        )

        logger.info(content)
        return JSONResponse(content=content)
    except Exception as e:
        logger.exception(f"Error calling agent: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e
