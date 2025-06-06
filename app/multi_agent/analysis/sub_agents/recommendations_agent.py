from typing import List

from google.adk import Agent
import logging

from ..utils import MODEL, call_single_agent
from ..schema import CompanyProfile, ComparativeAnalysisResult, Recommendation
from ..prompts import RECOMMENDATIONS_PROMPT

logger = logging.getLogger("uvicorn")


class RecommendationsAgent:
    def __init__(self):
        self.agent = Agent(
            model=MODEL,
            name="recommendations_agent",
            instruction=RECOMMENDATIONS_PROMPT,
            tools=[],  # No tools needed
        )

    async def call(
        self,
        target_profile: CompanyProfile,
        comparative_analysis: ComparativeAnalysisResult,
        user_id: str,
        session_id: str,
    ) -> List[Recommendation]:
        input_data = {
            "target_company_profile": target_profile.model_dump(),
            "comparative_analysis_result": comparative_analysis.model_dump(),
        }
        json_response = await call_single_agent(
            self.agent, user_id, session_id, RECOMMENDATIONS_PROMPT, input_data
        )
        return [Recommendation.model_validate(item) for item in json_response]
