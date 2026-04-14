from __future__ import annotations

import json
from typing import Any

EXECUTION_SPEC_SCHEMA_TEXT = """Return exactly one JSON object with this schema:
{
  "task_summary": "string",
  "deliverable": {
    "type": "string",
    "format": "string"
  },
  "hard_constraints": [
    {
      "id": "HC-01",
      "requirement": "string",
      "source_refs": ["string"]
    }
  ],
  "optional_guidance": [
    {
      "id": "OG-01",
      "guidance": "string",
      "source_refs": ["string"]
    }
  ],
  "interaction_requirements": [
    {
      "id": "IR-01",
      "interaction": "string",
      "states": ["string"],
      "source_refs": ["string"]
    }
  ],
  "forbidden_items": [
    {
      "id": "FI-01",
      "item": "string",
      "source_refs": ["string"]
    }
  ],
  "repair_requirements": [
    {
      "id": "RR-01",
      "requirement": "string",
      "source_refs": ["string"]
    }
  ],
  "acceptance_checks": [
    {
      "id": "AC-01",
      "check": "string",
      "source_refs": ["string"]
    }
  ],
  "unresolved_items": [
    {
      "id": "UN-01",
      "item": "string",
      "reason": "string",
      "source_refs": ["string"]
    }
  ]
}

Rules:
- Return JSON only. No markdown fences.
- Every list item must be concise and atomic.
- Keep the spec selective and query-aware; do not dump every possible rule from the corpus.
- Prefer the smallest set of requirements that still preserves correctness.
- Use these budgets unless the task clearly requires fewer:
  - hard_constraints: 12-20 items
  - optional_guidance: 0-6 items
  - interaction_requirements: 0-10 items
  - forbidden_items: 0-10 items
  - repair_requirements: 0-8 items
  - acceptance_checks: 6-12 items
  - unresolved_items: 0-5 items
- Do not restate the same requirement across multiple sections unless it is truly acting as a repair item.
- `source_refs` must cite only the allowed source refs when evidence exists.
- If evidence is weak or missing, prefer `unresolved_items` instead of inventing a hard constraint.
"""


def _json_default(output_format: str, task_summary: str) -> dict[str, Any]:
    deliverable_type = "html_document" if output_format == "html" else "text_deliverable"
    return {
        "task_summary": task_summary.strip(),
        "deliverable": {
            "type": deliverable_type,
            "format": output_format,
        },
        "hard_constraints": [],
        "optional_guidance": [],
        "interaction_requirements": [],
        "forbidden_items": [],
        "repair_requirements": [],
        "acceptance_checks": [],
        "unresolved_items": [],
    }


