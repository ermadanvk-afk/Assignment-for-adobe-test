# Adobe PS 1-Day Selection Assignment — Submission Summary

**Candidate Repository**: [https://github.com/ermadanvk-afk/Assignment-for-adobe-test](https://github.com/ermadanvk-afk/Assignment-for-adobe-test)  
**Live Production Web Application**: [https://adobe-hazel.vercel.app/](https://adobe-hazel.vercel.app/)  
**Selected Institute & Programme**: Indian Institute of Technology Bhilai (IIT Bhilai) — B.Tech in Computer Science and Engineering (CSE)  
**Curriculum Cohort**: 2023-24 Academic Session onwards (governed by IIT Bhilai Senate & DUGC)  

---

## 🔗 Quick Access Links

| Asset | Link | Description |
| :--- | :--- | :--- |
| **🚀 Live Interactive UI** | **[https://adobe-hazel.vercel.app/](https://adobe-hazel.vercel.app/)** | Hosted on Vercel: Interactive DAG visualizer, Rules simulator & Chunks inspector |
| **📂 GitHub Repository** | **[Assignment-for-adobe-test](https://github.com/ermadanvk-afk/Assignment-for-adobe-test)** | Full source code, test suite, and git commit history |
| **📑 Part D: Data Quality Report** | [`DATA_QUALITY_REPORT.md`](./DATA_QUALITY_REPORT.md) | 1-page completeness audit, 10 automated validator checks & verification protocol |
| **💡 Part E: Ideas Note** | [`IDEAS.md`](./IDEAS.md) | 1-page note: Hybrid Graph-RAG design, 3 questions answered vs. 3 questions not |
| **🔗 Sources & Licenses** | [`SOURCES.md`](./SOURCES.md) | Provenance table listing official URLs, retrieval timestamps & CC licenses |
| **📦 Ready Chunks File** | [`chunks.jsonl`](./chunks.jsonl) | 130 semantic retrieval chunks ready for Day-2 embedding |

---

## 📊 Summary of Pipeline Execution & Data Volume

```text
======================================================================
 IIT BHILAI B.TECH CSE KNOWLEDGE BASE & PIPELINE AUDIT
======================================================================
  • Course Catalogue:             27 Courses (Requirement: >= 15 | Exceeded +80%)
  • Prerequisite Edges:           24 Edges (Strictly Acyclic DAG verified)
  • Academic Regulations:         15 Rules (Separate quotable entries with numeric constraints)
  • Open Learning Resources:      32 Resources (Requirement: >= 30 | NPTEL, MIT OCW, Berkeley)
  • Skills & Competencies:        28 Taxonomy nodes
  • Course-Skill Links:           32 Links
  • Resource-Skill Links:         57 Links
  • Curriculum Modules:           24 Granular units
  • Practice Exercises:           5 Problems (With answer rubrics & difficulty tiers)
  • Retrieval Chunks:             130 Chunks in chunks.jsonl (Day-2 embedding ready)
  • Automated Validator:          10/10 Checks PASS (0 Errors)
  • Field Completeness:           100.0% in Courses, Rules, Resources, and Chunks
  • Automated Test Suite:         6/6 Pytest tests passing in 2.3s
======================================================================
```

---

## 🛠️ How to Verify & Run Locally

```bash
# 1. Clone repository
git clone https://github.com/ermadanvk-afk/Assignment-for-adobe-test.git
cd Assignment-for-adobe-test

# 2. Install Python dependencies
pip install pydantic networkx pytest

# 3. Run end-to-end pipeline in one command
python run_pipeline.py

# 4. Run automated test suite
python -m pytest tests/ -v

# 5. Launch web UI locally
cd ui
npm install
npm run dev
# Open http://localhost:3000 in your browser
```
