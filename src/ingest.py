"""Ingest Stage: Safely load untouched raw files from data/raw/."""

import json
import logging
from pathlib import Path
from typing import Dict, Any

from src.config import (
    RAW_DATA_DIR,
    RAW_SEED_CATALOGUE,
    RAW_COURSES_PDF,
    RAW_UG_MANUAL_PDF,
    RAW_HANDBOOK_PDF,
)

logger = logging.getLogger("pipeline.ingest")

def ingest_raw_data() -> Dict[str, Any]:
    """
    Verifies untouched raw storage in data/raw/ and loads raw extracted payloads.
    Returns the unparsed dictionary structure for downstream normalization.
    """
    logger.info("Stage 1: Ingesting raw source files from %s...", RAW_DATA_DIR)
    
    if not RAW_DATA_DIR.exists():
        raise FileNotFoundError(f"Raw data directory does not exist: {RAW_DATA_DIR}")

    # Verify official raw PDF documents are present untouched
    raw_files = [RAW_COURSES_PDF, RAW_UG_MANUAL_PDF, RAW_HANDBOOK_PDF, RAW_SEED_CATALOGUE]
    for rf in raw_files:
        if not rf.exists():
            logger.warning("Raw file %s is missing from data/raw/!", rf.name)
        else:
            logger.info("Verified untouched raw artifact: %s (%d bytes)", rf.name, rf.stat().st_size)

    if not RAW_SEED_CATALOGUE.exists():
        raise FileNotFoundError(f"Raw seed catalog missing: {RAW_SEED_CATALOGUE}")

    with open(RAW_SEED_CATALOGUE, "r", encoding="utf-8") as f:
        raw_payload = json.load(f)

    logger.info(
        "Ingested %d courses, %d prereq edges, %d rules, %d resources, %d skills from raw seeds.",
        len(raw_payload.get("courses", [])),
        len(raw_payload.get("prerequisite_edges", [])),
        len(raw_payload.get("academic_rules", [])),
        len(raw_payload.get("resources", [])),
        len(raw_payload.get("skills", [])),
    )
    return raw_payload

