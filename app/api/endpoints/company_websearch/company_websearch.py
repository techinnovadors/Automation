from uuid import uuid4
import logging

from fastapi import APIRouter, Form, HTTPException

from app.multi_agent.analysis.orchestrator import OrchestratorAgent
from app.multi_agent.analysis.schema import CompanyProfile, StartupProfile
from app.multi_agent.analysis.target_company_profiler_agent import (
    TargetCompanyProfilerAgent,
)

logger = logging.getLogger("uvicorn")

router = APIRouter()


@router.post("/company_websearch")
async def company_websearch(target_profile: CompanyProfile):
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


@router.post("/target_company_profiler")
async def target_company_profiler(target_profile: StartupProfile):
    try:
        target_company_profiler_agent = TargetCompanyProfilerAgent()
        content = await target_company_profiler_agent.call(
            target_profile=target_profile,
            user_id=str(uuid4()),
            session_id=str(uuid4()),
        )

        logger.info(content)
        return content
    except Exception as e:
        logger.exception(f"Error calling agent: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e
