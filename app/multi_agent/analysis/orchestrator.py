import json
import logging
import os
from datetime import datetime

from .sub_agents import (
    CompetitorIdentificationAgent,
    CompetitorDetailsAgent,
    ComparativeAnalysisAgent,
    ExecutiveSummaryAgent,
)

from .schema import (
    FullCompetitiveAnalysisReport,
    CompanyProfile,
)
from .utils import save_json_to_file

logger = logging.getLogger(__name__)

BASE_OUTPUT_DIR = "/Users/apple/work/Antennae/Automation/outputs/example"


# The Orchestrator Agent that manages the workflow
class OrchestratorAgent:
    def __init__(self):
        self.competitor_identifier = CompetitorIdentificationAgent()
        self.competitor_details_agent = CompetitorDetailsAgent()
        self.comparative_analyser = ComparativeAnalysisAgent()
        # self.recommendations_agent = RecommendationsAgent()
        self.executive_summary_agent = ExecutiveSummaryAgent()

    async def run_analysis(
        self, target_profile: CompanyProfile, user_id: str, session_id: str
    ) -> FullCompetitiveAnalysisReport:
        """
        Orchestrates the entire competitive analysis process by calling specialized agents sequentially.
        """
        # Create a unique output directory for this analysis run
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = os.path.join("outputs", f"run_{session_id}_{timestamp}")
        os.makedirs(output_dir, exist_ok=True)

        logger.info(
            f"Orchestrator: Starting analysis for {target_profile.name}. Outputs will be saved to '{output_dir}'"
        )

        save_json_to_file(target_profile, "01_target_profile.json", output_dir)
        logger.info(f"Orchestrator: Target company profiled: {target_profile.name}")
        # target_profile_file_path = os.path.join(
        #     BASE_OUTPUT_DIR, "01_target_profile.json"
        # )
        # with open(target_profile_file_path, "r", encoding="utf-8") as f:
        #     target_profile = json.load(f)
        #     target_profile = CompanyProfile.model_validate(target_profile)
        #     logger.info(f"Orchestrator: Target company profiled: {target_profile.name}")

        # 2. Identify Competitors
        logger.info("Orchestrator: Calling CompetitorIdentificationAgent...")
        competitor_infos = await self.competitor_identifier.call(
            target_profile, user_id, f"{session_id}-competitor-id"
        )
        save_json_to_file(competitor_infos, "02_competitor_infos.json", output_dir)
        logger.info(
            f"Orchestrator: Found {len(competitor_infos)} potential competitors."
        )
        # competitor_infos_file_path = os.path.join(
        #     BASE_OUTPUT_DIR, "02_competitor_infos.json"
        # )
        # with open(competitor_infos_file_path, "r", encoding="utf-8") as f:
        #     competitor_infos = json.load(f)
        #     competitor_infos = [
        #         CompetitorInfo.model_validate(item) for item in competitor_infos
        #     ]
        #     logger.info(
        #         f"Orchestrator: Found {len(competitor_infos)} potential competitors."
        #     )
        # 3. Profile Each Competitor
        # For simplicity, profiling sequentially. In a real application, this could be parallelized.
        competitor_profiles = await self.competitor_details_agent.profile_competitors_in_parallel(
            competitor_infos,
            user_id,
            session_prefix=session_id,
            output_dir=output_dir,
        )

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
                # recommendations=[],
                executive_summary="No competitors could be identified or profiled for detailed analysis.",
            )

        # 4. Perform Comparative Analysis
        logger.info("Orchestrator: Calling ComparativeAnalysisAgent...")
        comparative_analysis = await self.comparative_analyser.call(
            competitor_profiles, user_id, f"{session_id}-compare"
        )
        save_json_to_file(
            comparative_analysis, "04_comparative_analysis.json", output_dir
        )
        logger.info("Orchestrator: Comparative analysis complete.")

        # 5. Generate Recommendations
        # logger.info("Orchestrator: Calling RecommendationsAgent...")
        # recommendations = await self.recommendations_agent.call(
        #     target_profile, comparative_analysis, user_id, f"{session_id}-recommend"
        # )
        # save_json_to_file(recommendations, "05_recommendations.json", output_dir)
        # logger.info(f"Orchestrator: Generated {len(recommendations)} recommendations.")

        # Assemble preliminary report for executive summary generation
        report_data = FullCompetitiveAnalysisReport(
            target_company_profile=target_profile,
            competitor_profiles=competitor_profiles,
            comparative_analysis=comparative_analysis,
        )

        # 6. Generate Executive Summary
        logger.info("Orchestrator: Calling ExecutiveSummaryAgent...")
        executive_summary = await self.executive_summary_agent.call(
            report_data, user_id, f"{session_id}-exec-summary"
        )
        save_json_to_file(executive_summary, "06_executive_summary.json", output_dir)
        logger.info("Orchestrator: Executive summary complete.")

        # Final report assembly
        report_data.executive_summary = executive_summary
        save_json_to_file(
            report_data, "07_full_competitive_analysis_report.json", output_dir
        )

        logger.info("Orchestrator: Full competitive analysis process complete.")
        return report_data
