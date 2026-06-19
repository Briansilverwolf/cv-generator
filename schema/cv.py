from pydantic import BaseModel, Field
from typing import List, Optional, Literal


# ---------------------------
# CORE CONTACT + IDENTITY
# ---------------------------

class ContactBlock(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    online_profiles: List[str] = Field(default_factory=list)


# ---------------------------
# SUMMARY (ATS-OPTIMIZED)
# ---------------------------

class SummaryBlock(BaseModel):
    text: str
    tone: Literal["formal", "neutral", "technical"] = "neutral"
    keyword_density: Optional[float] = None  # estimated ATS keyword density


# ---------------------------
# SKILLS (ATS-GROUPED)
# ---------------------------

class SkillBlock(BaseModel):
    category: str
    skills: List[str]  = Field(default_factory = list, description=" short description of the skill")
    keywords: List[str] = Field(default_factory=list)  # ATS enrichment layer


# ---------------------------
# EXPERIENCE (ATS BULLETS)
# ---------------------------

class ExperienceBullet(BaseModel):
    text: str
    impact_level: Optional[Literal["low", "medium", "high"]] = None
    keyword_tags: List[str] = Field(default_factory=list)


class ExperienceBlock(BaseModel):
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    bullets: List[ExperienceBullet] = Field(default_factory=list)


# ---------------------------
# EDUCATION
# ---------------------------

class EducationBlock(BaseModel):
    institution: str
    degree: str
    field_of_study: Optional[str] = None
    graduation_year: Optional[int] = None
    honors: Optional[str] = None


# ---------------------------
# CERTIFICATIONS
# ---------------------------

class CertificationBlock(BaseModel):
    name: str
    issuer: Optional[str] = None
    year: Optional[int] = None
    verification_url: Optional[str] = None


# ---------------------------
# PROJECTS (ATS + TECH STACK)
# ---------------------------

class ProjectBullet(BaseModel):
    text: str
    keywords: List[str] = Field(default_factory=list)


class ProjectBlock(BaseModel):
    name: str
    description: Optional[str] = None
    bullets: List[ProjectBullet] = Field(default_factory=list)
    tech_stack: List[str] = Field(default_factory=list)
    link: Optional[str] = None





class CVGenerationIR(BaseModel):
    contact: ContactBlock
    summary: SummaryBlock
    skills: List[SkillBlock]
    experience: List[ExperienceBlock] = Field(default_factory=list)
    projects: List[ProjectBlock] = Field(default_factory=list)
    education: List[EducationBlock] = Field(default_factory=list)
    certifications: List[CertificationBlock] = Field(default_factory=list)
    generation_metadata: Optional[dict] = None