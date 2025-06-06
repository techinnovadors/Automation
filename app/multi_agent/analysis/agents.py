import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

# Assuming google.adk is available and configured in your environment
# If not, you would need to adapt to use google.generativeai directly and simulate Agent/Runner.
from google.adk import Agent
from google.adk.tools import google_search
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

from .prompts import (
    TARGET_COMPANY_PROFILER_PROMPT,
    COMPETITOR_IDENTIFICATION_PROMPT,
    COMPETITOR_DETAILS_PROMPT,
    COMPARATIVE_ANALYSIS_PROMPT,
    RECOMMENDATIONS_PROMPT,
    EXECUTIVE_SUMMARY_PROMPT,
)
from .schema import (
    CompanyProfile,
    CompetitorInfo,
    CompetitorProfile,
    ComparativeAnalysisResult,
    Recommendation,
    FullCompetitiveAnalysisReport,
)

logger = logging.getLogger(__name__)

# Model to be used by all agents
MODEL = "gemini-2.5-flash-preview-05-20"
APP_NAME = "MultiAgentCompetitiveAnalysis"

def _save_json_to_file(data: Any, base_filename: str, session_id: str):
    """Saves serializable data to a timestamped JSON file."""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Sanitize base_filename to be safe for file paths
        safe_base_filename = "".join(
            c for c in base_filename if c.isalnum() or c in ("_", "-")
        ).rstrip()
        file_path = f"{safe_base_filename}_{session_id}_{timestamp}.json"

        def convert_to_dict(obj: Any) -> Any:
            """Recursively convert Pydantic models to dicts."""
            if hasattr(obj, "model_dump"):
                return obj.model_dump()
            if isinstance(obj, list):
                return [convert_to_dict(i) for i in obj]
            if isinstance(obj, dict):
                return {k: convert_to_dict(v) for k, v in obj.items()}
            return obj

        data_to_save = convert_to_dict(data)

        with open(file_path, "w") as f:
            json.dump(data_to_save, f, indent=4)
        logger.info(f"Saved data to {file_path}")
    except Exception as e:
        logger.error(
            f"Failed to save '{base_filename}' to JSON: {e}", exc_info=True
        )


def _clean_json_from_text(text: str) -> str:
    """
    Extracts a JSON string from a text that might contain markdown code fences.
    Handles both JSON objects ({...}) and JSON arrays ([...]).
    """
    json_start_index = text.find("{")
    array_start_index = text.find("[")

    # Determine the actual start index
    if json_start_index == -1 and array_start_index == -1:
        return text  # No JSON object or array found
    elif json_start_index == -1:  # Only array found
        start_index = array_start_index
    elif array_start_index == -1:  # Only JSON object found
        start_index = json_start_index
    else:  # Both found, pick the earliest one
        start_index = min(json_start_index, array_start_index)

    json_end_index = text.rfind("}")
    array_end_index = text.rfind("]")

    # Determine the actual end index
    if json_end_index == -1 and array_end_index == -1:
        return text  # No JSON object or array end found
    elif json_end_index == -1:  # Only array end found
        end_index = array_end_index
    elif array_end_index == -1:  # Only JSON object end found
        end_index = json_end_index
    else:  # Both found, pick the latest one
        end_index = max(json_end_index, array_end_index)

    return text[start_index : end_index + 1]


