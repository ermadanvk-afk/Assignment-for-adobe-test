# Part E: Ideas Note — Leveraging the Knowledge Base for an Academic Buddy

Building an intelligent student advisor requires moving beyond unstructured text search. Academic advising is governed by rigid deterministic constraints (prerequisite DAGs, credit caps, probation thresholds) combined with rich educational content (syllabi, competencies, and open learning pathways). Below is our blueprint for how this source-traced dataset empowers an autonomous Academic Buddy.

---

## 1. System Architecture: Hybrid Graph-RAG Retrieval

Rather than relying purely on vector similarity—which frequently hallucinates constraint logic—the buddy uses a **Hybrid Graph-RAG Architecture**:
1. **Deterministic Reasoning Layer (Knowledge Graph)**: Modeled using the entities exported in `data/processed/` (`courses`, `prerequisite_edges`, `skills`, `academic_rules`). Graph traversals evaluate prerequisite chains, compute topological course schedules, and test constraint satisfaction without LLM speculation.
2. **Dense Semantic Retrieval Layer (Vector DB)**: Consuming `chunks.jsonl`, dense vector search retrieves fine-grained syllabus definitions, learning outcomes, and pedagogic recommendations mapped to student interests.
3. **Deterministic Constraint Engine**: When an academic decision is required, the rules engine audits student inputs against quotable regulations (`numeric_limit`, `category`, `applies_to`) and cites the official ordinance verbatim.

---

## 2. Three Student Questions the Buddy Can Answer Exceptionally Well

### Question 1: Prerequisite Impact & Semester Planning Under Failure
> **"I received an F grade in CSL202 (Data Structures) in Semester 3. Can I register for CSL252 (Algorithms) or CSL301 (Operating Systems) in Semester 4, and how do credit limits affect my recovery plan?"**

- **Why the buddy excels**:
  - The buddy queries the prerequisite DAG and finds that `CSL202` is a **hard prerequisite** for both `CSL252` (Design and Analysis of Algorithms) and `CSL301` (Operating Systems).
  - It quotes **Rule `RULE_PREREQUISITE_CLEARANCE`** (UG Manual §2.2.5): *"A precedent course defined as a prerequisite must be cleared before the dependent course can be taken."* Hence, the student is blocked from registering for either course.
  - It queries **Rule `RULE_CREDIT_UNDERLOAD_MIN`** and **`RULE_CREDIT_OVERLOAD_MAX`** (UG Manual §2.4.2), explaining that the student must maintain at least 15 credits in Semester 4, suggests clearing `CSL202` at the earliest offering, and notes that later semesters allow overload up to 21 credits with DUGC convener approval.

### Question 2: MOOC / NPTEL Credit Transfer & Policy Compliance
> **"Can I take an advanced 12-week NPTEL course in Machine Learning and transfer 3 credits toward my B.Tech CSE elective requirements?"**

- **Why the buddy excels**:
  - The buddy cites **Rule `RULE_NPTEL_MAX_CREDITS`** (UG Manual §3.2.1), verifying that students can credit up to 6 credits across their entire UG curriculum.
  - It cites **Rule `RULE_NPTEL_EQUIVALENCE_DURATION`**: A 14-week/42-hour MOOC equates to 3 credits at IIT Bhilai (and explains whether a 12-week course satisfies or requires departmental approval).
  - It outlines the mandatory procedural steps: request must be submitted prior to course start, DUGC convener serves as instructor-in-charge, course code will be designated as `CSL495`, and the proctored grade counts directly toward CGPA calculation (**Rule `RULE_NPTEL_GRADING_PROCEDURE`**).

### Question 3: Skill Gap Analysis & Self-Paced Remediation
> **"I want to prepare for CSL301 (Operating Systems) over the summer. What specific competencies will I need, and what open resources should I study?"**

- **Why the buddy excels**:
  - Traverses the knowledge graph from `CSL301` to its linked skills: `SKILL_MEMORY_HIERARCHY`, `SKILL_OS_CONCURRENCY`, and `SKILL_FILE_SYSTEMS`.
  - Recommends the exact mapped open learning resources: **MIT 6.828 Operating System Engineering** (`RES_MIT_OCW_04`, hands-on xv6 labs), **Berkeley CS162** (`RES_BERKELEY_03`), and **NPTEL Operating Systems Fundamentals** (`RES_NPTEL_CS_04`).
  - Provides practice mastery check problems directly from `exercises.json` (`EX_OS_03`: Coffman deadlock conditions & Banker's algorithm).

---

## 3. Three Student Questions the Buddy CANNOT Answer (and Why)

### Question 1: Real-Time Faculty Allotment & Timetable Conflicts
> **"Who is instructing CSL302 (Compiler Design) next Tuesday at 10:00 AM, and what is their attendance leniency?"**

- **Why it cannot answer**: The dataset models immutable curricula, syllabi, and official ordinances, not dynamic semester timetables, classroom scheduling spreadsheets, or confidential faculty teaching assignments. Subjective impressions of faculty leniency are intentionally excluded on ethical grounds.

### Question 2: Individual Financial Aid, Hostel Allotments & Fee Waivers
> **"Has my semester tuition fee waiver been approved by the institute, and can I get a single-occupancy hostel room?"**

- **Why it cannot answer**: Protecting student privacy (Data Ethics Ground Rule) forbids storing real student identifiers, financial records, income certificates, or ERP transaction histories. The buddy can cite award eligibility guidelines (`P.K. Jain Memorial Award` in `academic_rules`), but cannot inspect live accounts.

### Question 3: Discretionary Exam Accommodations & Ad-hoc Petitions
> **"If I miss my mid-semester exam for an external hackathon, will the department conduct a makeup exam for me?"**

- **Why it cannot answer**: While the buddy can cite **Rule `RULE_MINIMUM_ATTENDANCE`** (75% mandatory attendance) and **UG Manual §2.3.6** (prohibition of outside participation during academic probation), re-examination requests fall under the ad-hoc discretionary authority of individual course instructors and the Department Undergraduate Committee (DUGC). Static regulatory documents do not contain minutes of discretionary committee approvals.

