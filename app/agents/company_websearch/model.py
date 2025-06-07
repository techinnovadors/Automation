from typing import List, Optional
from pydantic import BaseModel, HttpUrl


class FundingRound(BaseModel):
    round_type: Optional[str]
    date: Optional[str]
    amount: Optional[str]
    investors: Optional[List[str]] = []


class AcceleratorProgram(BaseModel):
    name: Optional[str]
    year: Optional[str]
    achievements: Optional[str]


class BasicInformation(BaseModel):
    company_name: Optional[str]
    headquarters: Optional[str]
    founded_year: Optional[int]
    founders: Optional[List[str]] = []
    key_executives: Optional[List[str]] = []
    employee_count: Optional[str]


class BusinessOverview(BaseModel):
    industry: Optional[str]
    sector: Optional[str]
    products_services: Optional[List[str]] = []
    business_model: Optional[str]
    target_customers: Optional[List[str]] = []
    target_geographies: Optional[List[str]] = []


class FundingAndInvestors(BaseModel):
    total_funding_raised: Optional[str]
    funding_rounds: Optional[List[FundingRound]] = []
    key_investors: Optional[List[str]] = []


class MarketPresenceAndOperations(BaseModel):
    operational_regions: Optional[List[str]] = []
    strategic_partnerships: Optional[List[str]] = []
    distribution_networks: Optional[List[str]] = []
    notable_clients: Optional[List[str]] = []


class GrowthStatistics(BaseModel):
    revenue: Optional[str]
    user_base: Optional[str]
    gmv: Optional[str]
    orders: Optional[str]


class TractionAndMetrics(BaseModel):
    growth_statistics: Optional[GrowthStatistics]
    sales_milestones: Optional[List[str]] = []
    product_adoption_metrics: Optional[List[str]] = []


class StrategicVision(BaseModel):
    mission: Optional[str]
    long_term_goals: Optional[str]
    esg_initiatives: Optional[List[str]] = []


class RecentDevelopments(BaseModel):
    news: Optional[List[str]] = []
    product_launches: Optional[List[str]] = []
    geographic_expansions: Optional[List[str]] = []
    key_updates: Optional[List[str]] = []


class OfficialLinks(BaseModel):
    website: Optional[HttpUrl]
    linkedin: Optional[HttpUrl]
    tracxn: Optional[HttpUrl]
    crunchbase: Optional[HttpUrl]
    other_links: Optional[List[HttpUrl]] = []


class CompanyProfile(BaseModel):
    basic_information: Optional[BasicInformation]
    business_overview: Optional[BusinessOverview]
    funding_and_investors: Optional[FundingAndInvestors]
    market_presence_and_operations: Optional[MarketPresenceAndOperations]
    traction_and_metrics: Optional[TractionAndMetrics]
    accelerator_incubator_participation: Optional[List[AcceleratorProgram]] = []
    strategic_vision: Optional[StrategicVision]
    recent_developments: Optional[RecentDevelopments]
    official_links: Optional[OfficialLinks]

class CompanyWebSearchOutput(BaseModel):
    company_profile: Optional[CompanyProfile]