from pydantic import BaseModel, Field
from typing import List, Optional, Dict

# --- Core Data Models for a Single Fiscal Year's Snapshot within a comparison ---


class EquitySnapshot(BaseModel):
    value: Optional[str] = Field(
        None, description="The financial value of the metric (e.g., 'around ₹22 Cr')."
    )
    notes: Optional[str] = Field(
        None,
        description="Additional notes or context for the metric for this specific year.",
    )


class DebtSnapshot(BaseModel):
    value: Optional[str] = Field(
        None,
        description="The financial value of the total debt (e.g., '₹170-₹180 Cr').",
    )
    notes: Optional[str] = Field(
        None,
        description="Additional notes or context for the debt for this specific year.",
    )
    financing_ratio: Optional[str] = Field(
        None,
        description="The percentage of total assets financed by debt for this specific year (e.g., '85-90% of total assets').",
    )


class AssetSnapshot(BaseModel):
    value: Optional[str] = Field(
        None, description="The financial value of the asset (e.g., 'around ₹200 Cr')."
    )
    notes: Optional[str] = Field(
        None,
        description="Additional notes or context for the asset for this specific year.",
    )


class IncomeSnapshot(BaseModel):
    value: Optional[str] = Field(
        None,
        description="The financial value of the income (e.g., 'approximately ₹120 Cr').",
    )
    notes: Optional[str] = Field(
        None,
        description="Additional notes or context for the income for this specific year.",
    )


class ProfitSnapshot(BaseModel):
    value: Optional[str] = Field(
        None, description="The financial value of the profit (e.g., '~₹6 Cr')."
    )
    notes: Optional[str] = Field(
        None,
        description="Additional notes or context for the profit or margin for this specific year.",
    )


# --- Consolidated Annual Data for specific fiscal years within a comparison ---


class FiscalYearEquityAndLiabilitiesData(BaseModel):
    shareholders_equity: Optional[EquitySnapshot] = Field(
        None, description="Shareholders' equity data for this specific fiscal year."
    )
    equity_share_capital: Optional[EquitySnapshot] = Field(
        None, description="Equity share capital data for this specific fiscal year."
    )
    total_debt: Optional[DebtSnapshot] = Field(
        None, description="Total debt data for this specific fiscal year."
    )


class AssetsSummaryForComparison(BaseModel):
    total_assets: Optional[AssetSnapshot] = Field(
        None, description="Summary data for total assets for this fiscal year."
    )
    property_plant_equipment_notes: Optional[str] = Field(
        None,
        description="Notes on Property, Plant & Equipment (PPE) for this fiscal year (e.g., 'minimal capital expenditure').",
    )
    current_assets_notes: Optional[str] = Field(
        None,
        description="Notes on current assets for this fiscal year (e.g., 'modest increase due to higher trade receivables').",
    )
    cash_and_bank_balances: Optional[str] = Field(
        None,
        description="Status of cash and bank balances for this fiscal year (e.g., 'remained low').",
    )
    inventory: Optional[str] = Field(
        None,
        description="Description of inventory's role as an asset component for this fiscal year (e.g., 'very small asset component').",
    )
    # asset_turnover could be added here if it's a static value per year, or derived from a ratio model


class IncomeAndProfitabilityForComparison(BaseModel):
    revenue_from_operations: Optional[IncomeSnapshot] = Field(
        None, description="Revenue from operations data for this fiscal year."
    )
    other_income_notes: Optional[str] = Field(
        None, description="Notes on 'Other Income' significance for this fiscal year."
    )
    total_income_notes: Optional[str] = Field(
        None, description="Overall trend notes for total income for this fiscal year."
    )
    operating_expenses_notes: Optional[str] = Field(
        None,
        description="Notes on operating expenses for this fiscal year (e.g., 'managed costs well').",
    )
    key_operating_expenses: Optional[List[str]] = Field(
        None,
        description="List of key operating expense categories for this fiscal year.",
    )
    finance_costs_notes: Optional[str] = Field(
        None, description="Notes on finance costs for this fiscal year."
    )
    depreciation_notes: Optional[str] = Field(
        None, description="Notes on depreciation for this fiscal year."
    )
    net_profit_after_tax: Optional[ProfitSnapshot] = Field(
        None, description="Net profit after tax data for this fiscal year."
    )
    net_profit_margin: Optional[ProfitSnapshot] = Field(
        None, description="Net profit margin data for this fiscal year."
    )
    dividends: Optional[str] = Field(
        None, description="Information on dividend payouts for this fiscal year."
    )
    tax_expense: Optional[str] = Field(
        None, description="Information on tax expense for this fiscal year."
    )


# --- Liquidity Metric (used within FiscalYearComparisonData) ---
class LiquidityMetric(BaseModel):
    current_ratio: Optional[str] = Field(
        None, description="The calculated current ratio (e.g., '< 1')."
    )
    notes: Optional[str] = Field(
        None,
        description="Notes on the liquidity position (e.g., 'strained due to significant short-term borrowings').",
    )


# --- Single Comparison Period Model ---


class FiscalYearComparisonData(BaseModel):
    comparison_years: str = Field(
        ...,
        description="The string representing the fiscal year comparison (e.g., 'FY 2024-2025 vs FY 2023-2024').",
    )
    current_fy_data: Optional[FiscalYearEquityAndLiabilitiesData] = Field(
        None,
        description="Equity & Liabilities snapshot for the 'current' year of the comparison.",
    )
    previous_fy_data: Optional[FiscalYearEquityAndLiabilitiesData] = Field(
        None,
        description="Equity & Liabilities snapshot for the 'previous' year of the comparison.",
    )
    assets_summary: Optional[AssetsSummaryForComparison] = Field(
        None,
        description="Summary of asset changes and state for the comparison period (primarily reflecting the 'current' year's assets and notes on changes from 'previous').",
    )
    income_and_profitability_summary: Optional[IncomeAndProfitabilityForComparison] = (
        Field(
            None,
            description="Summary of income and profitability changes and state for the comparison period (primarily reflecting the 'current' year's performance and notes on changes from 'previous').",
        )
    )
    liquidity_position: Optional[LiquidityMetric] = Field(
        None,
        description="Summary of the company's liquidity position relevant to this comparison (e.g., for the latest year in comparison).",
    )
    overall_change_notes: Optional[str] = Field(
        None,
        description="Overall notes describing key financial changes across these two years within this specific comparison.",
    )


