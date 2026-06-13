from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class CandidateProfile(BaseModel):
    """Basic candidate information extracted from the CV."""

    name: Optional[str] = Field(
        default=None,
        description="Candidate full name."
    )

    email: Optional[str] = Field(
        default=None,
        description="Primary email address."
    )

    phone: Optional[str] = Field(
        default=None,
        description="Primary phone number."
    )

    location: Optional[str] = Field(
        default=None,
        description="Candidate location or city."
    )

    online_profiles: List[str] = Field(
        default_factory=list,
        description="Portfolio, GitHub, LinkedIn, personal website, or other professional profiles."
    )

    target_roles: List[str] = Field(
        default_factory=list,
        description="Roles the candidate appears to be targeting."
    )

    seniority_level: Optional[
        Literal[
            "Intern",
            "Junior",
            "Mid-Level",
            "Senior",
            "Lead",
            "Manager",
            "Executive"
        ]
    ] = Field(
        default=None,
        description="Estimated career level."
    )

    years_of_experience: Optional[float] = Field(
        default=None,
        description="Estimated total years of professional experience."
    )


class Skill(BaseModel):
    """Normalized candidate skill."""

    name: str = Field(
        description="Canonical skill name."
    )

    category: Literal[
        "Programming",
        "Framework",
        "Database",
        "Cloud",
        "Tool",
        "TechnicalSkill",
        "SoftSkill",
        "Language",
        "Other"
    ] = Field(
        description="Skill category."
    )

    confidence: float = Field(
        ge=0,
        le=1,
        description="Confidence that the skill was correctly extracted."
    )


class Achievement(BaseModel):
    """Achievement extracted from an experience or project."""

    statement: str = Field(
        description="Achievement statement."
    )

    quantified: bool = Field(
        description="Whether the achievement contains measurable impact."
    )

    metric: Optional[str] = Field(
        default=None,
        description="Detected metric such as 20%, 100 users, $10K saved."
    )


class Experience(BaseModel):
    """Professional experience entry."""

    title: str = Field(
        description="Job title."
    )

    company: str = Field(
        description="Employer or organization."
    )

    start_date: Optional[str] = Field(
        default=None,
        description="Employment start date."
    )

    end_date: Optional[str] = Field(
        default=None,
        description="Employment end date."
    )

    duration_months: Optional[int] = Field(
        default=None,
        description="Estimated duration in months."
    )

    responsibilities: List[str] = Field(
        default_factory=list,
        description="Key duties and responsibilities."
    )

    achievements: List[Achievement] = Field(
        default_factory=list,
        description="Achievements associated with the role."
    )

    technologies: List[str] = Field(
        default_factory=list,
        description="Technologies, tools, and platforms used."
    )


class Education(BaseModel):
    """Educational qualification."""

    degree: str = Field(
        description="Degree, diploma, certificate, or qualification."
    )

    institution: str = Field(
        description="School, college, or university."
    )

    field_of_study: Optional[str] = Field(
        default=None,
        description="Area of study."
    )

    graduation_year: Optional[int] = Field(
        default=None,
        description="Year completed."
    )


class Certification(BaseModel):
    """Professional certification."""

    name: str = Field(
        description="Certification name."
    )

    issuer: Optional[str] = Field(
        default=None,
        description="Organization issuing the certification."
    )

    year: Optional[int] = Field(
        default=None,
        description="Year awarded."
    )


class Project(BaseModel):
    """Project extracted from the CV."""

    name: str = Field(
        description="Project name."
    )

    description: str = Field(
        description="Project overview."
    )

    technologies: List[str] = Field(
        default_factory=list,
        description="Technologies used."
    )

    outcomes: List[str] = Field(
        default_factory=list,
        description="Project results, impact, or achievements."
    )


class Strength(BaseModel):
    """Candidate strength identified during analysis."""

    category: str = Field(
        description="Strength category."
    )

    evidence: List[str] = Field(
        default_factory=list,
        description="Supporting evidence from the CV."
    )

    confidence: float = Field(
        ge=0,
        le=1,
        description="Confidence in the strength assessment."
    )


class Weakness(BaseModel):
    """Potential weakness or improvement area."""

    category: str = Field(
        description="Weakness category."
    )

    evidence: List[str] = Field(
        default_factory=list,
        description="Evidence supporting the weakness."
    )

    severity: Literal[
        "Low",
        "Medium",
        "High"
    ] = Field(
        description="Impact severity."
    )


class ATSKeywordAnalysis(BaseModel):
    """ATS keyword matching results."""

    matched_keywords: List[str] = Field(
        default_factory=list,
        description="Keywords successfully identified in the CV."
    )

    missing_keywords: List[str] = Field(
        default_factory=list,
        description="Important keywords missing from the CV."
    )


