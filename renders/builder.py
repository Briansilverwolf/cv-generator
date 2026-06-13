from pydantic import BaseModel
from typing import Any, List, Dict

from schema.cv import CVGenerationIR


class RenderSection(BaseModel):
    type: str
    data: Any


class RenderTree(BaseModel):
    contact: Dict
    summary: Dict
    sections: List[RenderSection]




class RenderTreeBuilder:

    def build(self, ir: CVGenerationIR) -> RenderTree:
        return RenderTree(
            contact=self._build_contact(ir),
            summary=self._build_summary(ir),
            sections=self._build_sections(ir)
        )

    # -------------------------
    # Contact normalization
    # -------------------------
    def _build_contact(self, ir: CVGenerationIR):
        c = ir.contact
        return {
            "name": c.name,
            "email": c.email,
            "phone": c.phone,
            "location": c.location,
            "profiles": c.online_profiles
        }

    # -------------------------
    # Summary normalization
    # -------------------------
    def _build_summary(self, ir: CVGenerationIR):
        s = ir.summary
        return {
            "text": s.text,
            "tone": s.tone,
            "keyword_density": s.keyword_density
        }

    # -------------------------
    # Sections (core abstraction)
    # -------------------------
    def _build_sections(self, ir: CVGenerationIR):

        sections = []

        if ir.experience:
            sections.append(
                RenderSection(
                    type="experience",
                    data=[self._experience_item(e) for e in ir.experience]
                )
            )

        if ir.skills:
            sections.append(
                RenderSection(
                    type="skills",
                    data=[self._skills_item(s) for s in ir.skills]
                )
            )

        if ir.education:
            sections.append(
                RenderSection(
                    type="education",
                    data=[self._education_item(e) for e in ir.education]
                )
            )

        if ir.projects:
            sections.append(
                RenderSection(
                    type="projects",
                    data=[self._project_item(p) for p in ir.projects]
                )
            )

        if ir.certifications:
            sections.append(
                RenderSection(
                    type="certifications",
                    data=[self._cert_item(c) for c in ir.certifications]
                )
            )

        return sections

    # -------------------------
    # Experience normalization
    # -------------------------
    def _experience_item(self, e):
        return {
            "title": e.title,
            "company": e.company,
            "location": e.location,
            "start_date": e.start_date,
            "end_date": e.end_date,
            "bullets": [
                {
                    "text": b.text,
                    "impact_level": b.impact_level,
                    "keywords": b.keyword_tags
                }
                for b in e.bullets
            ]
        }

    # -------------------------
    # Skills normalization
    # -------------------------
    def _skills_item(self, s):
        return {
            "category": s.category,
            "skills": s.skills,
            "keywords": s.keywords
        }

    # -------------------------
    # Education normalization
    # -------------------------
    def _education_item(self, e):
        return {
            "institution": e.institution,
            "degree": e.degree,
            "field_of_study": e.field_of_study,
            "graduation_year": e.graduation_year,
            "honors": e.honors
        }

    # -------------------------
    # Projects normalization
    # -------------------------
    def _project_item(self, p):
        return {
            "name": p.name,
            "description": p.description,
            "tech_stack": p.tech_stack,
            "link": p.link,
            "bullets": [
                {
                    "text": b.text,
                    "keywords": b.keywords
                }
                for b in p.bullets
            ]
        }

    # -------------------------
    # Certifications normalization
    # -------------------------
    def _cert_item(self, c):
        return {
            "name": c.name,
            "issuer": c.issuer,
            "year": c.year,
            "verification_url": c.verification_url
        }
        
