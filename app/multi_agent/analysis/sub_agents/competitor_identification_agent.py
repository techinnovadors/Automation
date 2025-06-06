from typing import List

from google.adk import Agent
from google.adk.tools import google_search

from ..utils import MODEL, call_single_agent
from ..schema import CompanyProfile, CompetitorInfo
from ..prompts import COMPETITOR_IDENTIFICATION_PROMPT


class CompetitorIdentificationAgent:
    def __init__(self):
        self.agent = Agent(
            model=MODEL,
            name="competitor_identification_agent",
            instruction=COMPETITOR_IDENTIFICATION_PROMPT,
            tools=[google_search],  # This agent needs web search
        )

    async def call(
        self, target_profile: CompanyProfile, user_id: str, session_id: str
    ) -> List[CompetitorInfo]:
        input_data = target_profile.model_dump()
        json_response = await call_single_agent(
            self.agent,
            user_id,
            session_id,
            COMPETITOR_IDENTIFICATION_PROMPT,
            input_data,
        )
        return [CompetitorInfo.model_validate(item) for item in json_response]

