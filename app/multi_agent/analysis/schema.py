from pydantic import BaseModel, Field, AliasPath, ValidationError
from typing import List, Dict, Optional, Any

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class Citation(BaseModel):
    source_name: str
    date: Optional[str] = None


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
    core_products_services: List[ProductService] = Field(default_factory=list, alias="core_products_service_lines")
    key_metrics: List[KeyMetric] = Field(default_factory=list)
    market_segments: List[MarketSegment] = Field(default_factory=list)
    geographic_footprint: List[GeographicFootprintEntry] = Field(default_factory=list)
    unique_value_propositions: List[ValueProposition] = Field(default_factory=list)
    recent_developments: List[RecentDevelopment] = Field(default_factory=list)
    citations: List[Citation] = Field(default_factory=list)
    other_relevant_info: Optional[Dict[str, Any]] = None

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True


# Schema for identifying a competitor (name and optional URL)
class CompetitorInfo(BaseModel):
    name: str
    url: Optional[str] = None


# Schema for a competitor's detailed profile (inherits from CompanyProfile)
class CompetitorProfile(CompanyProfile):
    pass  # No new fields, just a semantic distinction for clarity


# Represents a single criterion in the comparative analysis matrix
class ComparativeCriterion(BaseModel):
    name: str  # e.g., "Product Lines", "Pricing Model", "Market Share"
    target_value: Optional[str] = None
    competitor_values: Dict[str, str] = Field(
        default_factory=dict
    )  # Competitor name -> value


# Schema for the overall comparative analysis results
class ComparativeAnalysisResult(BaseModel):
    summary: str
    comparison_matrix: List[ComparativeCriterion] = Field(default_factory=list)
    key_strengths: List[str] = Field(default_factory=list)
    key_weaknesses: List[str] = Field(default_factory=list)
    market_trends_opportunities: List[str] = Field(default_factory=list)
    threats_risks: List[str] = Field(default_factory=list)
    benchmarking_best_practices: Dict[str, str] = Field(
        default_factory=dict
    )  # Competitor -> what they do well


# Schema for a single strategic recommendation
class Recommendation(BaseModel):
    initiative: str
    timeframe: str  # "short-term", "mid-term", "long-term"
    details: str
    estimated_resources: Optional[str] = None
    kpis: List[str] = Field(default_factory=list)


# The comprehensive final report schema
class FullCompetitiveAnalysisReport(BaseModel):
    target_company_profile: CompanyProfile
    competitor_profiles: List[CompetitorProfile] = Field(default_factory=list)
    comparative_analysis: Optional[ComparativeAnalysisResult] = None
    recommendations: List[Recommendation] = Field(default_factory=list)
    executive_summary: Optional[str] = None  # Will be generated last
