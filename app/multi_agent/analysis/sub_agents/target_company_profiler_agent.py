from google.adk import Agent
from google.adk.tools import google_search
import logging
import os

from ..utils import MODEL, call_single_agent
from ..schema import CompanyProfile
from ..prompts import TARGET_COMPANY_PROFILER_PROMPT

logger = logging.getLogger("uvicorn")

os.environ["GEMINI_API_KEY"] = "AIzaSyBB2Dokeq-ehG4uDylTUxS71WdIcMi0Ct8"

# Individual Specialized Agents
class TargetCompanyProfilerAgent:
    def __init__(self):
        self.agent = Agent(
            model=MODEL,
            name="target_company_profiler_agent",
            instruction=TARGET_COMPANY_PROFILER_PROMPT,
            tools=[google_search],  # This agent needs web search
        )

    async def call(
        self, company_url: str, user_id: str, session_id: str
    ) -> CompanyProfile:
        input_data = {"company_url": company_url}
        raw_response = await call_single_agent(
            self.agent, user_id, session_id, "", input_data
        )

        logger.info(f"TargetCompanyProfilerAgent Response: {raw_response}")

        return CompanyProfile.model_validate(raw_response)
