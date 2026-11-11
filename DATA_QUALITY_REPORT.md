# Part D: Data Quality & Provenance Audit Report

**Institute**: Indian Institute of Technology Bhilai (IIT Bhilai)  
**Program**: Bachelor of Technology (B.Tech) in Computer Science and Engineering  
**Audit Timestamp**: 2026-11-11  
**Pipeline Run Status**: **PASS (0 Errors, 10/10 Checks Passed)**  

---

## 1. Inventory of Ingested Entities & Chunks

All data artifacts were extracted from official institute publications (`iitbhilai.ac.in`) and open courseware repositories.

| Entity Type | Records Collected | Target Threshold | Status | Storage Location |
| :--- | :---: | :---: | :---: | :--- |
| **Course Catalogue** | **27** | $\ge 15$ | **Exceeded (+80%)** | `data/processed/courses.csv`, `courses.json` |
| **Prerequisite Edges** | **24** | $\ge 10$ | **Exceeded** | `data/processed/prerequisite_edges.csv`, `.json` |
| **Academic Rules** | **15** | $\ge 4$ | **Exceeded (+275%)** | `data/processed/academic_rules.csv`, `.json` |
| **Open Learning Resources** | **32** | $\ge 30$ | **Exceeded (+6.7%)** | `data/processed/resources.csv`, `.json` |
| **Skills & Competencies** | **28** | Taxonomy | **Complete** | `data/processed/skills.csv`, `.json` |
| **Course-Skill Links** | **32** | Cross-linked | **Complete** | `data/processed/course_skill_links.csv`, `.json` |
| **Resource-Skill Links** | **57** | Cross-linked | **Complete** | `data/processed/resource_skill_links.csv`, `.json` |
| **Curriculum Modules / Lessons** | **24** | Granular units | **Complete** | `data/processed/modules_lessons.csv`, `.json` |
| **Practice Exercises (Bonus)** | **5** | Self-assessment | **Complete** | `data/processed/exercises.csv`, `.json` |
| **Retrieval Chunks** | **130** | Embed-ready | **Complete** | `chunks.jsonl`, `data/processed/chunks.jsonl` |

---

## 2. Field Completeness Audit

Completeness measures the percentage of defined schema fields populated with valid, non-null, non-empty data.

| Entity Type | Total Attributes Evaluated | Filled Attributes | Completeness Rate | Notes |
| :--- | :---: | :---: | :---: | :--- |
| **Courses** | 324 | 324 | **100.0%** | Full coverage of code, title, credits, semester, syllabus, URL. |
| **Prerequisite Edges** | 144 | 144 | **100.0%** | All edges include course, prerequisite, kind, and source provenance. |
| **Skills** | 196 | 188 | **95.92%** | Unfilled slots represent root skills lacking a `parent_skill` by design. |
| **Course-Skill Links** | 96 | 96 | **100.0%** | 100% paired with depth indicators (`intro`, `working`, `advanced`). |
| **Academic Rules** | 120 | 118 | **98.33%** | Qualitative rules (e.g., registration window) omit `numeric_limit`. |
| **Open Resources** | 288 | 288 | **100.0%** | Title, provider, license, duration, format, and URL 100% populated. |
| **Resource-Skill Links** | 171 | 171 | **100.0%** | Fully linked to skills and difficulty tiers. |
| **Modules / Lessons** | 120 | 120 | **100.0%** | Sequential orders and concept summaries present. |
| **Practice Exercises** | 25 | 25 | **100.0%** | Questions, answer rubrics, and difficulty tiers populated. |
| **Retrieval Chunks** | 1,040 | 1,040 | **100.0%** | All chunks preserve parent ID, entity type, text, and filter metadata. |

---

## 3. Automated Validator Suite & Error Trapping

The validator (`src/validator.py`) runs 10 deterministic gates prior to exporting data. In testing and integration runs:

1. **Cycle Detection in Prerequisite Graph (DAG)**: Tested using NetworkX cycle algorithms. Catches any cyclic dependency (e.g. $A \to B \to A$) and immediately raises `PipelineValidationError`. The production catalog is verified strictly acyclic.
2. **Dangling Prerequisite Course Codes**: Verifies that both `edge.course` and `edge.requires` exist in the Course catalog. Caught test injection of nonexistent course `CSL999_GHOST`.
3. **Duplicate Course Code Protection**: Ensures uniqueness across primary keys (`code`).
4. **Credit Integrity Check**: Verifies that every course credit value is a strictly positive real number ($> 0$).
5. **Universal Provenance Assertion**: Ensures that every entity carries a valid, well-formed HTTPS `source_url` and retrieval timestamp (`2026-11-11`).
6. **Referential Integrity for Skills & Modules**: Guarantees all foreign keys in `course_skill_links`, `resource_skill_links`, and `modules_lessons` reference valid entities.

---

## 4. Missing or Uncertain Data Points

1. **Elective Course Seasonality**: While core courses have fixed semesters (Sem 1 to 6), advanced departmental electives (e.g., `CSL505 Cryptography`, `CSL510 Approximation Algorithms`) may rotate between Monsoon and Winter semesters depending on faculty availability.
2. **Open Elective (OE) Catalog Granularity**: IIT Bhilai allows students to satisfy OE requirements via cross-departmental courses (Mechanical, Electrical, Liberal Arts). These change each semester based on departmental scheduling and are treated as dynamic elective slots in the model.

---

## 5. Verification Protocol for Teammates (Sample Audit)

To independently verify the authenticity of any record:
1. **Course Verification**: Open `data/processed/courses.json`. Pick any course (e.g., `CSL301 Operating Systems`). Locate the `source_url` (`https://iitbhilai.ac.in/index.php?pid=new_schedule_programs`). Open the raw PDF in `data/raw/iit_bhilai_courses_of_study_new.pdf` and navigate to page 84 to verify the verbatim credits (4.0), L-T-P (3-0-2), prerequisites (`CSL202`, `CSL251`), and xv6 syllabus.
2. **Academic Rule Verification**: Pick rule `RULE_NPTEL_MAX_CREDITS`. Open `data/raw/iit_bhilai_ug_manual.pdf` at page 30, Section 3.2.1: verify that students are allowed to opt for a maximum of 6 credits from MOOC-based portals during their undergraduate program.
3. **Open Resource Verification**: Pick resource `RES_MIT_OCW_01`. Open the direct link `https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/` and verify that the course is published under Creative Commons `CC BY-NC-SA 4.0`.
4. **One-Command Automated Verification**: Run `python -m pytest tests/` in terminal to execute all 6 automated integration tests.

