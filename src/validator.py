"""Validator Stage: Rigorously verifies referential integrity, DAG acyclicity, schema constraints, and provenance."""

import logging
from typing import Dict, Any, List
import networkx as nx

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
)

logger = logging.getLogger("pipeline.validator")

class PipelineValidationError(Exception):
    """Raised when data integrity or schema invariants are violated."""
    pass

class ValidationReport:
    def __init__(self):
        self.checks_run = 0
        self.passed_checks = 0
        self.warnings: List[str] = []
        self.errors: List[str] = []

    def record_check(self, name: str, passed: bool, message: str = ""):
        self.checks_run += 1
        if passed:
            self.passed_checks += 1
            logger.info("  [PASS] %s", name)
        else:
            self.errors.append(f"{name}: {message}")
            logger.error("  [FAIL] %s: %s", name, message)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "checks_run": self.checks_run,
            "passed_checks": self.passed_checks,
            "failed_checks": len(self.errors),
            "status": "PASS" if not self.errors else "FAIL",
            "errors": self.errors,
            "warnings": self.warnings,
        }

def validate_pipeline_data(entities: Dict[str, List[Any]]) -> ValidationReport:
    """
    Executes mandatory data quality and integrity checks.
    Fails loudly by raising PipelineValidationError if critical constraints are broken.
    """
    logger.info("Stage 3: Running rigorous data integrity validator...")
    report = ValidationReport()

    courses: List[Course] = entities.get("courses", [])
    prereqs: List[PrerequisiteEdge] = entities.get("prerequisite_edges", [])
    skills: List[Skill] = entities.get("skills", [])
    course_skills: List[CourseSkillLink] = entities.get("course_skill_links", [])
    rules: List[AcademicRule] = entities.get("academic_rules", [])
    resources: List[Resource] = entities.get("resources", [])
    modules: List[ModuleLesson] = entities.get("modules_lessons", [])
    exercises: List[Exercise] = entities.get("exercises", [])

    course_codes = set()
    duplicate_codes = set()
    for c in courses:
        if c.code in course_codes:
            duplicate_codes.add(c.code)
        course_codes.add(c.code)

    # 1. Check for Duplicate Course Codes
    report.record_check(
        "No Duplicate Course Codes",
        len(duplicate_codes) == 0,
        f"Found duplicate course codes: {duplicate_codes}"
    )

    # 2. Check for Non-Numeric or Non-Positive Credits
    invalid_credits = [c.code for c in courses if not isinstance(c.credits, (int, float)) or c.credits <= 0]
    report.record_check(
        "Valid Positive Numeric Credits",
        len(invalid_credits) == 0,
        f"Courses with invalid credits: {invalid_credits}"
    )

    # 3. Check for Missing Source URLs across all entities
    missing_urls = []
    for c in courses:
        if not c.source_url or not c.source_url.startswith("http"):
            missing_urls.append(f"Course {c.code}")
    for p in prereqs:
        if not p.source_url or not p.source_url.startswith("http"):
            missing_urls.append(f"Prereq {p.course}->{p.requires}")
    for r in rules:
        if not r.source_url or not r.source_url.startswith("http"):
            missing_urls.append(f"Rule {r.id}")
    for res in resources:
        if not res.source_url or not res.source_url.startswith("http"):
            missing_urls.append(f"Resource {res.id}")
    for s in skills:
        if not s.source_url or not s.source_url.startswith("http"):
            missing_urls.append(f"Skill {s.id}")

    report.record_check(
        "All Records Have Valid Source URLs",
        len(missing_urls) == 0,
        f"Entities missing valid source URLs: {missing_urls[:10]}"
    )

    # 4. Check for Prerequisite Referring to Missing Course
    missing_prereq_refs = []
    for edge in prereqs:
        if edge.course not in course_codes:
            missing_prereq_refs.append(f"Dependent course '{edge.course}' does not exist in course catalog")
        if edge.requires not in course_codes:
            missing_prereq_refs.append(f"Required prerequisite course '{edge.requires}' does not exist in course catalog")

    report.record_check(
        "Prerequisites Reference Existing Courses",
        len(missing_prereq_refs) == 0,
        f"Missing prerequisite references: {missing_prereq_refs}"
    )

    # 5. Check for Prerequisite Cycles (DAG Acyclicity via NetworkX)
    dag = nx.DiGraph()
    for c in courses:
        dag.add_node(c.code)
    for edge in prereqs:
        # Edge from prerequisite to dependent course: requires -> course
        dag.add_edge(edge.requires, edge.course)

    is_dag = nx.is_directed_acyclic_graph(dag)
    cycles = []
    if not is_dag:
        cycles = list(nx.simple_cycles(dag))

    report.record_check(
        "Prerequisite Graph is Directed Acyclic Graph (DAG) with No Cycles",
        is_dag,
        f"Detected cycle(s) in prerequisite dependency graph: {cycles}"
    )

    # 6. Check for Course-Skill Referential Integrity
    skill_ids = {s.id for s in skills}
    missing_skill_refs = []
    for cs in course_skills:
        if cs.course not in course_codes:
            missing_skill_refs.append(f"Course '{cs.course}' in course_skill_links not in catalog")
        if cs.skill not in skill_ids:
            missing_skill_refs.append(f"Skill '{cs.skill}' in course_skill_links not in skills list")

    report.record_check(
        "Course-Skill Links Referential Integrity",
        len(missing_skill_refs) == 0,
        f"Broken course-skill links: {missing_skill_refs}"
    )

    # 7. Check for Minimum Threshold Requirements
    report.record_check(
        "Course Catalog Volume Meets Brief (>= 15 courses)",
        len(courses) >= 15,
        f"Only {len(courses)} courses collected (minimum 15 required)"
    )

    report.record_check(
        "Open Educational Resources Volume Meets Brief (>= 30 resources)",
        len(resources) >= 30,
        f"Only {len(resources)} resources collected (minimum 30 required)"
    )

    report.record_check(
        "Academic Rules Volume Meets Brief (>= 4 key rules)",
        len(rules) >= 4,
        f"Only {len(rules)} academic rules collected"
    )

    # 8. Check for Parent Existence in Modules
    resource_ids = {res.id for res in resources}
    valid_parents = course_codes.union(resource_ids)
    orphan_modules = [m.id for m in modules if m.parent_id not in valid_parents]
    report.record_check(
        "Module Lessons Have Valid Parent References",
        len(orphan_modules) == 0,
        f"Modules with non-existent parent IDs: {orphan_modules}"
    )

    # Fail loudly if any error was caught
    if report.errors:
        error_summary = "\n  - " + "\n  - ".join(report.errors)
        raise PipelineValidationError(
            f"Pipeline validation failed with {len(report.errors)} fatal errors:{error_summary}"
        )

    logger.info("All %d validation checks passed successfully!", report.checks_run)
    return report

