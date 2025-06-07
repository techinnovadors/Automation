import logging
from typing import Any, Dict
from google.adk import Agent
from google.adk.tools import google_search
from google.genai import types

from ..utils import MODEL, call_single_agent  # Import common utilities
from ..schema import CompanyProfile, StartupProfile  # Import both schemas
from ..prompts import TARGET_COMPANY_PROFILER_PROMPT  # Import prompt

logger = logging.getLogger(__name__)  # Using uvicorn logger as specified by the user


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
        self, target_profile: StartupProfile, user_id: str, session_id: str
    ) -> CompanyProfile:
        """
        Augments a given StartupProfile with additional general company information.

        Args:
            target_profile (StartupProfile): The initial startup profile from the API request.
            user_id (str): Unique identifier for the user.
            session_id (str): Unique identifier for the current session.

        Returns:
            CompanyProfile: A comprehensive company profile including data from StartupProfile
                            and newly researched fields.
        """
        # Pass the entire StartupProfile as input data to the agent
        # The prompt is designed to instruct the LLM to parse this and then research
        input_data = { "company_url": target_profile.websiteUrl }  # Convert Pydantic model to dict for input

        logger.info(
            f"TargetCompanyProfilerAgent: Augmenting StartupProfile for {target_profile.registeredName}"
        )

        # Call the single agent. The prompt instructs the agent to perform web searches
        # using the provided websiteUrl from the StartupProfile and populate the
        # remaining CompanyProfile fields.
        raw_response = await call_single_agent(
            self.agent, user_id, session_id, TARGET_COMPANY_PROFILER_PROMPT, input_data
        )

        logger.info(f"TargetCompanyProfilerAgent Raw Response: {raw_response}")

        # Validate the raw response against the CompanyProfile schema
        # This will convert the LLM's JSON output into a structured CompanyProfile object
        augmented_company_profile = CompanyProfile.model_validate(raw_response)

        logger.info(
            f"TargetCompanyProfilerAgent: Successfully augmented profile for {augmented_company_profile.name}"
        )

        return augmented_company_profile
