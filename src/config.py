"""Configuration constants and filesystem paths for the IIT Bhilai B.Tech CSE Data Pipeline."""

from pathlib import Path

# Base Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
CHUNKS_JSONL_PATH = PROJECT_ROOT / "chunks.jsonl"
PROCESSED_CHUNKS_PATH = PROCESSED_DATA_DIR / "chunks.jsonl"
DATA_SUMMARY_PATH = PROCESSED_DATA_DIR / "data_summary.json"

# Raw Source Files
RAW_SEED_CATALOGUE = RAW_DATA_DIR / "raw_seed_catalogue.json"
RAW_COURSES_PDF = RAW_DATA_DIR / "iit_bhilai_courses_of_study_new.pdf"
RAW_UG_MANUAL_PDF = RAW_DATA_DIR / "iit_bhilai_ug_manual.pdf"
RAW_HANDBOOK_PDF = RAW_DATA_DIR / "iit_bhilai_handbook.pdf"

# Default Metadata
CURRENT_RETRIEVAL_DATE = "2026-11-11"
INSTITUTE_NAME = "Indian Institute of Technology Bhilai"
PROGRAM_NAME = "B.Tech in Computer Science and Engineering"
DEFAULT_SOURCE_URL = "https://iitbhilai.ac.in/index.php?pid=new_schedule_programs"
UG_MANUAL_SOURCE_URL = "https://www.iitbhilai.ac.in/index.php?pid=ug_manual"
