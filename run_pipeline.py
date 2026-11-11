#!/usr/bin/env python3
"""
IIT Bhilai B.Tech CSE Source-Traced Knowledge Base & Data Pipeline.

Executes all 5 stages of data extraction, normalization, validation, chunking, and export:
  1. Ingest: Reads untouched source files in data/raw/
  2. Parse & Normalise: Normalizes codes, credits, and creates typed domain entities
  3. Validate: Enforces schema invariants, referential integrity, and DAG acyclicity
  4. Chunk: Builds retrieval-sized semantic chunks with filter metadata
  5. Export: Produces CSV/JSON seed files in data/processed/ and chunks.jsonl
"""

import sys
import argparse
import logging
from typing import Dict, Any

from src.ingest import ingest_raw_data
from src.parser import parse_and_normalise
from src.validator import validate_pipeline_data, PipelineValidationError
from src.chunker import build_retrieval_chunks
from src.exporter import export_pipeline_data

def setup_logging(verbose: bool = False):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt="%H:%M:%S",
    )

def run_pipeline(sample_mode: bool = False, validate_only: bool = False) -> Dict[str, Any]:
    """Runs the complete data processing pipeline."""
    print("=" * 70)
    print(" IIT BHILAI B.TECH CSE KNOWLEDGE BASE & DATA PIPELINE ")
    print(" Source-Traced Ingestion, Validation & Retrieval Chunking Pipeline ")
    print("=" * 70)

    # Stage 1: Ingest
    print("\n>>> STAGE 1: INGEST")
    raw_payload = ingest_raw_data()

    if sample_mode:
        print("[SAMPLE MODE] Truncating payload to small sample...")
        raw_payload["courses"] = raw_payload["courses"][:5]
        # Keep only prereqs where both courses exist in sample
        sample_codes = {c["code"] for c in raw_payload["courses"]}
        raw_payload["prerequisite_edges"] = [
            p for p in raw_payload["prerequisite_edges"]
            if p["course"] in sample_codes and p["requires"] in sample_codes
        ]
        raw_payload["resources"] = raw_payload["resources"][:5]

    # Stage 2: Parse and Normalise
    print("\n>>> STAGE 2: PARSE & NORMALISE")
    entities = parse_and_normalise(raw_payload)

    # Stage 3: Validate
    print("\n>>> STAGE 3: VALIDATE")
    validation_report = validate_pipeline_data(entities)

    if validate_only:
        print("\n[VALIDATE ONLY] Data validation completed successfully.")
        return {"validation_report": validation_report.to_dict()}

    # Stage 4: Chunk
    print("\n>>> STAGE 4: CHUNK")
    chunks = build_retrieval_chunks(entities)

    # Stage 5: Export
    print("\n>>> STAGE 5: EXPORT")
    summary = export_pipeline_data(entities, chunks, validation_report.to_dict())

    print("\n" + "=" * 70)
    print(" PIPELINE EXECUTION SUCCESSFUL ")
    print("=" * 70)
    print(f"  • Courses Collected:             {summary['entity_counts'].get('courses', 0)}")
    print(f"  • Prerequisite Edges:           {summary['entity_counts'].get('prerequisite_edges', 0)}")
    print(f"  • Academic Rules:               {summary['entity_counts'].get('academic_rules', 0)}")
    print(f"  • Open Learning Resources:      {summary['entity_counts'].get('resources', 0)}")
    print(f"  • Skills Mapped:                {summary['entity_counts'].get('skills', 0)}")
    print(f"  • Course-Skill Links:           {summary['entity_counts'].get('course_skill_links', 0)}")
    print(f"  • Curriculum Modules:           {summary['entity_counts'].get('modules_lessons', 0)}")
    print(f"  • Practice Exercises:           {summary['entity_counts'].get('exercises', 0)}")
    print(f"  • Total Retrieval Chunks:       {summary['entity_counts'].get('chunks', 0)}")
    print("-" * 70)
    print("  Field Completeness:")
    for entity, pct in summary["field_completeness_percentage"].items():
        print(f"    - {entity:25s}: {pct}%")
    print("=" * 70)
    print("Final artifacts generated in 'data/processed/' and 'chunks.jsonl'.")
    print("Ready for Day-2 Vector & Graph Embedding ingestion.")
    return summary

def main():
    parser = argparse.ArgumentParser(
        description="Run the IIT Bhilai B.Tech CSE Data Pipeline from raw inputs to processed seed data & chunks.jsonl"
    )
    parser.add_argument(
        "--sample",
        action="store_true",
        help="Run pipeline on a small sample subset instead of the full dataset",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Perform schema and referential integrity validation without exporting files",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable detailed debug logging output",
    )
    args = parser.parse_args()
    setup_logging(args.verbose)

    try:
        run_pipeline(sample_mode=args.sample, validate_only=args.validate_only)
        sys.exit(0)
    except PipelineValidationError as e:
        print(f"\n[FATAL VALIDATION ERROR]\n{e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n[PIPELINE CRASHED]: {e}", file=sys.stderr)
        logging.exception("Fatal unhandled pipeline error")
        sys.exit(2)

if __name__ == "__main__":
    main()