class ATSAnalysis(BaseModel):
    """ATS-oriented scoring and evaluation."""

    formatting_score: int = Field(
        ge=0,
        le=100,
        description="Formatting and ATS compatibility score."
    )

    keyword_score: int = Field(
        ge=0,
        le=100,
        description="Keyword optimization score."
    )

    experience_score: int = Field(
        ge=0,
        le=100,
        description="Experience relevance score."
    )

    achievement_score: int = Field(
        ge=0,
        le=100,
        description="Achievement quality score."
    )

    readability_score: int = Field(
        ge=0,
        le=100,
        description="Readability and clarity score."
    )

    overall_score: int = Field(
        ge=0,
        le=100,
        description="Overall ATS readiness score."
    )

    keyword_analysis: ATSKeywordAnalysis = Field(
        description="Detailed keyword matching results."
    )


class GapAnalysis(BaseModel):
    """Identified gaps affecting candidate competitiveness."""

    missing_keywords: List[str] = Field(
        default_factory=list,
        description="Keywords recommended for inclusion."
    )

    weak_sections: List[str] = Field(
        default_factory=list,
        description="Sections requiring improvement."
    )

    missing_metrics: List[str] = Field(
        default_factory=list,
        description="Missing measurable achievements."
    )


class RewriteTarget(BaseModel):
    """Specific improvement target for CV rewriting."""

    original_text: str = Field(
        description="Original content found in the CV."
    )

    reason: str = Field(
        description="Why the content should be improved."
    )


class Recommendation(BaseModel):
    """Recommended improvement action."""

    priority: Literal[
        "Low",
        "Medium",
        "High"
    ] = Field(
        description="Recommendation priority."
    )

    category: str = Field(
        description="Area requiring improvement."
    )

    recommendation: str = Field(
        description="Suggested improvement."
    )


class RewritePlan(BaseModel):
    """Instructions for CV enhancement."""

    weak_bullets: List[RewriteTarget] = Field(
        default_factory=list,
        description="Bullets that should be rewritten."
    )

    missing_sections: List[str] = Field(
        default_factory=list,
        description="Sections that should be added."
    )

    recommended_projects: List[str] = Field(
        default_factory=list,
        description="Projects worth highlighting or adding."
    )


class ATSOptimizationHints(BaseModel):
    keyword_density_target: float = 0.08
    prioritize_keywords: List[str] = Field(default_factory=list)
    avoid_keywords: List[str] = Field(default_factory=list)

    rewrite_mode: Literal["strict", "balanced", "creative"] = "balanced"

    # Controls how aggressively weak content is rewritten
    enhancement_level: Literal["light", "medium", "aggressive"] = "medium"


class CVQualityMetrics(BaseModel):
    ats_score: Optional[int] = None
    keyword_coverage: Optional[int] = None
    readability_score: Optional[int] = None

    has_quantified_achievements: bool = False
    has_action_verbs: bool = False
    experience_strength: Literal["weak", "moderate", "strong"] = "moderate"
    

class CVAnalysisIR(BaseModel):
    """Master IR produced by CV analysis."""

    candidate_profile: CandidateProfile = Field(
        description="Candidate profile information."
    )
    professional_summary: Optional[str] = Field(
        default=None,
        description="Extracted professional summary."
    )
    skills: List[Skill] = Field(
        default_factory=list,
        description="Normalized skill inventory."
    )
    experiences: List[Experience] = Field(
        default_factory=list,
        description="Professional experience history."
    )
    education: List[Education] = Field(
        default_factory=list,
        description="Educational background."
    )
    certifications: List[Certification] = Field(
        default_factory=list,
        description="Professional certifications."
    )
    projects: List[Project] = Field(
        default_factory=list,
        description="Projects extracted or inferred from the CV."
    )
    strengths: List[Strength] = Field(
        default_factory=list,
        description="Identified strengths."
    )
    weaknesses: List[Weakness] = Field(
        default_factory=list,
        description="Identified weaknesses."
    )
    ats_analysis: ATSAnalysis = Field(
        description="ATS scoring and evaluation."
    )
    gap_analysis: GapAnalysis = Field(
        description="Detected gaps and missing information."
    )
    quality: CVQualityMetrics = Field(default_factory=CVQualityMetrics)
    
    ats_hints: ATSOptimizationHints = Field(default_factory=ATSOptimizationHints)
    
    rewrite_plan: RewritePlan = Field(
        description="Structured instructions for CV improvement."
    )

    recommendations: List[Recommendation] = Field(default_factory=list,description="Prioritized recommendations.")
    
