from __future__ import annotations

from collections import Counter
from typing import Any


def _normalize(text: str) -> str:
    return " ".join(text.lower().split())


def recall_at_k(retrieved_ids: list[str], oracle_ids: list[str]) -> float | None:
    if not oracle_ids:
        return None
    overlap = len(set(retrieved_ids[: len(retrieved_ids)]) & set(oracle_ids))
    return round(overlap / len(set(oracle_ids)), 4)


def precision_at_k(retrieved_ids: list[str], oracle_ids: list[str]) -> float | None:
    if not retrieved_ids or not oracle_ids:
        return None
    overlap = len(set(retrieved_ids) & set(oracle_ids))
    return round(overlap / len(retrieved_ids), 4)


def constraint_coverage(text: str, constraints: list[str]) -> float | None:
    if not constraints:
        return None
    normalized_text = _normalize(text)
    matched = sum(1 for item in constraints if _normalize(item) in normalized_text)
    return round(matched / len(constraints), 4)


def count_issues_by_code(issues: list[dict[str, Any]]) -> dict[str, int]:
    counter = Counter(issue.get("code", "unknown") for issue in issues)
    return dict(sorted(counter.items()))


def total_tokens(call_logs: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "input_tokens": sum(int(item.get("input_tokens", 0) or 0) for item in call_logs),
        "output_tokens": sum(int(item.get("output_tokens", 0) or 0) for item in call_logs),
    }
