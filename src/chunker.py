"""Chunker Stage: Splits domain entities into retrieval-optimized chunks with rich filter metadata."""

import logging
from typing import Dict, Any, List

from src.schema import (
    Course,
    PrerequisiteEdge,
    AcademicRule,
    Resource,
    ModuleLesson,
    Exercise,
    Chunk,
)

logger = logging.getLogger("pipeline.chunker")

def build_retrieval_chunks(entities: Dict[str, List[Any]]) -> List[Chunk]:
    """
    Splits syllabi, academic regulations, open educational resources, and lessons into
    retrieval-sized semantic chunks (~150-350 tokens) formatted for dense/sparse vector embedding.
    """
    logger.info("Stage 4: Generating retrieval-sized chunks with filter metadata...")
    chunks: List[Chunk] = []

    courses: List[Course] = entities.get("courses", [])
    prereqs: List[PrerequisiteEdge] = entities.get("prerequisite_edges", [])
    rules: List[AcademicRule] = entities.get("academic_rules", [])
    resources: List[Resource] = entities.get("resources", [])
    modules: List[ModuleLesson] = entities.get("modules_lessons", [])
    exercises: List[Exercise] = entities.get("exercises", [])

    # Map course prerequisites for quick metadata injection
    prereq_map: Dict[str, List[str]] = {}
    for p in prereqs:
        prereq_map.setdefault(p.course, []).append(f"{p.requires} ({p.kind})")

    # 1. Chunk Courses: Overview Chunk & Detailed Syllabus Chunk
    for c in courses:
        reqs = prereq_map.get(c.code, ["None"])
        req_str = ", ".join(reqs)
        
        # Course Overview Chunk
        overview_text = (
            f"Course Code: {c.code}\n"
            f"Title: {c.title}\n"
            f"Department: {c.dept}\n"
            f"Credits: {c.credits} (L-T-P: {c.lecture_tutorial_practical or 'N/A'})\n"
            f"Semester Offered: Semester {c.semester_offered}\n"
            f"Curriculum Category: {c.type}\n"
            f"Instruction Mode: {c.mode}\n"
            f"Prerequisites: {req_str}\n"
            f"Summary: {c.title} is an official {c.type} course offered by the Department of {c.dept} at IIT Bhilai."
        )
        chunks.append(Chunk(
            chunk_id=f"chk_course_{c.code}_overview",
            parent_id=c.code,
            parent_type="course",
            chunk_type="course_overview",
            text=overview_text,
            filter_metadata={
                "entity": "course",
                "course_code": c.code,
                "dept": c.dept,
                "credits": c.credits,
                "semester": c.semester_offered,
                "category": c.type,
                "prerequisites": reqs,
            },
            source_url=c.source_url,
            retrieved_on=c.retrieved_on,
        ))

        # Course Syllabus Content Chunk
        syllabus_text = (
            f"Course: {c.code} - {c.title}\n"
            f"Department: {c.dept} | Credits: {c.credits}\n"
            f"Detailed Syllabus & Learning Objectives:\n{c.objectives}"
        )
        chunks.append(Chunk(
            chunk_id=f"chk_course_{c.code}_syllabus",
            parent_id=c.code,
            parent_type="course",
            chunk_type="syllabus_content",
            text=syllabus_text,
            filter_metadata={
                "entity": "course",
                "course_code": c.code,
                "dept": c.dept,
                "credits": c.credits,
                "semester": c.semester_offered,
                "category": c.type,
            },
            source_url=c.source_url,
            retrieved_on=c.retrieved_on,
        ))

    # 2. Chunk Academic Rules: Quotable Independent Entries
    for r in rules:
        rule_text = (
            f"IIT Bhilai Academic Regulation [{r.id}]\n"
            f"Category: {r.category}\n"
            f"Applies To: {r.applies_to}\n"
            f"Numeric Limit: {r.numeric_limit if r.numeric_limit is not None else 'N/A'}\n"
            f"Ordinance Provision:\n\"{r.text}\""
        )
        chunks.append(Chunk(
            chunk_id=f"chk_rule_{r.id}",
            parent_id=r.id,
            parent_type="academic_rule",
            chunk_type="rule_statement",
            text=rule_text,
            filter_metadata={
                "entity": "academic_rule",
                "rule_id": r.id,
                "category": r.category,
                "numeric_limit": r.numeric_limit,
                "applies_to": r.applies_to,
            },
            source_url=r.source_url,
            retrieved_on=r.retrieved_on,
        ))

    # 3. Chunk Open Educational Resources
    for res in resources:
        res_text = (
            f"Open Learning Resource: {res.title}\n"
            f"Resource ID: {res.id}\n"
            f"Provider: {res.provider}\n"
            f"Licence: {res.licence}\n"
            f"Format: {res.format}\n"
            f"Duration / Workload: {res.duration}\n"
            f"Direct Access URL: {res.url}\n"
            f"Description: Curated open educational material mapped to IIT Bhilai B.Tech CSE learning outcomes."
        )
        chunks.append(Chunk(
            chunk_id=f"chk_res_{res.id}",
            parent_id=res.id,
            parent_type="resource",
            chunk_type="resource_profile",
            text=res_text,
            filter_metadata={
                "entity": "resource",
                "resource_id": res.id,
                "provider": res.provider,
                "licence": res.licence,
                "format": res.format,
                "url": res.url,
            },
            source_url=res.source_url,
            retrieved_on=res.retrieved_on,
        ))

    # 4. Chunk Modules & Lessons
    for m in modules:
        mod_text = (
            f"Module / Lesson Unit: {m.title}\n"
            f"Parent ID: {m.parent_id} | Unit Sequence: {m.order}\n"
            f"Core Concepts Covered:\n{m.summary}"
        )
        chunks.append(Chunk(
            chunk_id=f"chk_mod_{m.id}",
            parent_id=m.parent_id,
            parent_type="module",
            chunk_type="lesson_unit",
            text=mod_text,
            filter_metadata={
                "entity": "module",
                "module_id": m.id,
                "parent_id": m.parent_id,
                "order": m.order,
            },
            source_url="https://iitbhilai.ac.in/index.php?pid=new_schedule_programs",
            retrieved_on="2026-11-11",
        ))

    # 5. Chunk Practice Exercises
    for ex in exercises:
        ex_text = (
            f"Practice Exercise [{ex.id}]\n"
            f"Target Skill: {ex.skill}\n"
            f"Difficulty Tier: {ex.difficulty.upper()}\n"
            f"Problem Statement:\n{ex.question}\n"
            f"Reference Solution & Rubric:\n{ex.answer_key}"
        )
        chunks.append(Chunk(
            chunk_id=f"chk_ex_{ex.id}",
            parent_id=ex.id,
            parent_type="exercise",
            chunk_type="exercise_problem",
            text=ex_text,
            filter_metadata={
                "entity": "exercise",
                "exercise_id": ex.id,
                "skill": ex.skill,
                "difficulty": ex.difficulty,
            },
            source_url="https://iitbhilai.ac.in/index.php?pid=new_schedule_programs",
            retrieved_on="2026-11-11",
        ))

    logger.info("Generated %d retrieval-ready chunks.", len(chunks))
    return chunks
