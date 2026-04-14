from __future__ import annotations

import json
import re
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from src.config import (
    GENERATION_MODEL,
    LIGHT_MODEL,
    OPENAI_BASE_URL,
    PROMPT_BUILD_MODEL,
)
from src.compression import execution_spec_search_text, render_execution_spec
from src.domain_profiles import get_domain_profile
from src.evaluation.metrics import (
    constraint_coverage,
    count_issues_by_code,
    precision_at_k,
    recall_at_k,
    total_tokens,
)
from src.graph.pipeline import build_graph

ROOT_DIR = Path(__file__).resolve().parents[2]
RUNS_DIR = ROOT_DIR / "experiments" / "runs"
DEFAULT_BASELINE_REF = "web_design_profile_v1_compact_pass"


def slugify(text: str, limit: int = 48) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    return (slug or "run")[:limit]


def utc_timestamp() -> str:
    return datetime.utcnow().strftime("%Y%m%d_%H%M%S")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def git_capture(args: list[str]) -> str | None:
    try:
        result = subprocess.run(
            args,
            cwd=ROOT_DIR,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except Exception:
        return None


def get_git_metadata() -> dict[str, Any]:
    sha = git_capture(["git", "rev-parse", "HEAD"])
    branch = git_capture(["git", "branch", "--show-current"])
    dirty = git_capture(["git", "status", "--porcelain"])
    return {
        "commit_sha": sha,
        "branch": branch,
        "is_dirty": bool(dirty),
        "dirty_files": dirty.splitlines() if dirty else [],
    }


def build_initial_state(query: str, profile: str) -> dict[str, Any]:
    return {
        "user_query": query,
        "domain": profile,
        "intent": None,
        "retrieved_chunks": None,
        "retrieved_chunk_details": None,
        "context": None,
        "expanded_queries": None,
        "built_prompt": None,
        "execution_spec": None,
        "generation_result": None,
        "quality_check": None,
        "retry_count": 0,
        "call_logs": [],
        "intent_metadata": None,
        "retrieval_metadata": None,
        "compression_metadata": None,
        "spec_parse_metadata": None,
        "generation_metadata": None,
    }


def run_agent_once(query: str, profile: str) -> tuple[dict[str, Any], float]:
    app = build_graph()
    start = time.perf_counter()
    result = app.invoke(build_initial_state(query, profile))
    duration_sec = round(time.perf_counter() - start, 3)
    return result, duration_sec


def build_run_id(profile: str, query: str, dataset_item_id: str | None = None) -> str:
    suffix = dataset_item_id or slugify(query)
    return f"{utc_timestamp()}_{profile}_{suffix}"


def persist_run(
    *,
    query: str,
    profile_name: str,
    result: dict[str, Any],
    duration_sec: float,
    run_id: str,
    output_root: Path | None = None,
    baseline_ref: str = DEFAULT_BASELINE_REF,
    dataset_item_id: str | None = None,
    ablation_flags: list[str] | None = None,
) -> Path:
    output_dir = (output_root or RUNS_DIR) / run_id
    output_dir.mkdir(parents=True, exist_ok=True)

    profile = get_domain_profile(profile_name)
    call_logs = list(result.get("call_logs") or [])
    token_totals = total_tokens(call_logs)
    quality = result.get("quality_check") or {"pass": False, "issues": [], "checks": {}}
    retrieved_details = list(result.get("retrieved_chunk_details") or [])

    manifest = {
        "run_id": run_id,
        "timestamp": run_id.split("_", 2)[0] + "_" + run_id.split("_", 2)[1],
        "profile": profile_name,
        "system_version": get_git_metadata(),
        "baseline_ref": baseline_ref,
        "models": {
            "light_model": LIGHT_MODEL,
            "prompt_build_model": PROMPT_BUILD_MODEL,
            "generation_model": GENERATION_MODEL,
        },
        "provider": {
            "openai_base_url": OPENAI_BASE_URL,
        },
        "query": query,
        "ablation_flags": ablation_flags or [],
        "dataset_item_id": dataset_item_id,
        "duration_sec": duration_sec,
    }

    query_payload = {
        "query": query,
        "profile": profile_name,
        "intent": result.get("intent"),
        "intent_metadata": result.get("intent_metadata"),
        "dataset_item_id": dataset_item_id,
    }

    retrieval_payload = {
        "expanded_queries": result.get("expanded_queries") or [],
        "retrieved_chunks": result.get("retrieved_chunks") or [],
        "retrieved_chunk_details": retrieved_details,
        "retrieval_metadata": result.get("retrieval_metadata"),
        "context_chars": len(result.get("context") or ""),
    }

    compression_payload = {
        "compression_metadata": result.get("compression_metadata"),
        "spec_parse_metadata": result.get("spec_parse_metadata"),
        "execution_spec": result.get("execution_spec") or {},
        "execution_spec_text": result.get("built_prompt") or "",
        "source_refs": [item["id"] for item in retrieved_details],
        "constraint_coverage": None,
    }

    generation_payload = {
        "generation_metadata": result.get("generation_metadata"),
        "artifact_chars": len(result.get("generation_result") or ""),
    }

    validator_payload = {
        "pass": quality.get("pass"),
        "issues": quality.get("issues") or [],
        "checks": quality.get("checks") or {},
        "retry_count": result.get("retry_count", 0),
        "issue_count_by_code": count_issues_by_code(quality.get("issues") or []),
    }

    summary_payload = {
        "run_id": run_id,
        "profile": profile_name,
        "dataset_item_id": dataset_item_id,
        "pass": quality.get("pass"),
        "retry_count": result.get("retry_count", 0),
        "retrieved_chunk_count": len(retrieved_details),
        "compression_retention_ratio": (result.get("compression_metadata") or {}).get("retention_ratio"),
        "total_input_tokens": token_totals["input_tokens"],
        "total_output_tokens": token_totals["output_tokens"],
        "duration_sec": duration_sec,
        "issue_count_by_code": validator_payload["issue_count_by_code"],
    }

    write_json(output_dir / "run_manifest.json", manifest)
    write_json(output_dir / "query.json", query_payload)
    write_json(output_dir / "retrieval.json", retrieval_payload)
    write_json(output_dir / "compression.json", compression_payload)
    write_json(output_dir / "generation.json", generation_payload)
    write_json(output_dir / "validator.json", validator_payload)
    write_json(output_dir / "summary.json", summary_payload)
    write_json(output_dir / "call_logs.json", {"call_logs": call_logs})

    (output_dir / "context.txt").write_text(result.get("context") or "", encoding="utf-8")
    (output_dir / "execution_spec.txt").write_text(
        result.get("built_prompt") or render_execution_spec(result.get("execution_spec") or {}),
        encoding="utf-8",
    )
    write_json(output_dir / "execution_spec.json", result.get("execution_spec") or {})
    artifact_ext = "html" if profile.output_format == "html" else "txt"
    (output_dir / f"artifact.{artifact_ext}").write_text(
        result.get("generation_result") or "",
        encoding="utf-8",
    )

    return output_dir


def evaluate_result_against_benchmark(
    *,
    benchmark_item: dict[str, Any],
    result: dict[str, Any],
) -> dict[str, Any]:
    retrieved_ids = [item["id"] for item in result.get("retrieved_chunk_details") or []]
    oracle_chunk_ids = list(benchmark_item.get("oracle_chunk_ids") or [])
    oracle_constraints = list(benchmark_item.get("oracle_constraints") or [])
    built_prompt = result.get("built_prompt") or ""
    execution_spec_text = execution_spec_search_text(result.get("execution_spec") or {})

    return {
        "task_id": benchmark_item.get("task_id"),
        "retrieval_recall": recall_at_k(retrieved_ids, oracle_chunk_ids),
        "retrieval_precision": precision_at_k(retrieved_ids, oracle_chunk_ids),
        "hard_constraint_coverage": constraint_coverage(execution_spec_text or built_prompt, oracle_constraints),
        "validator_pass": (result.get("quality_check") or {}).get("pass"),
        "retry_count": result.get("retry_count", 0),
    }
