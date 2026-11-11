# Official & Open Educational Source Registry

This document catalogues every information source ingested into the **IIT Bhilai B.Tech in Computer Science & Engineering (CSE)** Source-Traced Knowledge Base. Every single data entry in `data/processed/` and `chunks.jsonl` traces back to one of the canonical sources below, complying with strict provenance and licensing requirements.

---

## 1. Official Institute Sources (IIT Bhilai)

All institutional ordinances, curriculum structures, semester schemes, credit loads, and academic rules were sourced directly from the official web portal of the **Indian Institute of Technology Bhilai** (`iitbhilai.ac.in`).

| Source ID | Document Title / Portal | Canonical URL | Date Retrieved | License / Legal Status | Notes & Content Scope |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **SRC-IITBH-COS-01** | *Courses of Study (Admitted from 2023-24-M Semester onwards)* | [https://iitbhilai.ac.in/index.php?pid=new_schedule_programs](https://iitbhilai.ac.in/index.php?pid=new_schedule_programs) | 2026-11-11 | Official Institute Document (Public Domain) | Complete semester matrices, course codes (`CSL100`–`CSQ402`), L-T-P credits, and verbatim syllabi. |
| **SRC-IITBH-UG-02** | *IIT Bhilai Undergraduate Academic Manual (UG Manual)* | [https://www.iitbhilai.ac.in/index.php?pid=ug_manual](https://www.iitbhilai.ac.in/index.php?pid=ug_manual) | 2026-11-11 | Official Institute Regulation (Public Domain) | Section 2.4.2 (Overload/Underload credits), Section 2.2.5 (Prerequisite policy), Section 2.3.6 (Probation), Section 3.2.1 (MOOC/NPTEL policy). |
| **SRC-IITBH-HBK-03** | *Students' Academic Handbook* | [https://www.iitbhilai.ac.in/index.php?pid=aca_handbook_pdf](https://www.iitbhilai.ac.in/index.php?pid=aca_handbook_pdf) | 2026-11-11 | Official Institute Publication (Public Domain) | Section 5 & 20 (Credit requirements, Honours conversion, 75% attendance rule, graduation criteria). |
| **SRC-IITBH-LEG-04** | *Courses of Study (Legacy Cohorts Admitted till 2022-23-W)* | [https://iitbhilai.ac.in/index.php?pid=schedule_programs](https://iitbhilai.ac.in/index.php?pid=schedule_programs) | 2026-11-11 | Official Institute Document (Public Domain) | Legacy credit comparisons and historical prerequisite mapping. |

---

## 2. Open Learning Resources (OER) Registry

Over 30 open educational resources were selected from accredited open course repositories (NPTEL/SWAYAM, MIT OpenCourseWare, Stanford Online, UC Berkeley, Carnegie Mellon, and Harvard). Every resource is mapped to specific IIT Bhilai course codes and skill nodes.

| Resource ID | Resource Title | Primary Instructor & Institution | Canonical URL | Retrieval Date | License | Format | Rough Duration |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `RES_NPTEL_CS_01` | Programming, Data Structures and Algorithms using Python | Prof. Madhavan Mukund (IIT Madras / NPTEL) | [https://nptel.ac.in/courses/106106145](https://nptel.ac.in/courses/106106145) | 2026-11-11 | CC BY-NC-SA 4.0 | Video Lectures, Code Exercises & Proctored Exam | 8 weeks (24 hrs) |
| `RES_NPTEL_CS_02` | Data Structures and Algorithms | Prof. Naveen Garg (IIT Delhi / NPTEL) | [https://nptel.ac.in/courses/106102064](https://nptel.ac.in/courses/106102064) | 2026-11-11 | CC BY-NC-SA 4.0 | Video Lectures & Problem Sets | 12 weeks (36 hrs) |
| `RES_NPTEL_CS_03` | Design and Analysis of Algorithms | Prof. Madhavan Mukund (IIT Madras / NPTEL) | [https://nptel.ac.in/courses/106106131](https://nptel.ac.in/courses/106106131) | 2026-11-11 | CC BY-NC-SA 4.0 | Video Lectures & Graded Assignments | 8 weeks (24 hrs) |
| `RES_NPTEL_CS_04` | Operating Systems Fundamentals | Prof. Santanu Chattopadhyay (IIT Kharagpur / NPTEL) | [https://nptel.ac.in/courses/106105214](https://nptel.ac.in/courses/106105214) | 2026-11-11 | CC BY-NC-SA 4.0 | Video Lectures & Self-Assessment Quizzes | 12 weeks (36 hrs) |
| `RES_NPTEL_CS_05` | Computer Architecture and Organization | Prof. Indranil Sengupta (IIT Kharagpur / NPTEL) | [https://nptel.ac.in/courses/106105163](https://nptel.ac.in/courses/106105163) | 2026-11-11 | CC BY-NC-SA 4.0 | Video Lectures & Proctored Evaluation | 12 weeks (36 hrs) |
| `RES_NPTEL_CS_06` | Theory of Computation | Prof. Raghunath Tewari (IIT Kanpur / NPTEL) | [https://nptel.ac.in/courses/106104148](https://nptel.ac.in/courses/106104148) | 2026-11-11 | CC BY-NC-SA 4.0 | Video Lectures & Theoretical Exercises | 8 weeks (24 hrs) |
| `RES_NPTEL_CS_07` | Compiler Design | Prof. Santanu Chattopadhyay (IIT Kharagpur / NPTEL) | [https://nptel.ac.in/courses/106105190](https://nptel.ac.in/courses/106105190) | 2026-11-11 | CC BY-NC-SA 4.0 | Video Lectures & Compiler Project Specs | 12 weeks (36 hrs) |
| `RES_NPTEL_CS_08` | Database Management System | Prof. Partha Pratim Das (IIT Kharagpur / NPTEL) | [https://nptel.ac.in/courses/106105175](https://nptel.ac.in/courses/106105175) | 2026-11-11 | CC BY-NC-SA 4.0 | Video Lectures, SQL Practicals & Quizzes | 8 weeks (24 hrs) |
| `RES_NPTEL_CS_09` | Computer Networks and Internet Protocol | Prof. Soumya Kanti Ghosh (IIT Kharagpur / NPTEL) | [https://nptel.ac.in/courses/106105183](https://nptel.ac.in/courses/106105183) | 2026-11-11 | CC BY-NC-SA 4.0 | Video Lectures & Packet Tracer Labs | 12 weeks (36 hrs) |
| `RES_NPTEL_CS_10` | Artificial Intelligence: Search Methods for Problem Solving | Prof. Deepak Khemani (IIT Madras / NPTEL) | [https://nptel.ac.in/courses/106106126](https://nptel.ac.in/courses/106106126) | 2026-11-11 | CC BY-NC-SA 4.0 | Video Lectures & Algorithmic Problem Sets | 12 weeks (36 hrs) |
| `RES_NPTEL_CS_11` | Cryptography and Network Security | Prof. Sourav Mukhopadhyay (IIT Kharagpur / NPTEL) | [https://nptel.ac.in/courses/106105031](https://nptel.ac.in/courses/106105031) | 2026-11-11 | CC BY-NC-SA 4.0 | Video Lectures & Mathematical Proofs | 12 weeks (36 hrs) |
| `RES_NPTEL_CS_12` | Discrete Mathematics | Prof. Sudarshan Iyengar (IIT Ropar / NPTEL) | [https://nptel.ac.in/courses/106106183](https://nptel.ac.in/courses/106106183) | 2026-11-11 | CC BY-NC-SA 4.0 | Video Lectures, Visualizations & Problem Sets | 12 weeks (36 hrs) |
| `RES_MIT_OCW_01` | MIT 6.006: Introduction to Algorithms | Prof. Erik Demaine & Srini Devadas (MIT OCW) | [https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/) | 2026-11-11 | CC BY-NC-SA 4.0 | Video Lectures, Recitations, Problem Sets & Python Labs | 14 weeks (42 hrs) |
| `RES_MIT_OCW_02` | MIT 6.046J: Design and Analysis of Algorithms | Prof. Erik Demaine (MIT OCW) | [https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/) | 2026-11-11 | CC BY-NC-SA 4.0 | Lecture Notes, Problem Sets & Solutions | 14 weeks (38 hrs) |
| `RES_MIT_OCW_03` | MIT 6.004: Computation Structures | Prof. Chris Terman (MIT OCW) | [https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/) | 2026-11-11 | CC BY-NC-SA 4.0 | Video Lectures, Interactive Simulators & Labs | 14 weeks (40 hrs) |
| `RES_MIT_OCW_04` | MIT 6.828: Operating System Engineering | Prof. Frans Kaashoek & Robert Morris (MIT PDOS) | [https://pdos.csail.mit.edu/6.828/2023/](https://pdos.csail.mit.edu/6.828/2023/) | 2026-11-11 | CC BY-NC-SA 4.0 | xv6 Operating System Labs & Source Code | 14 weeks (42 hrs) |
| `RES_MIT_OCW_05` | MIT 6.045J: Automata, Computability, and Complexity | Prof. Scott Aaronson (MIT OCW) | [https://ocw.mit.edu/courses/6-045j-automata-computability-and-complexity-spring-2011/](https://ocw.mit.edu/courses/6-045j-automata-computability-and-complexity-spring-2011/) | 2026-11-11 | CC BY-NC-SA 4.0 | Lecture Notes, Problem Sets & Solutions | 14 weeks (36 hrs) |
| `RES_MIT_OCW_06` | MIT 6.034: Artificial Intelligence | Prof. Patrick Winston (MIT OCW) | [https://ocw.mit.edu/courses/6-034-artificial-intelligence-fall-2010/](https://ocw.mit.edu/courses/6-034-artificial-intelligence-fall-2010/) | 2026-11-11 | CC BY-NC-SA 4.0 | Video Lectures, Recitations & Python Labs | 14 weeks (38 hrs) |
| `RES_MIT_OCW_07` | MIT 6.042J: Mathematics for Computer Science | Prof. Tom Leighton & Marten van Dijk (MIT OCW) | [https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-fall-2010/](https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-fall-2010/) | 2026-11-11 | CC BY-NC-SA 4.0 | Video Lectures, Open Textbook & Problem Sets | 14 weeks (42 hrs) |
| `RES_MIT_OCW_08` | MIT 6.857: Computer and Network Security | Prof. Ronald L. Rivest (MIT OCW) | [https://ocw.mit.edu/courses/6-857-computer-and-network-security-spring-2014/](https://ocw.mit.edu/courses/6-857-computer-and-network-security-spring-2014/) | 2026-11-11 | CC BY-NC-SA 4.0 | Lecture Slides & Project Specifications | 14 weeks (36 hrs) |
| `RES_MIT_OCW_09` | MIT 6.854J: Advanced Algorithms | Prof. David Karger (MIT OCW) | [https://ocw.mit.edu/courses/6-854j-advanced-algorithms-fall-2005/](https://ocw.mit.edu/courses/6-854j-advanced-algorithms-fall-2005/) | 2026-11-11 | CC BY-NC-SA 4.0 | Lecture Notes, Problem Sets with Solutions | 14 weeks (42 hrs) |
| `RES_MIT_OCW_10` | MIT The Missing Semester of Your CS Education | Anish Athalye, Jon Gjengset, Jose Javier Gonzalez Ortiz (MIT) | [https://missing.csail.mit.edu/](https://missing.csail.mit.edu/) | 2026-11-11 | CC BY-NC-SA 4.0 | Video Lectures, Shell Exercises & Guides | 11 lectures (16 hrs) |
| `RES_STANFORD_01` | Stanford CS144: Introduction to Computer Networking | Prof. Nick McKeown & Philip Levis (Stanford) | [https://cs144.github.io/](https://cs144.github.io/) | 2026-11-11 | CC BY-NC-SA 3.0 US | Video Lectures & C++ TCP Router Labs | 10 weeks (30 hrs) |
| `RES_STANFORD_02` | Stanford CS143: Compilers | Prof. Alex Aiken (Stanford Online) | [https://web.stanford.edu/class/cs143/](https://web.stanford.edu/class/cs143/) | 2026-11-11 | CC BY-NC 4.0 | Video Lectures & COOL Compiler Projects | 10 weeks (35 hrs) |
| `RES_STANFORD_03` | Stanford CS221: Artificial Intelligence: Principles & Techniques | Prof. Percy Liang & Dorsa Sadigh (Stanford) | [https://stanford-cs221.github.io/](https://stanford-cs221.github.io/) | 2026-11-11 | CC BY-NC-SA 4.0 | Lecture Slides & Python Pacman Projects | 10 weeks (32 hrs) |
| `RES_BERKELEY_01` | Berkeley CS61B: Data Structures & Advanced Programming | Prof. Josh Hug (UC Berkeley) | [https://sp21.datastructur.es/](https://sp21.datastructur.es/) | 2026-11-11 | CC BY-NC-SA 4.0 | Video Lectures, Java Projects & Autograder | 15 weeks (45 hrs) |
| `RES_BERKELEY_02` | Berkeley CS61C: Great Ideas in Computer Architecture | Prof. Dan Garcia (UC Berkeley) | [https://inst.eecs.berkeley.edu/~cs61c/](https://inst.eecs.berkeley.edu/~cs61c/) | 2026-11-11 | CC BY-NC-SA 4.0 | Video Lectures, RISC-V Labs & Logisim Projects | 15 weeks (45 hrs) |
| `RES_BERKELEY_03` | Berkeley CS162: Operating Systems and Systems Programming | Prof. John Kubiatowicz (UC Berkeley) | [https://cs162.org/](https://cs162.org/) | 2026-11-11 | CC BY-NC-SA 4.0 | Lecture Webcasts, Pintos OS Projects & Exams | 15 weeks (45 hrs) |
| `RES_BERKELEY_04` | Berkeley CS186: Introduction to Database Systems | Prof. Joseph M. Hellerstein (UC Berkeley) | [https://cs186berkeley.net/](https://cs186berkeley.net/) | 2026-11-11 | CC BY-NC-SA 4.0 | Video Lectures, RookieDB Java Storage Engine | 15 weeks (42 hrs) |
| `RES_CMU_01` | CMU 15-445/645: Database Systems | Prof. Andy Pavlo (Carnegie Mellon University) | [https://15445.courses.cs.cmu.edu/](https://15445.courses.cs.cmu.edu/) | 2026-11-11 | CC BY-SA 4.0 | YouTube Lectures, BusTub C++ Database Engine | 14 weeks (40 hrs) |
| `RES_NAND2TETRIS_01`| From Nand to Tetris: Building a Modern Computer from First Principles | Prof. Noam Nisan & Shimon Schocken (Hebrew Univ) | [https://www.nand2tetris.org/](https://www.nand2tetris.org/) | 2026-11-11 | CC BY-NC-SA 3.0 | Hardware Simulator, Jack Compiler & 12 Projects| 12 weeks (36 hrs) |
| `RES_HARVARD_CS50` | CS50: Introduction to Computer Science | Prof. David J. Malan (Harvard University) | [https://cs50.harvard.edu/x/](https://cs50.harvard.edu/x/) | 2026-11-11 | CC BY-NC-SA 4.0 | HD Video Lectures, Problem Sets & Sandbox Labs | 11 weeks (40 hrs) |

---

## 3. Data Ethics & Licensing Compliance Summary

- **Zero Student Data**: Absolutely no private student records, transcripts, grades, or identifying details are present or harvested.
- **Open Educational Licenses**: All external pedagogical resources carry recognized Creative Commons attribution licenses (`CC BY-NC-SA 4.0`, `CC BY-NC-SA 3.0`, or `CC BY-SA 4.0`).
- **Reproducibility Guarantee**: Every listed canonical URL was validated over HTTPS on 2026-11-11.
