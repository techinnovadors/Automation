from uuid import uuid4
import logging

from fastapi import APIRouter, Form, HTTPException

from app.multi_agent.analysis.orchestrator import OrchestratorAgent
from app.multi_agent.analysis.schema import StartupProfile

logger = logging.getLogger("uvicorn")

router = APIRouter()


@router.post("/analysis_of_application_company")
async def analysis_of_application_company(target_profile: StartupProfile):
    try:
        company_websearch_agent = OrchestratorAgent()
        content = await company_websearch_agent.run_analysis(
            target_profile=target_profile,
            user_id=str(uuid4()),
            session_id=str(uuid4()),
        )

        logger.info(content)
        return content
    except Exception as e:
        logger.exception(f"Error calling agent: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e
