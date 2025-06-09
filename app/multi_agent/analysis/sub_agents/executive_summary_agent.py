from google.adk import Agent
import logging

from ..schema import FullCompetitiveAnalysisReport
from ..prompts import EXECUTIVE_SUMMARY_PROMPT
from ..utils import MODEL, call_single_agent

logger = logging.getLogger("uvicorn")


class ExecutiveSummaryAgent:
    def __init__(self):
        self.agent = Agent(
            model=MODEL,
            name="executive_summary_agent",
            instruction=EXECUTIVE_SUMMARY_PROMPT,
            tools=[],  # No tools needed
        )

    async def call(
        self, report_data: FullCompetitiveAnalysisReport, user_id: str, session_id: str
    ) -> str:
        # Prepare a concise version of the report data for the summary agent
        input_data = {
            "target_company_profile": report_data.target_company_profile.model_dump(),
            "competitor_profiles": [
                p.model_dump() for p in report_data.competitor_profiles
            ],
            "comparative_analysis_result": (
                report_data.comparative_analysis.model_dump()
                if report_data.comparative_analysis
                else {}
            ),
            "recommendations": [r.model_dump() for r in report_data.recommendations],
        }
        json_response = await call_single_agent(
            self.agent, user_id, session_id, "", input_data
        )
        # The prompt expects a single string as JSON output (e.g., "This is the summary.")
        # json.loads will parse this directly as a string.
        return json_response