def _extract_json_blob(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        stripped = "\n".join(lines).strip()

    start = stripped.find("{")
    end = stripped.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("No JSON object found in model output.")
    return stripped[start : end + 1]


def _stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def _normalize_refs(value: Any, allowed_source_refs: set[str]) -> list[str]:
    if isinstance(value, list):
        refs = [_stringify(item) for item in value]
    elif value:
        refs = [_stringify(value)]
    else:
        refs = []

    normalized: list[str] = []
    seen = set()
    for ref in refs:
        if not ref:
            continue
        if allowed_source_refs and ref not in allowed_source_refs:
            continue
        if ref not in seen:
            normalized.append(ref)
            seen.add(ref)
    return normalized


def _normalize_string_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [_stringify(item) for item in value if _stringify(item)]
    if value:
        text = _stringify(value)
        return [text] if text else []
    return []


def _normalize_item(
    value: Any,
    *,
    index: int,
    prefix: str,
    text_key: str,
    allowed_source_refs: set[str],
    extra_keys: tuple[str, ...] = (),
) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        text = _stringify(value)
        if not text:
            return None
        value = {text_key: text}

    text = _stringify(value.get(text_key))
    if not text:
        return None

    item = {
        "id": _stringify(value.get("id")) or f"{prefix}-{index:02d}",
        text_key: text,
        "source_refs": _normalize_refs(value.get("source_refs"), allowed_source_refs),
    }

    for key in extra_keys:
        if key == "states":
            item[key] = _normalize_string_list(value.get(key))
        else:
            item[key] = _stringify(value.get(key))
    return item


def _normalize_items(
    raw_items: Any,
    *,
    prefix: str,
    text_key: str,
    allowed_source_refs: set[str],
    extra_keys: tuple[str, ...] = (),
) -> list[dict[str, Any]]:
    items = raw_items if isinstance(raw_items, list) else []
    normalized: list[dict[str, Any]] = []
    for idx, item in enumerate(items, start=1):
        normalized_item = _normalize_item(
            item,
            index=idx,
            prefix=prefix,
            text_key=text_key,
            allowed_source_refs=allowed_source_refs,
            extra_keys=extra_keys,
        )
        if normalized_item:
            normalized.append(normalized_item)
    return normalized


def _dedupe_items(items: list[dict[str, Any]], text_key: str) -> list[dict[str, Any]]:
    deduped: list[dict[str, Any]] = []
    seen = set()
    for item in items:
        text = _stringify(item.get(text_key)).lower()
        if not text or text in seen:
            continue
        deduped.append(item)
        seen.add(text)
    return deduped


def parse_execution_spec(
    raw_text: str,
    *,
    output_format: str,
    task_summary: str,
    allowed_source_refs: list[str] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    allowed = set(allowed_source_refs or [])
    base = _json_default(output_format, task_summary)
    metadata = {
        "parse_ok": False,
        "fallback_used": False,
        "parse_error": None,
    }

    try:
        payload = json.loads(_extract_json_blob(raw_text))
        if not isinstance(payload, dict):
            raise ValueError("Execution spec root must be an object.")
        metadata["parse_ok"] = True
    except Exception as exc:
        payload = {}
        metadata["fallback_used"] = True
        metadata["parse_error"] = str(exc)

    spec = {
        "task_summary": _stringify(payload.get("task_summary")) or base["task_summary"],
        "deliverable": {
            "type": _stringify((payload.get("deliverable") or {}).get("type")) or base["deliverable"]["type"],
            "format": _stringify((payload.get("deliverable") or {}).get("format")) or output_format,
        },
        "hard_constraints": _normalize_items(
            payload.get("hard_constraints"),
            prefix="HC",
            text_key="requirement",
            allowed_source_refs=allowed,
        ),
        "optional_guidance": _normalize_items(
            payload.get("optional_guidance"),
            prefix="OG",
            text_key="guidance",
            allowed_source_refs=allowed,
        ),
        "interaction_requirements": _normalize_items(
            payload.get("interaction_requirements"),
            prefix="IR",
            text_key="interaction",
            allowed_source_refs=allowed,
            extra_keys=("states",),
        ),
        "forbidden_items": _normalize_items(
            payload.get("forbidden_items"),
            prefix="FI",
            text_key="item",
            allowed_source_refs=allowed,
        ),
        "repair_requirements": _normalize_items(
            payload.get("repair_requirements"),
            prefix="RR",
            text_key="requirement",
            allowed_source_refs=allowed,
        ),
        "acceptance_checks": _normalize_items(
            payload.get("acceptance_checks"),
            prefix="AC",
            text_key="check",
            allowed_source_refs=allowed,
        ),
        "unresolved_items": _normalize_items(
            payload.get("unresolved_items"),
            prefix="UN",
            text_key="item",
            allowed_source_refs=allowed,
            extra_keys=("reason",),
        ),
    }

    spec["hard_constraints"] = _dedupe_items(spec["hard_constraints"], "requirement")
    spec["optional_guidance"] = _dedupe_items(spec["optional_guidance"], "guidance")
    spec["interaction_requirements"] = _dedupe_items(spec["interaction_requirements"], "interaction")
    spec["forbidden_items"] = _dedupe_items(spec["forbidden_items"], "item")
    spec["repair_requirements"] = _dedupe_items(spec["repair_requirements"], "requirement")
    spec["acceptance_checks"] = _dedupe_items(spec["acceptance_checks"], "check")
    spec["unresolved_items"] = _dedupe_items(spec["unresolved_items"], "item")

    if metadata["fallback_used"] and raw_text.strip():
        spec["hard_constraints"].append(
            {
                "id": "HC-RAW",
                "requirement": raw_text.strip(),
                "source_refs": [],
            }
        )

    source_refs = collect_source_refs(spec)
    spec["source_coverage"] = {
        "allowed_source_refs": sorted(allowed),
        "used_source_refs": source_refs,
        "unused_source_refs": [ref for ref in sorted(allowed) if ref not in source_refs],
    }
    return spec, metadata


def collect_source_refs(spec: dict[str, Any]) -> list[str]:
    refs: list[str] = []
    seen = set()
    for key in (
        "hard_constraints",
        "optional_guidance",
        "interaction_requirements",
        "forbidden_items",
        "repair_requirements",
        "acceptance_checks",
        "unresolved_items",
    ):
        for item in spec.get(key, []) or []:
            for ref in item.get("source_refs", []) or []:
                if ref not in seen:
                    refs.append(ref)
                    seen.add(ref)
    return refs


def render_execution_spec(spec: dict[str, Any]) -> str:
    return json.dumps(spec, ensure_ascii=False, indent=2)


def render_execution_spec_brief(spec: dict[str, Any]) -> str:
    def render_list(title: str, items: list[dict[str, Any]], key: str, *, include_states: bool = False) -> str:
        if not items:
            return ""
        lines = [f"## {title}"]
        for item in items:
            text = _stringify(item.get(key))
            if not text:
                continue
            line = f"- {item.get('id', '')}: {text}".strip()
            refs = item.get("source_refs") or []
            if refs:
                line += f" [refs: {', '.join(refs)}]"
            lines.append(line)
            if include_states and item.get("states"):
                lines.append(f"  states: {', '.join(item['states'])}")
        return "\n".join(lines)

    blocks = [
        "# EXECUTION SPEC",
        f"## TASK SUMMARY\n{_stringify(spec.get('task_summary'))}",
        "## DELIVERABLE\n"
        f"type={_stringify((spec.get('deliverable') or {}).get('type'))}\n"
        f"format={_stringify((spec.get('deliverable') or {}).get('format'))}",
        render_list("HARD CONSTRAINTS", spec.get("hard_constraints") or [], "requirement"),
        render_list("INTERACTION REQUIREMENTS", spec.get("interaction_requirements") or [], "interaction", include_states=True),
        render_list("FORBIDDEN ITEMS", spec.get("forbidden_items") or [], "item"),
        render_list("REPAIR REQUIREMENTS", spec.get("repair_requirements") or [], "requirement"),
        render_list("ACCEPTANCE CHECKS", spec.get("acceptance_checks") or [], "check"),
        render_list("OPTIONAL GUIDANCE", spec.get("optional_guidance") or [], "guidance"),
        render_list("UNRESOLVED ITEMS", spec.get("unresolved_items") or [], "item"),
    ]
    return "\n\n".join(block for block in blocks if block.strip())


def execution_spec_search_text(spec: dict[str, Any]) -> str:
    parts = [_stringify(spec.get("task_summary"))]
    for key, field in (
        ("hard_constraints", "requirement"),
        ("optional_guidance", "guidance"),
        ("interaction_requirements", "interaction"),
        ("forbidden_items", "item"),
        ("repair_requirements", "requirement"),
        ("acceptance_checks", "check"),
        ("unresolved_items", "item"),
    ):
        for item in spec.get(key, []) or []:
            text = _stringify(item.get(field))
            if text:
                parts.append(text)
        if key == "interaction_requirements":
            for item in spec.get(key, []) or []:
                states = item.get("states") or []
                if states:
                    parts.append(" ".join(states))
    return "\n".join(part for part in parts if part)
