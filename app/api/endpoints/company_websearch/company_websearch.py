from uuid import uuid4
import logging

from fastapi import APIRouter, Form, HTTPException

from app.multi_agent.analysis.orchestrator import OrchestratorAgent

logger = logging.getLogger("uvicorn")

router = APIRouter()


@router.post("/company_websearch")
async def company_websearch(company_url: str = Form(...)):
    try:
        company_websearch_agent = OrchestratorAgent()
        content = await company_websearch_agent.run_analysis(
            company_url=company_url, user_id=str(uuid4()), session_id=str(uuid4())
        )

        logger.info(content)
        return content
    except Exception as e:
        logger.exception(f"Error calling agent: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e