async def _call_single_agent(
    agent_instance: Agent,
    user_id: str,
    session_id: str,
    prompt_text: str,
    input_data: Optional[Dict[str, Any]] = None,
) -> Any:
    """
    Helper function to call a single agent, manage its session, and parse its JSON output.
    """
    session_service = (
        InMemorySessionService()
    )  # Each sub-agent gets its own session service for isolated runs
    runner = Runner(
        agent=agent_instance, app_name=APP_NAME, session_service=session_service
    )

    full_prompt = prompt_text
    if input_data:
        # Embed input_data as JSON for the agent to process
        full_prompt += f"\n\nHere is the input data:\n```json\n{json.dumps(input_data, indent=2)}\n```"

    content = types.Content(parts=[types.Part(text=full_prompt)], role="user")
    raw_response = ""
    try:
        await session_service.create_session(
            app_name=APP_NAME, user_id=user_id, session_id=session_id
        )
        async for event in runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content
        ):
            # Check for final response containing content
            if event.is_final_response() and event.content and event.content.parts:
                raw_response = event.content.parts[0].text
                break
            # Handle potential agent escalations (errors)
            elif event.actions and event.actions.escalate:
                logger.error(
                    f"Agent '{agent_instance.name}' escalation: {event.actions.escalate}"
                )
                raise Exception(
                    f"Agent '{agent_instance.name}' escalation: {event.actions.escalate}"
                )
    except Exception as e:
        logger.error(f"Error running agent '{agent_instance.name}': {e}", exc_info=True)
        raise  # Re-raise the exception after logging
    finally:
        # Ensure the session is always deleted
        await session_service.delete_session(
            app_name=APP_NAME, user_id=user_id, session_id=session_id
        )

    if not raw_response:
        raise Exception(f"Agent '{agent_instance.name}' returned no content.")

    try:
        cleaned_json_str = _clean_json_from_text(raw_response)
        if not cleaned_json_str:
            raise ValueError(f"Could not extract JSON from response: {raw_response}")
        return json.loads(cleaned_json_str)
    except json.JSONDecodeError as e:
        logger.error(
            f"JSON decode error from agent '{agent_instance.name}' response: {e}\nRaw response: {raw_response}",
            exc_info=True,
        )
        raise ValueError(
            f"Invalid JSON response from agent '{agent_instance.name}'. Raw: {raw_response}"
        ) from e
    except ValueError as e:
        logger.error(
            f"Validation error from agent '{agent_instance.name}' response: {e}\nRaw response: {raw_response}",
            exc_info=True,
        )
        raise


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
        raw_response = await _call_single_agent(
            self.agent, user_id, session_id, TARGET_COMPANY_PROFILER_PROMPT, input_data
        )

        logger.info(f"Raw response: {raw_response}")

        return CompanyProfile.model_validate(raw_response)


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
        json_response = await _call_single_agent(
            self.agent,
            user_id,
            session_id,
            COMPETITOR_IDENTIFICATION_PROMPT,
            input_data,
        )
        return [CompetitorInfo.model_validate(item) for item in json_response]


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
        json_response = await _call_single_agent(
            self.agent, user_id, session_id, COMPETITOR_DETAILS_PROMPT, input_data
        )
        # If the agent returns an empty dict or invalid data, handle it gracefully
        if not json_response or not json_response.get("name"):
            logger.warning(
                f"CompetitorDetailsAgent returned incomplete/empty profile for {competitor_info.name}. Returning partial."
            )
            return CompetitorProfile(
                name=competitor_info.name, url=competitor_info.url or "N/A"
            )
        return CompetitorProfile.model_validate(json_response)


