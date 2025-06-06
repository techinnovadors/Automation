from typing import List

from google.adk import Agent
import logging
from google.genai import types

from ..utils import MODEL, call_single_agent
from ..schema import CompanyProfile, CompetitorProfile, ComparativeAnalysisResult
from ..prompts import COMPARATIVE_ANALYSIS_PROMPT

logger = logging.getLogger(__name__)


class ComparativeAnalysisAgent:
    def __init__(self):
        self.agent = Agent(
            model=MODEL,
            name="comparative_analysis_agent",
            instruction=COMPARATIVE_ANALYSIS_PROMPT,
            tools=[],  # No tools needed for this agent, it processes internal data
            generate_content_config=types.GenerateContentConfig(
                response_mime_type="application/json",
                max_output_tokens=50000,
            ),
        )

    async def call(
        self,
        target_profile: CompanyProfile,
        competitor_profiles: List[CompetitorProfile],
        user_id: str,
        session_id: str,
    ) -> ComparativeAnalysisResult:
        input_data = {
            "target_company_profile": target_profile.model_dump(),
            "competitor_profiles": [p.model_dump() for p in competitor_profiles],
        }
        json_response = await call_single_agent(
            self.agent, user_id, session_id, COMPARATIVE_ANALYSIS_PROMPT, input_data
        )
        return ComparativeAnalysisResult.model_validate(json_response)
