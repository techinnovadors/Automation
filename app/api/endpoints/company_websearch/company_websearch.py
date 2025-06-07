import os
from datetime import datetime
from uuid import uuid4
import logging
from typing import List

from fastapi import APIRouter, Form, HTTPException

from app.multi_agent.analysis.orchestrator import OrchestratorAgent
from app.multi_agent.analysis.schema import CompanyProfile, CompetitorInfo, StartupProfile
from app.multi_agent.analysis.target_company_profiler_agent import (
    TargetCompanyProfilerAgent,
)
from app.multi_agent.analysis.sub_agents.competitor_identification_agent import (
    CompetitorIdentificationAgent,
)
from app.multi_agent.analysis.sub_agents.competitor_details_agent import (
    CompetitorDetailsAgent,
)

logger = logging.getLogger(__name__)

router = APIRouter()


async def get_company_profile(company_url: str, user_id: str, session_id: str) -> CompanyProfile:
    try:
        target_company_profiler_agent = TargetCompanyProfilerAgent()
        content = await target_company_profiler_agent.call(
            target_profile_url=company_url,
            user_id=user_id,
            session_id=session_id,
        )
        return content
    except Exception as e:
        logger.exception(f"Error calling agent: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e

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
        content = await get_company_profile(
            target_profile.websiteUrl,
            str(uuid4()),
            str(uuid4()),
        )

        logger.info(content)
        return content
    except Exception as e:
        logger.exception(f"Error calling agent: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/competitor_identification")
async def competitor_identification(target_profile: CompanyProfile):
    try:
        competitor_identification_agent = CompetitorIdentificationAgent()
        content = await competitor_identification_agent.call(
            target_profile=target_profile,
            user_id=str(uuid4()),
            session_id=str(uuid4()),
        )

        logger.info(content)
        return content
    except Exception as e:
        logger.exception(f"Error calling agent: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/competitor_details")
async def competitor_details(competitor_info: CompetitorInfo | List[CompetitorInfo]):
    try:
        session_id = str(uuid4())
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = os.path.join("outputs", f"run_{session_id}_{timestamp}")
        os.makedirs(output_dir, exist_ok=True)
        competitor_details_agent = CompetitorDetailsAgent()
        if isinstance(competitor_info, CompetitorInfo):
            competitor_info = [competitor_info]

        content = await competitor_details_agent.profile_competitors_in_parallel(
            competitor_infos=competitor_info,
            user_id=str(uuid4()),
            session_prefix=session_id,
            output_dir=output_dir,
        )

        logger.info(content)
        return content
    except Exception as e:
        logger.exception(f"Error calling agent: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e
