"""Exporter Stage: Serializes validated entities to clean CSV/JSON in data/processed/ and chunks.jsonl."""

import json
import csv
import logging
from pathlib import Path
from typing import Dict, Any, List
from pydantic import BaseModel

from src.config import (
    PROCESSED_DATA_DIR,
    CHUNKS_JSONL_PATH,
    PROCESSED_CHUNKS_PATH,
    DATA_SUMMARY_PATH,
)
from src.schema import Chunk

logger = logging.getLogger("pipeline.exporter")

def model_list_to_dicts(models: List[BaseModel]) -> List[Dict[str, Any]]:
    return [m.model_dump() for m in models]

def export_csv(data: List[Dict[str, Any]], filepath: Path) -> None:
    if not data:
        return
    fieldnames = list(data[0].keys())
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def export_json(data: List[Dict[str, Any]], filepath: Path) -> None:
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def export_pipeline_data(entities: Dict[str, List[Any]], chunks: List[Chunk], validation_report: Dict[str, Any]) -> Dict[str, Any]:
    """
    Serializes all data entities to CSV and JSON files in data/processed/, writes chunks.jsonl,
    and produces an audited data summary report.
    """
    logger.info("Stage 5: Exporting processed seed artifacts and chunks.jsonl...")
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    summary_counts: Dict[str, int] = {}
    field_completeness: Dict[str, float] = {}

    for entity_name, model_list in entities.items():
        dict_records = model_list_to_dicts(model_list)
        summary_counts[entity_name] = len(dict_records)

        # Calculate field completeness percentage
        if dict_records:
            total_slots = 0
            filled_slots = 0
            for r in dict_records:
                for k, v in r.items():
                    total_slots += 1
                    if v is not None and v != "":
                        filled_slots += 1
            completeness = round((filled_slots / total_slots) * 100, 2)
            field_completeness[entity_name] = completeness

        # Export CSV
        csv_file = PROCESSED_DATA_DIR / f"{entity_name}.csv"
        export_csv(dict_records, csv_file)

        # Export JSON
        json_file = PROCESSED_DATA_DIR / f"{entity_name}.json"
        export_json(dict_records, json_file)

    # Export chunks.jsonl to both root and data/processed/
    chunk_dicts = [c.model_dump() for c in chunks]
    summary_counts["chunks"] = len(chunk_dicts)

    for target_path in [CHUNKS_JSONL_PATH, PROCESSED_CHUNKS_PATH]:
        with open(target_path, "w", encoding="utf-8") as f:
            for c in chunk_dicts:
                f.write(json.dumps(c, ensure_ascii=False) + "\n")

    logger.info("Wrote %d chunks to %s", len(chunk_dicts), CHUNKS_JSONL_PATH.name)

    # Generate Summary Metrics Payload
    summary_payload = {
        "pipeline_status": "SUCCESS",
        "entity_counts": summary_counts,
        "field_completeness_percentage": field_completeness,
        "validation_report": validation_report,
        "exported_files": [
            f"data/processed/{k}.csv" for k in entities.keys()
        ] + [
            f"data/processed/{k}.json" for k in entities.keys()
        ] + ["chunks.jsonl", "data/processed/chunks.jsonl"],
    }

    with open(DATA_SUMMARY_PATH, "w", encoding="utf-8") as f:
        json.dump(summary_payload, f, indent=2)

    logger.info("Export complete. Processed artifacts are ready for Day-2 embedding.")
    return summary_payload
