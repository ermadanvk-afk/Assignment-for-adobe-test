"""Pydantic schemas defining the strongly typed entities of the IIT Bhilai Knowledge Graph."""

from enum import Enum
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, field_validator, HttpUrl

class SourceType(str, Enum):
    OFFICIAL = "official"
    OPEN_LICENCE = "open-licence"
    MANUAL = "manual"

class PrerequisiteKind(str, Enum):
    HARD = "hard"
    RECOMMENDED = "recommended"

class SkillLevel(str, Enum):
    INTRODUCTORY = "introductory"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class SkillDepth(str, Enum):
    INTRO = "intro"
    WORKING = "working"
    ADVANCED = "advanced"

class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class Course(BaseModel):
    code: str = Field(..., description="Unique course identifier code (e.g. CSL202)")
    title: str = Field(..., description="Full title of the course")
    dept: str = Field(..., description="Offering academic department")
    credits: float = Field(..., gt=0, description="Total academic credit value")
    lecture_tutorial_practical: Optional[str] = Field(None, description="L-T-P credit structure breakdown")
    semester_offered: int = Field(..., ge=1, le=8, description="Standard curriculum semester offered (1-8)")
    type: str = Field(..., description="Category: Institute Core, Program Core, Program Elective, Program Linked, Capstone")
    mode: str = Field(..., description="Instructional delivery mode (e.g. Lecture + Practical)")
    objectives: str = Field(..., min_length=20, description="Syllabus topics and key learning objectives")
    source_url: str = Field(..., description="Authoritative origin URL")
    retrieved_on: str = Field(..., description="ISO 8601 retrieval date")
    source_type: SourceType = Field(default=SourceType.OFFICIAL, description="Type of source")

    @field_validator("code")
    @classmethod
    def clean_course_code(cls, v: str) -> str:
        return v.strip().upper()

class PrerequisiteEdge(BaseModel):
    course: str = Field(..., description="Target course code requiring the prerequisite")
    requires: str = Field(..., description="Prerequisite course code that must be cleared")
    kind: PrerequisiteKind = Field(default=PrerequisiteKind.HARD, description="Hard mandatory or recommended precedent")
    source_url: str = Field(..., description="Source document URL")
    retrieved_on: str = Field(..., description="ISO 8601 retrieval date")
    source_type: SourceType = Field(default=SourceType.OFFICIAL)

    @field_validator("course", "requires")
    @classmethod
    def clean_codes(cls, v: str) -> str:
        return v.strip().upper()

class Skill(BaseModel):
    id: str = Field(..., description="Unique skill identifier (e.g. SKILL_TREES_AND_HEAPS)")
    name: str = Field(..., description="Human-readable skill competency title")
    level: SkillLevel = Field(..., description="Competency tier")
    parent_skill: Optional[str] = Field(None, description="Parent skill ID in competency taxonomy")
    source_url: str = Field(..., description="Source reference URL")
    retrieved_on: str = Field(..., description="ISO 8601 retrieval date")
    source_type: SourceType = Field(default=SourceType.OFFICIAL)

class CourseSkillLink(BaseModel):
    course: str = Field(..., description="Course code")
    skill: str = Field(..., description="Target skill ID")
    depth: SkillDepth = Field(..., description="Depth of skill coverage in this course")

    @field_validator("course")
    @classmethod
    def clean_course(cls, v: str) -> str:
        return v.strip().upper()

class AcademicRule(BaseModel):
    id: str = Field(..., description="Unique rule identifier (e.g. RULE_CREDIT_OVERLOAD_MAX)")
    category: str = Field(..., description="Rule taxonomy category: Credit Limits, Prerequisites, Minor/Honours, MOOC")
    text: str = Field(..., min_length=20, description="Exact quotable regulation text from manual/ordinances")
    numeric_limit: Optional[float] = Field(None, description="Quantitative limit if applicable (e.g. 21.0 credits, 4.5 SGPA)")
    applies_to: str = Field(..., description="Target student population / cohort affected")
    source_url: str = Field(..., description="Official manual or ordinance URL")
    retrieved_on: str = Field(..., description="ISO 8601 retrieval date")
    source_type: SourceType = Field(default=SourceType.OFFICIAL)

class Resource(BaseModel):
    id: str = Field(..., description="Unique resource identifier (e.g. RES_NPTEL_CS_02)")
    title: str = Field(..., description="Title of educational resource")
    provider: str = Field(..., description="Originating institution/platform (e.g. NPTEL / IIT Delhi, MIT OCW)")
    licence: str = Field(..., description="Open licensing terms (e.g. CC BY-NC-SA 4.0)")
    format: str = Field(..., description="Delivery media format (e.g. Video Lectures & Labs)")
    duration: str = Field(..., description="Approximate course duration/workload (e.g. 12 weeks / 36 hours)")
    url: str = Field(..., description="Direct public URL")
    source_url: str = Field(..., description="Provenance verification URL")
    retrieved_on: str = Field(..., description="ISO 8601 retrieval date")
    source_type: SourceType = Field(default=SourceType.OPEN_LICENCE)

class ResourceSkillLink(BaseModel):
    resource: str = Field(..., description="Resource ID")
    skill: str = Field(..., description="Skill ID supported by the resource")
    level: SkillLevel = Field(..., description="Level taught in resource")

class ModuleLesson(BaseModel):
    id: str = Field(..., description="Unique module identifier (e.g. MOD_CS202_01)")
    parent_id: str = Field(..., description="Parent course code or resource ID")
    order: int = Field(..., ge=1, description="Sequence position in curriculum")
    title: str = Field(..., description="Module/unit title")
    summary: str = Field(..., description="Detailed concepts and topics covered in module")

class Exercise(BaseModel):
    id: str = Field(..., description="Unique exercise identifier (e.g. EX_DSA_01)")
    skill: str = Field(..., description="Skill ID evaluated by this exercise")
    difficulty: DifficultyLevel = Field(..., description="Cognitive difficulty tier")
    question: str = Field(..., description="Problem description or challenge")
    answer_key: str = Field(..., description="Reference answer and evaluation rubric")

class Chunk(BaseModel):
    chunk_id: str = Field(..., description="Globally unique chunk identifier")
    parent_id: str = Field(..., description="Originating entity identifier (course, rule, resource, module)")
    parent_type: str = Field(..., description="Type of entity: course, academic_rule, resource, module, exercise")
    chunk_type: str = Field(..., description="Specific text role: syllabus_unit, rule_statement, resource_overview, exercise_problem")
    text: str = Field(..., description="Clean, retrieval-optimized text segment")
    filter_metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata key-value pairs for vector DB filtering")
    source_url: str = Field(..., description="Direct citation URL for traceability")
    retrieved_on: str = Field(..., description="ISO 8601 retrieval date")

