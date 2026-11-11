"""Unit and Integration Tests for the IIT Bhilai Knowledge Base Pipeline."""

import pytest
import copy
from src.ingest import ingest_raw_data
from src.parser import parse_and_normalise
from src.validator import validate_pipeline_data, PipelineValidationError
from src.chunker import build_retrieval_chunks

@pytest.fixture
def valid_payload():
    return ingest_raw_data()

def test_full_pipeline_validation(valid_payload):
    """Verifies that the authentic dataset passes all validation constraints."""
    entities = parse_and_normalise(valid_payload)
    report = validate_pipeline_data(entities)
    assert report.checks_run >= 10
    assert len(report.errors) == 0
    assert report.to_dict()["status"] == "PASS"

def test_prerequisite_missing_course_fails_loudly(valid_payload):
    """Validator must fail loudly if a prerequisite references a non-existent course."""
    corrupted = copy.deepcopy(valid_payload)
    corrupted["prerequisite_edges"].append({
        "course": "CSL202",
        "requires": "CSL999_GHOST_COURSE",
        "kind": "hard",
        "source_url": "https://iitbhilai.ac.in",
        "retrieved_on": "2026-11-11",
        "source_type": "official"
    })
    entities = parse_and_normalise(corrupted)
    with pytest.raises(PipelineValidationError) as exc_info:
        validate_pipeline_data(entities)
    assert "CSL999_GHOST_COURSE" in str(exc_info.value)

def test_prerequisite_cycle_detection_fails_loudly(valid_payload):
    """Validator must detect cycles in prerequisite graph and fail loudly."""
    corrupted = copy.deepcopy(valid_payload)
    # CSL202 requires CSL100. Let's make CSL100 require CSL202, creating an immediate cycle!
    corrupted["prerequisite_edges"].append({
        "course": "CSL100",
        "requires": "CSL202",
        "kind": "hard",
        "source_url": "https://iitbhilai.ac.in",
        "retrieved_on": "2026-11-11",
        "source_type": "official"
    })
    entities = parse_and_normalise(corrupted)
    with pytest.raises(PipelineValidationError) as exc_info:
        validate_pipeline_data(entities)
    assert "cycle" in str(exc_info.value).lower()

def test_duplicate_course_code_fails_loudly(valid_payload):
    """Validator must detect duplicate course codes."""
    corrupted = copy.deepcopy(valid_payload)
    dup_course = copy.deepcopy(corrupted["courses"][0])
    corrupted["courses"].append(dup_course)
    entities = parse_and_normalise(corrupted)
    with pytest.raises(PipelineValidationError) as exc_info:
        validate_pipeline_data(entities)
    assert "Duplicate Course Codes" in str(exc_info.value)

def test_missing_source_url_fails_loudly(valid_payload):
    """Validator must fail loudly if a record has an empty or invalid source URL."""
    corrupted = copy.deepcopy(valid_payload)
    corrupted["courses"][0]["source_url"] = ""
    entities = parse_and_normalise(corrupted)
    with pytest.raises(PipelineValidationError) as exc_info:
        validate_pipeline_data(entities)
    assert "Source URLs" in str(exc_info.value)

def test_chunking_preserves_metadata(valid_payload):
    """Ensures chunking produces proper retrieval chunks with parent IDs and filter metadata."""
    entities = parse_and_normalise(valid_payload)
    chunks = build_retrieval_chunks(entities)
    assert len(chunks) > 50

    course_chunks = [c for c in chunks if c.parent_type == "course"]
    assert len(course_chunks) >= len(entities["courses"])
    for c in course_chunks:
        assert c.source_url.startswith("http")
        assert "dept" in c.filter_metadata
        assert "credits" in c.filter_metadata

    rule_chunks = [c for c in chunks if c.parent_type == "academic_rule"]
    assert len(rule_chunks) == len(entities["academic_rules"])
    for r in rule_chunks:
        assert "category" in r.filter_metadata

