from typing import List, Optional
import asyncio

from google.adk import Agent
from google.adk.tools import google_search
import logging

from ..utils import MODEL, call_single_agent, save_json_to_file, MAX_CONCURRENT_PROFILES
from ..schema import CompetitorInfo, CompetitorProfile
from ..prompts import COMPETITOR_DETAILS_PROMPT

logger = logging.getLogger(__name__)


class CompetitorDetailsAgent:
    def __init__(self):
        self.agent = Agent(
            model=MODEL,
            name="competitor_details_agent",
            instruction=COMPETITOR_DETAILS_PROMPT,
            tools=[google_search],  # This agent needs web search
        )

    async def call(
        self, competitor_info: CompetitorInfo, user_id: str, session_id: str
    ) -> CompetitorProfile:
        input_data = competitor_info.model_dump()
        json_response = await call_single_agent(
            self.agent, user_id, session_id, COMPETITOR_DETAILS_PROMPT, input_data
        )
        logger.info(f"CompetitorDetailsAgent response: {json_response}")
        # If the agent returns an empty dict or invalid data, handle it gracefully
        if not json_response or not json_response.get("name"):
            logger.warning(
                f"CompetitorDetailsAgent returned incomplete/empty profile for {competitor_info.name}. Returning partial."
            )
            return CompetitorProfile(
                name=competitor_info.name, url=competitor_info.url or "N/A"
            )
        return CompetitorProfile.model_validate(json_response)


async def profile_competitors_in_parallel(
    competitor_infos: List[CompetitorInfo],
    competitor_details_agent: CompetitorDetailsAgent,
    user_id: str,
    session_prefix: str,
    output_dir: str,  # Pass output_dir to _safe_profile
) -> List[CompetitorProfile]:
    """
    Profiles multiple competitors concurrently using the CompetitorDetailsAgent.
    Handles errors for individual profiles and saves successful ones to file immediately.
    Implements a concurrency limit using asyncio.Semaphore.
    """
    competitor_profiles_tasks = []
    # Create a semaphore to limit concurrent tasks
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_PROFILES)

    async def _safe_profile(
        info: CompetitorInfo,
        task_session_id: str,
        current_output_dir: str,  # Receive output_dir
    ) -> Optional[CompetitorProfile]:
        """Wrapper to acquire semaphore and handle individual profiling with retries.
        Saves the profile to file immediately upon success.
        """
        async with semaphore:
            logger.info(
                f"Semaphore acquired. Profiling competitor: {info.name} ({info.url or 'No URL provided'})"
            )
            try:
                # The call method internally uses call_single_agent, which has retry logic
                profile = await competitor_details_agent.call(
                    info, user_id, task_session_id
                )
                logger.info(f"Semaphore released. Successfully profiled: {info.name}")

                # --- MOVED: Save JSON immediately after successful profiling ---
                save_json_to_file(
                    profile,
                    f"03_competitor_profile_{info.name.replace(' ', '_').replace('/', '')}.json",
                    current_output_dir,  # Use the passed output_dir
                )
                # -------------------------------------------------------------

                return profile
            except Exception as e:
                logger.warning(
                    f"Failed to profile competitor {info.name} after all retries in _safe_profile: {e}. Skipping this competitor.",
                    exc_info=True,
                )
                return None  # Return None if profiling ultimately fails

    for i, info in enumerate(competitor_infos):
        task_session_id = f"{session_prefix}-comp-detail-{i}"
        competitor_profiles_tasks.append(
            _safe_profile(info, task_session_id, output_dir)
        )  # Pass output_dir to task

    # Run all competitor profiling tasks concurrently with a limit
    logger.info(
        f"Orchestrator: Running {len(competitor_infos)} CompetitorDetailsAgent tasks in parallel with a concurrency limit of {MAX_CONCURRENT_PROFILES}..."
    )

    profiled_results = await asyncio.gather(*competitor_profiles_tasks)

    competitor_profiles: List[CompetitorProfile] = []
    for i, profile_or_none in enumerate(profiled_results):
        # No longer saving here, as it's done inside _safe_profile
        if profile_or_none:
            competitor_profiles.append(profile_or_none)
        else:
            info = competitor_infos[i]  # Still need info for logging context
            logger.warning(
                f"Competitor {info.name} was skipped due to previous errors or validation issues."
            )

    return competitor_profiles