class ComparativeAnalysisAgent:
    def __init__(self):
        self.agent = Agent(
            model=MODEL,
            name="comparative_analysis_agent",
            instruction=COMPARATIVE_ANALYSIS_PROMPT,
            tools=[],  # No tools needed for this agent, it processes internal data
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
        json_response = await _call_single_agent(
            self.agent, user_id, session_id, COMPARATIVE_ANALYSIS_PROMPT, input_data
        )
        return ComparativeAnalysisResult.model_validate(json_response)


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
        json_response = await _call_single_agent(
            self.agent, user_id, session_id, RECOMMENDATIONS_PROMPT, input_data
        )
        return [Recommendation.model_validate(item) for item in json_response]


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
        json_response = await _call_single_agent(
            self.agent, user_id, session_id, EXECUTIVE_SUMMARY_PROMPT, input_data
        )
        # The prompt expects a single string as JSON output (e.g., "This is the summary.")
        # json.loads will parse this directly as a string.
        return json_response


# The Orchestrator Agent that manages the workflow
class OrchestratorAgent:
    def __init__(self):
        self.target_profiler = TargetCompanyProfilerAgent()
        self.competitor_identifier = CompetitorIdentificationAgent()
        self.competitor_details_agent = CompetitorDetailsAgent()
        self.comparative_analyser = ComparativeAnalysisAgent()
        self.recommendations_agent = RecommendationsAgent()
        self.executive_summary_agent = ExecutiveSummaryAgent()

    async def run_analysis(
        self, company_url: str, user_id: str, session_id: str
    ) -> FullCompetitiveAnalysisReport:
        """
        Orchestrates the entire competitive analysis process by calling specialized agents sequentially.
        """
        logger.info(f"Orchestrator: Starting analysis for {company_url}")

        # 1. Profile Target Company
        logger.info("Orchestrator: Calling TargetCompanyProfilerAgent...")
        target_profile = await self.target_profiler.call(
            company_url, user_id, f"{session_id}-target-profile"
        )
        _save_json_to_file(target_profile, "target_profile", session_id)
        logger.info(f"Orchestrator: Target company profiled: {target_profile.name}")

        # 2. Identify Competitors
        logger.info("Orchestrator: Calling CompetitorIdentificationAgent...")
        competitor_infos = await self.competitor_identifier.call(
            target_profile, user_id, f"{session_id}-competitor-id"
        )
        _save_json_to_file(competitor_infos, "competitor_infos", session_id)
        logger.info(
            f"Orchestrator: Found {len(competitor_infos)} potential competitors."
        )

        # 3. Profile Each Competitor
        # For simplicity, profiling sequentially. In a real application, this could be parallelized.
        competitor_profiles: List[CompetitorProfile] = []
        for i, info in enumerate(competitor_infos):
            logger.info(
                f"Orchestrator: Calling CompetitorDetailsAgent for competitor {i+1}/{len(competitor_infos)}: {info.name} ({info.url or 'No URL provided'})"
            )
            try:
                profile = await self.competitor_details_agent.call(
                    info, user_id, f"{session_id}-comp-detail-{i}"
                )
                _save_json_to_file(
                    profile, f"competitor_profile_{info.name}", session_id
                )
                competitor_profiles.append(profile)
            except Exception as e:
                logger.warning(
                    f"Orchestrator: Failed to profile competitor {info.name}: {e}. Skipping this competitor.",
                    exc_info=True,
                )
                # You might add a placeholder profile or retry logic here if needed.

        logger.info(
            f"Orchestrator: Successfully profiled {len(competitor_profiles)} out of {len(competitor_infos)} identified competitors."
        )

        logger.info(f"Competitor profiles: {competitor_profiles}")


        # Ensure there are competitors to compare against
        if not competitor_profiles:
            logger.warning(
                "No competitor profiles gathered. Cannot perform comparative analysis or generate recommendations."
            )
            # Assemble a partial report and return
            return FullCompetitiveAnalysisReport(
                target_company_profile=target_profile,
                competitor_profiles=[],
                comparative_analysis=None,
                recommendations=[],
                executive_summary="No competitors could be identified or profiled for detailed analysis.",
            )

        # 4. Perform Comparative Analysis
        logger.info("Orchestrator: Calling ComparativeAnalysisAgent...")
        comparative_analysis = await self.comparative_analyser.call(
            target_profile, competitor_profiles, user_id, f"{session_id}-compare"
        )
        _save_json_to_file(comparative_analysis, "comparative_analysis", session_id)
        logger.info("Orchestrator: Comparative analysis complete.")

        # 5. Generate Recommendations
        logger.info("Orchestrator: Calling RecommendationsAgent...")
        recommendations = await self.recommendations_agent.call(
            target_profile, comparative_analysis, user_id, f"{session_id}-recommend"
        )
        _save_json_to_file(recommendations, "recommendations", session_id)
        logger.info(f"Orchestrator: Generated {len(recommendations)} recommendations.")

        # Assemble preliminary report for executive summary generation
        report_data = FullCompetitiveAnalysisReport(
            target_company_profile=target_profile,
            competitor_profiles=competitor_profiles,
            comparative_analysis=comparative_analysis,
            recommendations=recommendations,
        )

        # 6. Generate Executive Summary
        logger.info("Orchestrator: Calling ExecutiveSummaryAgent...")
        executive_summary = await self.executive_summary_agent.call(
            report_data, user_id, f"{session_id}-exec-summary"
        )
        _save_json_to_file(executive_summary, "executive_summary", session_id)
        logger.info("Orchestrator: Executive summary complete.")

        # Final report assembly
        report_data.executive_summary = executive_summary
        _save_json_to_file(report_data, "full_competitive_analysis_report", session_id)

        logger.info("Orchestrator: Full competitive analysis process complete.")
        return report_data