# --- Overall Financial Summary - List of Comparisons ---


class OverallFinancialSummary(BaseModel):
    comparative_periods: List[FiscalYearComparisonData] = Field(
        [],
        description="A list of financial analyses for different fiscal year comparison periods. Each item in the list represents a comparison between two consecutive fiscal years.",
    )


# --- Detailed Ratio Analysis Models ---


class CalculatedRatioValues(BaseModel):
    yearly_values: Dict[str, str] = Field(
        {},
        description="A dictionary where keys are fiscal year strings (e.g., 'fy_2024_2025') and values are the calculated ratio values for that year.",
    )


class RatioDetail(BaseModel):
    ratio_name: str = Field(
        ..., description="The name of the financial ratio (e.g., 'current_ratio')."
    )
    calculation_formula: str = Field(
        ...,
        description="The formula used to calculate the ratio (e.g., 'current_assets / current_liabilities').",
    )
    calculated_values: CalculatedRatioValues = Field(
        ..., description="The calculated values for the ratio across periods."
    )
    interpretation_and_analysis: str = Field(
        ...,
        description="Detailed interpretation and analysis of the ratio's significance and trends across available years.",
    )


class DetailedRatioAnalysis(BaseModel):
    liquidity_ratios: Optional[List[RatioDetail]] = Field(
        None, description="A list of liquidity ratio details."
    )
    solvency_ratios: Optional[List[RatioDetail]] = Field(
        None, description="A list of solvency ratio details."
    )
    profitability_ratios: Optional[List[RatioDetail]] = Field(
        None, description="A list of profitability ratio details."
    )
    efficiency_ratios: Optional[List[RatioDetail]] = Field(
        None, description="A list of efficiency ratio details."
    )


# --- Specific Financial Deep Dive Models ---


class SectionAnalysis(BaseModel):
    assessment: Optional[str] = Field(
        None, description="A high-level assessment of the specific financial area."
    )
    details: Optional[str] = Field(
        None,
        description="Detailed explanation and analysis of the financial area, potentially referencing trends across years.",
    )
    data_availability: Optional[str] = Field(
        None,
        description="Indicates if sufficient data was available for this analysis (e.g., 'insufficient_data_available_for_analysis').",
    )
    inferred_details: Optional[str] = Field(
        None, description="Details inferred when direct data was insufficient."
    )
    investments: Optional[str] = Field(
        None, description="Analysis of investments as non_core exposure."
    )
    loans_and_advances: Optional[str] = Field(
        None, description="Analysis of loans and advances as non_core exposure."
    )
    contingent_liabilities: Optional[str] = Field(
        None,
        description="Analysis of contingent liabilities related to non_core exposure.",
    )
    conclusion: Optional[str] = Field(
        None,
        description="A concluding remark for the specific non_core exposure analysis.",
    )


class SpecificFinancialDeepDive(BaseModel):
    operating_margin_stability: Optional[SectionAnalysis] = Field(
        None,
        description="Analysis of the stability of operating margins, potentially across multiple recent years.",
    )
    other_income_scrutiny: Optional[SectionAnalysis] = Field(
        None, description="Scrutiny of 'Other Income' for unusual components."
    )
    earnings_quality_assessment: Optional[SectionAnalysis] = Field(
        None,
        description="Assessment of earnings quality against cash flow, typically for the most recent period but with an eye on trends.",
    )
    working_capital_efficiency: Optional[SectionAnalysis] = Field(
        None, description="Analysis of working capital efficiency and its trend."
    )
    related_party_transactions_and_leakage: Optional[SectionAnalysis] = Field(
        None,
        description="Analysis of related_party_transactions for potential fund leakage.",
    )
    debt_service_capability: Optional[SectionAnalysis] = Field(
        None,
        description="Assessment of the company's ability to service its debt over time.",
    )
    reinvestment_strategy_capex: Optional[SectionAnalysis] = Field(
        None,
        description="Review of capital expenditure and reinvestment strategy across periods.",
    )
    equity_changes_and_promoters: Optional[SectionAnalysis] = Field(
        None,
        description="Examination of equity changes and promoter actions over time.",
    )
    non_core_exposure: Optional[SectionAnalysis] = Field(
        None,
        description="Scrutiny of non_core exposures like loans to group companies.",
    )


# --- Main Financial Analysis Model ---


class FinancialAnalysis(BaseModel):
    overall_financial_summary: Optional[OverallFinancialSummary] = Field(
        None,
        description="A high-level summary of the company's financial performance and position, structured by fiscal year comparison periods.",
    )
    detailed_ratio_analysis: Optional[DetailedRatioAnalysis] = Field(
        None,
        description="In-depth analysis of key financial ratios, showing multi-year trends.",
    )
    specific_financial_deep_dive: Optional[SpecificFinancialDeepDive] = Field(
        None,
        description="Detailed analysis of specific financial aspects, with insights into historical trends where relevant.",
    )


# --- Top-level schema ---
class FinancialAnalysisSchema(BaseModel):
    financial_analysis: FinancialAnalysis = Field(
        ..., description="The comprehensive financial analysis report."
    )
