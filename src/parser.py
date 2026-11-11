"""Parse and Normalise Stage: Transforms raw dictionaries into strongly typed, normalized domain entities."""

import re
import logging
from typing import Dict, Any, List

from src.schema import (
    Course,
    PrerequisiteEdge,
    Skill,
    CourseSkillLink,
    AcademicRule,
    Resource,
    ResourceSkillLink,
    ModuleLesson,
    Exercise,
    SourceType,
)

logger = logging.getLogger("pipeline.parser")

def clean_text_field(text: str) -> str:
    """Normalize whitespace and quotes in textual fields."""
    if not text:
        return ""
    # Replace weird unicode spaces or quotes
    text = re.sub(r'[\r\n\t]+', ' ', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()

def parse_and_normalise(raw_payload: Dict[str, Any]) -> Dict[str, List[Any]]:
    """
    Normalizes inconsistent strings, ensures uniform course codes, converts numeric credits,
    and constructs validated Pydantic instances.
    """
    logger.info("Stage 2: Parsing and normalising records across all domains...")
    
    parsed_courses: List[Course] = []
    for c in raw_payload.get("courses", []):
        parsed_courses.append(Course(
            code=c["code"].strip().upper(),
            title=clean_text_field(c["title"]),
            dept=clean_text_field(c["dept"]),
            credits=float(c["credits"]),
            lecture_tutorial_practical=c.get("lecture_tutorial_practical"),
            semester_offered=int(c["semester_offered"]),
            type=clean_text_field(c["type"]),
            mode=clean_text_field(c["mode"]),
            objectives=clean_text_field(c["objectives"]),
            source_url=c["source_url"].strip(),
            retrieved_on=c["retrieved_on"].strip(),
            source_type=SourceType(c.get("source_type", "official")),
        ))

    parsed_prereqs: List[PrerequisiteEdge] = []
    for p in raw_payload.get("prerequisite_edges", []):
        parsed_prereqs.append(PrerequisiteEdge(
            course=p["course"].strip().upper(),
            requires=p["requires"].strip().upper(),
            kind=p.get("kind", "hard"),
            source_url=p["source_url"].strip(),
            retrieved_on=p["retrieved_on"].strip(),
            source_type=SourceType(p.get("source_type", "official")),
        ))

    parsed_skills: List[Skill] = []
    for s in raw_payload.get("skills", []):
        parsed_skills.append(Skill(
            id=s["id"].strip().upper(),
            name=clean_text_field(s["name"]),
            level=s["level"].lower(),
            parent_skill=s["parent_skill"].strip().upper() if s.get("parent_skill") else None,
            source_url=s["source_url"].strip(),
            retrieved_on=s["retrieved_on"].strip(),
            source_type=SourceType(s.get("source_type", "official")),
        ))

    parsed_course_skills: List[CourseSkillLink] = []
    for cs in raw_payload.get("course_skill_links", []):
        parsed_course_skills.append(CourseSkillLink(
            course=cs["course"].strip().upper(),
            skill=cs["skill"].strip().upper(),
            depth=cs["depth"].lower(),
        ))

    parsed_rules: List[AcademicRule] = []
    for r in raw_payload.get("academic_rules", []):
        parsed_rules.append(AcademicRule(
            id=r["id"].strip().upper(),
            category=clean_text_field(r["category"]),
            text=clean_text_field(r["text"]),
            numeric_limit=float(r["numeric_limit"]) if r.get("numeric_limit") is not None else None,
            applies_to=clean_text_field(r["applies_to"]),
            source_url=r["source_url"].strip(),
            retrieved_on=r["retrieved_on"].strip(),
            source_type=SourceType(r.get("source_type", "official")),
        ))

    parsed_resources: List[Resource] = []
    for res in raw_payload.get("resources", []):
        parsed_resources.append(Resource(
            id=res["id"].strip().upper(),
            title=clean_text_field(res["title"]),
            provider=clean_text_field(res["provider"]),
            licence=clean_text_field(res["licence"]),
            format=clean_text_field(res["format"]),
            duration=clean_text_field(res["duration"]),
            url=res["url"].strip(),
            source_url=res["source_url"].strip(),
            retrieved_on=res["retrieved_on"].strip(),
            source_type=SourceType(res.get("source_type", "open-licence")),
        ))

    parsed_resource_skills: List[ResourceSkillLink] = []
    for rs in raw_payload.get("resource_skill_links", []):
        parsed_resource_skills.append(ResourceSkillLink(
            resource=rs["resource"].strip().upper(),
            skill=rs["skill"].strip().upper(),
            level=rs["level"].lower(),
        ))

    parsed_modules: List[ModuleLesson] = []
    for m in raw_payload.get("modules_lessons", []):
        parsed_modules.append(ModuleLesson(
            id=m["id"].strip().upper(),
            parent_id=m["parent_id"].strip().upper(),
            order=int(m["order"]),
            title=clean_text_field(m["title"]),
            summary=clean_text_field(m["summary"]),
        ))

    parsed_exercises: List[Exercise] = []
    for ex in raw_payload.get("exercises", []):
        parsed_exercises.append(Exercise(
            id=ex["id"].strip().upper(),
            skill=ex["skill"].strip().upper(),
            difficulty=ex["difficulty"].lower(),
            question=clean_text_field(ex["question"]),
            answer_key=clean_text_field(ex["answer_key"]),
        ))

    logger.info(
        "Successfully normalized %d courses, %d prereqs, %d skills, %d rules, %d resources, %d modules, %d exercises.",
        len(parsed_courses),
        len(parsed_prereqs),
        len(parsed_skills),
        len(parsed_rules),
        len(parsed_resources),
        len(parsed_modules),
        len(parsed_exercises),
    )

    return {
        "courses": parsed_courses,
        "prerequisite_edges": parsed_prereqs,
        "skills": parsed_skills,
        "course_skill_links": parsed_course_skills,
        "academic_rules": parsed_rules,
        "resources": parsed_resources,
        "resource_skill_links": parsed_resource_skills,
        "modules_lessons": parsed_modules,
        "exercises": parsed_exercises,
    }
