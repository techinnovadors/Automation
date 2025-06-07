from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any


class Citation(BaseModel):
    source_name: str
    date: Optional[str] = None
    source_url: Optional[str] = None


class Headquarters(BaseModel):
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None


class ProductService(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None


class KeyMetric(BaseModel):
    metric_name: str
    value: str
    source_name: Optional[str] = None
    source_url: Optional[str] = None
    date: Optional[str] = None


class MarketSegment(BaseModel):
    segment: str
    details: Optional[str] = None


class GeographicFootprintEntry(BaseModel):
    region: str
    details: Optional[str] = None


class ValueProposition(BaseModel):
    proposition: str
    details: Optional[str] = None


class RecentDevelopment(BaseModel):
    date: Optional[str] = None
    development: str
    source_name: Optional[str] = None
    source_url: Optional[str] = None
    details: Optional[str] = None


class CompanyProfile(BaseModel):
    name: str
    url: Optional[str] = None
    founding_date: Optional[str] = None
    headquarters: Optional[Headquarters] = None
    core_products_services: List[ProductService] = Field(
        default_factory=list, alias="core_products_service_lines"
    )
    key_metrics: List[KeyMetric] = Field(default_factory=list)
    market_segments: List[MarketSegment] = Field(default_factory=list)
    geographic_footprint: List[GeographicFootprintEntry] = Field(default_factory=list)
    unique_value_propositions: List[ValueProposition] = Field(default_factory=list)
    recent_developments: List[RecentDevelopment] = Field(default_factory=list)
    citations: List[Citation] = Field(default_factory=list)
    other_relevant_info: Optional[Dict[str, Any]] = None

    class Config:
        validate_by_name = True
        populate_by_name = True


# Schema for identifying a competitor (name and optional URL)
class CompetitorInfo(BaseModel):
    name: str
    url: Optional[str] = None


# Schema for a competitor's detailed profile (inherits from CompanyProfile)
class CompetitorProfile(CompanyProfile):
    pass  # No new fields, just a semantic distinction for clarity


# New nested model for competitor comparison value
class CompetitorComparisonValue(BaseModel):
    name: str
    value: str


# Updated ComparativeCriterion to match LLM output
class ComparativeCriterion(BaseModel):
    name: str = Field(
        validation_alias="criterion"
    )  # Map 'criterion' from LLM output to 'name'
    target_value: Optional[str] = Field(
        None, validation_alias="target_company"
    )  # Map 'target_company'
    competitors: List[CompetitorComparisonValue] = Field(
        default_factory=list
    )  # Expect a list of the new model


# New nested model for benchmarking best practices entry
class BenchmarkEntry(BaseModel):
    competitor_name: str
    area_of_excellence: str
    explanation: str


# Schema for the overall comparative analysis results
class ComparativeAnalysisResult(BaseModel):
    summary: str
    comparison_matrix: List[ComparativeCriterion] = Field(default_factory=list)
    key_strengths: List[str] = Field(default_factory=list)
    key_weaknesses: List[str] = Field(default_factory=list)
    market_trends_opportunities: List[str] = Field(default_factory=list)
    threats_risks: List[str] = Field(default_factory=list)
    # Updated to expect a list of BenchmarkEntry
    benchmarking_best_practices: List[BenchmarkEntry] = Field(default_factory=list)


# Schema for a single strategic recommendation
class Recommendation(BaseModel):
    initiative: str
    timeframe: str  # "short-term", "mid-term", "long-term"
    details: str
    estimated_resources: Optional[str] = None
    kpis: List[str] = Field(default_factory=list)


class FundingRound(BaseModel):
    fundsRaised: str  # Assuming string as it's "100" which could be "100M" etc.
    investorName: str
    mailId: Optional[str] = None
    monthYear: str  # e.g., "06/2022"
    phoneNumber: Optional[str] = None
    shareholding: str  # "10" (as string to accommodate percentages later maybe)
    stage: str  # e.g., "Seed"


class TeamMember(BaseModel):
    contactNumber: Optional[str] = None
    coreStrength: str
    designation: str
    email: Optional[str] = None
    linkedinUrl: Optional[str] = None
    location: str
    name: str
    pastExperience: str  # Assuming string as it's "8"
    qualifications: str
    # teamSize: str  # Assuming string as "15"


class TractionMetrics(BaseModel):
    clients: str
    ebitda: str
    gmv: str
    growth: str
    mau: str
    revenue: str


class StartupProfile(BaseModel):
    cityOfOperation: str
    dilution: Optional[str] = None  # Assuming string as "15" might imply percentage later
    domicile: str
    equityOffered: Optional[str] = None  # Assuming string as "15" might imply percentage later
    founderLinkedinUrls: List[str] = Field(default_factory=list)
    foundingYear: str  # "2021" as string
    fundingAmount: str  # "500" as string (could be "500M" etc.)
    marketType: str
    preMoneyValuation: str  # "3000" as string
    previousFundingRounds: List[FundingRound] = Field(default_factory=list)
    revenueARR: Optional[str] = None  # "500000" as string (to accommodate currency/units)
    registeredName: str
    revenueModel: str
    sector: List[str] = Field(default_factory=list)
    team: List[TeamMember] = Field(default_factory=list)
    traction: Dict[str, TractionMetrics]  # Dynamically named keys like "m1", "m2"
    useOfFunds: str
    websiteUrl: str

    class Config:
        validate_by_name = True
        populate_by_name = True

class ExecutiveSummary(BaseModel):
    summary: str

# The comprehensive final report schema
class FullCompetitiveAnalysisReport(BaseModel):
    target_company_profile: CompanyProfile
    competitor_profiles: List[CompetitorProfile] = Field(default_factory=list)
    comparative_analysis: Optional[ComparativeAnalysisResult] = None
    recommendations: List[Recommendation] = Field(default_factory=list)
    executive_summary: Optional[str] = None  # Will be generated last
