import os
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv

from src.compression import (
    EXECUTION_SPEC_SCHEMA_TEXT,
    collect_source_refs,
    parse_execution_spec,
    render_execution_spec_brief,
    render_execution_spec,
)
from src.config import (
    CHROMA_DB_PATH,
    GENERATION_MODEL,
    GENERATION_REASONING_EFFORT,
    INTENT_DEFAULT,
    INTENT_TYPES,
    LIGHT_MODEL,
    LIGHT_REASONING_EFFORT,
    OPENAI_BASE_URL,
    OPENAI_PREFER_CHAT_COMPLETIONS_STREAM,
    OPENAI_TIMEOUT_SECONDS,
    PROMPT_BUILD_MODEL,
    PROMPT_BUILD_REASONING_EFFORT,
    RETRIEVAL_DENSE_TOP_K,
    RETRIEVAL_ENABLE_DENSE,
    RETRIEVAL_ENABLE_LEXICAL,
    RETRIEVAL_ENABLE_PARENT_EXPANSION,
    RETRIEVAL_FINAL_TOP_K,
    RETRIEVAL_HYBRID_DENSE_WEIGHT,
    RETRIEVAL_HYBRID_LEXICAL_WEIGHT,
    RETRIEVAL_LEXICAL_TOP_K,
    RETRIEVAL_PARENT_EXPAND_MAX_EXTRA,
    RETRIEVAL_PARENT_EXPAND_MAX_FAMILIES,
    RETRIEVAL_PRE_RERANK_K,
    RETRIEVAL_RERANK_TOP_K,
)
from src.domain_profiles import DomainProfile, get_domain_profile
from src.evaluation.validators import get_validator
from src.graph.state import AgentState
from src.indexing.chroma_store import ChromaStore
from src.indexing.embedder import Embedder
from src.indexing.reranker import Reranker

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parents[2]

_embedder = None
_retriever_cache: dict[str, tuple[dict[str, ChromaStore], Reranker]] = {}
_doc_cache: dict[str, dict[str, str]] = {}
_validator_cache: dict[str, object] = {}


def resolve_profile(state: AgentState) -> DomainProfile:
    return get_domain_profile(state.get("domain"))


def safe_print(text: str) -> None:
    encoding = sys.stdout.encoding or "utf-8"
    sanitized = text.encode(encoding, errors="replace").decode(encoding, errors="replace")
    print(sanitized)


def get_openai_api_key() -> str:
    token = (
        os.getenv("OPENAI_API_KEY")
        or os.getenv("CODEX_API_KEY")
        or os.getenv("ANTHROPIC_AUTH_TOKEN")
    )
    if not token:
        raise RuntimeError("Missing OPENAI_API_KEY (or CODEX_API_KEY) in environment.")
    return token


def extract_output_text(payload: dict[str, Any]) -> str:
    direct = payload.get("output_text")
    if isinstance(direct, str) and direct.strip():
        return direct.strip()

    chunks: list[str] = []
    for item in payload.get("output", []):
        if item.get("type") == "message":
            for content in item.get("content", []):
                text = content.get("text") or content.get("content") or content.get("value")
                if isinstance(text, str) and content.get("type") in {"output_text", "text"}:
                    chunks.append(text)
        elif item.get("type") in {"output_text", "text"}:
            text = item.get("text") or item.get("content") or item.get("value")
            if isinstance(text, str):
                chunks.append(text)
    return "".join(chunks).strip()


def call_chat_completions_stream(
    prompt: str,
    *,
    system: str = "",
    model: str,
    max_tokens: int,
    reasoning_effort: str | None = None,
) -> tuple[str, int, int]:
    token = get_openai_api_key()
    base = OPENAI_BASE_URL.rstrip("/")
    endpoint = f"{base}/chat/completions"

    messages: list[dict[str, str]] = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    body: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "max_completion_tokens": max_tokens,
        "stream": True,
    }
    if reasoning_effort and reasoning_effort.lower() != "none":
        body["reasoning_effort"] = reasoning_effort

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    for attempt in range(2):
        try:
            with httpx.Client(timeout=OPENAI_TIMEOUT_SECONDS) as client:
                with client.stream("POST", endpoint, headers=headers, json=body) as response:
                    response.raise_for_status()
                    chunks: list[str] = []
                    input_tokens = 0
                    output_tokens = 0

                    for line in response.iter_lines():
                        if not line or not line.startswith("data: "):
                            continue
                        data = line[6:].strip()
                        if data == "[DONE]":
                            break
                        payload = httpx.Response(200, content=data).json()
                        choices = payload.get("choices", [])
                        if choices:
                            delta = choices[0].get("delta", {})
                            content = delta.get("content")
                            if isinstance(content, str):
                                chunks.append(content)
                        usage = payload.get("usage", {})
                        input_tokens = usage.get("prompt_tokens", input_tokens)
                        output_tokens = usage.get("completion_tokens", output_tokens)

                    return "".join(chunks).strip(), input_tokens, output_tokens
        except httpx.RemoteProtocolError as exc:
            if attempt == 0:
                print(f"[call_chat_completions_stream] stream dropped early: {exc}; retrying once in 3s")
                time.sleep(3)
                continue
            raise


def call_openai(
    prompt: str,
    *,
    system: str = "",
    model: str,
    max_tokens: int,
    reasoning_effort: str | None = None,
) -> tuple[str, int, int]:
    if OPENAI_PREFER_CHAT_COMPLETIONS_STREAM:
        return call_chat_completions_stream(
            prompt,
            system=system,
            model=model,
            max_tokens=max_tokens,
            reasoning_effort=reasoning_effort,
        )

    token = get_openai_api_key()
    base = OPENAI_BASE_URL.rstrip("/")
    endpoint = f"{base}/responses"

    body: dict[str, Any] = {
        "model": model,
        "input": prompt,
        "max_output_tokens": max_tokens,
    }
    if system:
        body["instructions"] = system
    if reasoning_effort and reasoning_effort.lower() != "none":
        body["reasoning"] = {"effort": reasoning_effort}

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    for attempt in range(2):
        try:
            with httpx.Client(timeout=OPENAI_TIMEOUT_SECONDS) as client:
                response = client.post(
                    endpoint,
                    headers=headers,
                    json=body,
                )
                response.raise_for_status()
                payload = response.json()
                usage = payload.get("usage", {})
                input_tokens = usage.get("input_tokens", usage.get("prompt_tokens", 0))
                output_tokens = usage.get("output_tokens", usage.get("completion_tokens", 0))
                text = extract_output_text(payload)
                if text:
                    return text, input_tokens, output_tokens
                print("[call_openai] empty text from /responses, falling back to streaming /chat/completions")
                return call_chat_completions_stream(
                    prompt,
                    system=system,
                    model=model,
                    max_tokens=max_tokens,
                    reasoning_effort=reasoning_effort,
                )
        except Exception as exc:
            if attempt == 0:
                print(f"[call_openai] first attempt failed: {exc}; retrying via streaming fallback in 3s")
                time.sleep(3)
                try:
                    return call_chat_completions_stream(
                        prompt,
                        system=system,
                        model=model,
                        max_tokens=max_tokens,
                        reasoning_effort=reasoning_effort,
                    )
                except Exception as fallback_exc:
                    print(f"[call_openai] streaming fallback also failed: {fallback_exc}")
            else:
                raise


def call_light_model(prompt: str, system: str | None = None) -> tuple[str, int, int]:
    return call_openai(
        prompt,
        system=system or "",
        model=LIGHT_MODEL,
        max_tokens=2000,
        reasoning_effort=LIGHT_REASONING_EFFORT,
    )


def get_retriever(profile: DomainProfile):
    global _embedder
    if _embedder is None:
        _embedder = Embedder()

    cached = _retriever_cache.get(profile.name)
    if cached is None:
        stores = {name: ChromaStore(CHROMA_DB_PATH, name) for name in profile.collections}
        reranker = Reranker()
        cached = (stores, reranker)
        _retriever_cache[profile.name] = cached

    return _embedder, cached[0], cached[1]


def load_context_documents(profile: DomainProfile) -> dict[str, str]:
    cached = _doc_cache.get(profile.name)
    if cached is None:
        cached = {}
        for doc in profile.context_documents:
            cached[doc.key] = (ROOT_DIR / doc.path).read_text(encoding="utf-8")
        _doc_cache[profile.name] = cached
    return cached


def get_profile_validator(profile: DomainProfile):
    validator = _validator_cache.get(profile.name)
    if validator is None:
        validator = get_validator(profile.validator_name)
        _validator_cache[profile.name] = validator
    return validator


def clean_model_output(result: str, output_format: str) -> str:
    text = result.strip()
    if text.startswith("```"):
        first_line, _, remainder = text.partition("\n")
        if first_line.startswith("```"):
            text = remainder or text
    if "```" in text:
        text = text[: text.rfind("```")]

    if output_format == "html" and "</html>" in text.lower():
        lower = text.lower()
        end_idx = lower.rfind("</html>") + len("</html>")
        text = text[:end_idx]

    return text.strip()


def append_call_log(state: AgentState, entry: dict[str, Any]) -> list[dict[str, Any]]:
    logs = list(state.get("call_logs") or [])
    logs.append(entry)
    return logs


def make_call_log(
    *,
    stage: str,
    model: str,
    reasoning_effort: str,
    max_tokens: int,
    prompt: str,
    system: str,
    output: str,
    input_tokens: int,
    output_tokens: int,
) -> dict[str, Any]:
    return {
        "stage": stage,
        "model": model,
        "reasoning_effort": reasoning_effort,
        "max_tokens": max_tokens,
        "prompt_chars": len(prompt),
        "system_chars": len(system),
        "output_chars": len(output),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
    }


def format_issue_block(state: AgentState) -> str:
    issues = (state.get("quality_check") or {}).get("issues") or []
    if not issues:
        return "No previous validation issues."

    lines = ["Previous validation issues that must be fixed:"]
    for issue in issues[:12]:
        lines.append(f"- [{issue['severity']}] {issue['message']}")
    return "\n".join(lines)


def format_retrieved_block(items: list[dict], label: str) -> str:
    if not items:
        return f"## {label}\n(none)"
    body = "\n\n---\n\n".join(
        f"[{item['collection']}] {item['title']}\nsource_ref={item['id']}\n{item['content']}" for item in items
    )
    return f"## {label}\n{body}"


def classify_intent(state: AgentState) -> dict:
    prompt = f"""Classify the user request into exactly one intent label.

Allowed labels:
- technique_selection: the user wants recommendations, techniques, or reference patterns
- main_generation: the user wants a full deliverable generated
- quality_check: the user wants an existing deliverable reviewed or validated

User request:
{state['user_query']}

Return only one label."""

    raw_intent, in_tok, out_tok = call_light_model(prompt)
    intent = raw_intent if raw_intent in set(INTENT_TYPES) else INTENT_DEFAULT
    log_entry = make_call_log(
        stage="classify_intent",
        model=LIGHT_MODEL,
        reasoning_effort=LIGHT_REASONING_EFFORT,
        max_tokens=2000,
        prompt=prompt,
        system="",
        output=raw_intent,
        input_tokens=in_tok,
        output_tokens=out_tok,
    )

    print(f"[classify_intent] input={in_tok}, output={out_tok}, {state['user_query']} -> {intent}")
    return {
        "intent": intent,
        "intent_metadata": {
            "raw_intent": raw_intent,
            "final_intent": intent,
            "input_tokens": in_tok,
            "output_tokens": out_tok,
        },
        "call_logs": append_call_log(state, log_entry),
    }


def expand_query(query: str, intent: str, profile: DomainProfile) -> tuple[list[str], dict[str, Any]]:
    axes = "\n".join(f"- {axis}" for axis in profile.query_axes)
    prompt = f"""Break the user request into 4 retrieval sub-queries that cover distinct angles.

Coverage axes:
{axes}

User request:
{query}

Intent:
{intent}

Return exactly 4 lines with no numbering and no explanation."""

    result, in_tok, out_tok = call_light_model(prompt)
    print(f"[expand_query] profile={profile.name}, input={in_tok}, output={out_tok}")
    queries = [line.strip() for line in result.splitlines() if line.strip()]
    queries.append(query)
    log_entry = make_call_log(
        stage="expand_query",
        model=LIGHT_MODEL,
        reasoning_effort=LIGHT_REASONING_EFFORT,
        max_tokens=2000,
        prompt=prompt,
        system="",
        output=result,
        input_tokens=in_tok,
        output_tokens=out_tok,
    )
    return queries[:5], log_entry


def _candidate_key(collection: str, chunk_id: str) -> str:
    return f"{collection}:{chunk_id}"


def _merge_candidate(
    candidate_map: dict[str, dict[str, Any]],
    *,
    collection: str,
    item: dict[str, Any],
    query: str,
    dense_score: float | None = None,
    dense_norm: float | None = None,
    lexical_score: float | None = None,
    lexical_norm: float | None = None,
) -> None:
    key = _candidate_key(collection, item["id"])
    existing = candidate_map.get(key)
    if existing is None:
        existing = dict(item)
        existing["collection"] = collection
        existing["dense_score"] = 0.0
        existing["dense_norm"] = 0.0
        existing["lexical_score"] = 0.0
        existing["lexical_norm"] = 0.0
        existing["matched_queries"] = []
        candidate_map[key] = existing

    if query not in existing["matched_queries"]:
        existing["matched_queries"].append(query)

    if dense_score is not None:
        existing["dense_score"] = max(existing.get("dense_score") or 0.0, dense_score)
        existing["dense_norm"] = max(existing.get("dense_norm") or 0.0, dense_norm or dense_score)

    if lexical_score is not None:
        existing["lexical_score"] = max(existing.get("lexical_score") or 0.0, lexical_score)
        existing["lexical_norm"] = max(existing.get("lexical_norm") or 0.0, lexical_norm or lexical_score)


def _compute_hybrid_score(item: dict[str, Any]) -> float:
    dense_norm = float(item.get("dense_norm") or 0.0)
    lexical_norm = float(item.get("lexical_norm") or 0.0)

    if RETRIEVAL_ENABLE_DENSE and RETRIEVAL_ENABLE_LEXICAL:
        score = (RETRIEVAL_HYBRID_DENSE_WEIGHT * dense_norm) + (
            RETRIEVAL_HYBRID_LEXICAL_WEIGHT * lexical_norm
        )
    elif RETRIEVAL_ENABLE_DENSE:
        score = dense_norm
    elif RETRIEVAL_ENABLE_LEXICAL:
        score = lexical_norm
    else:
        score = 0.0

    query_bonus = min(len(item.get("matched_queries") or []), 3) * 0.03
    return round(score + query_bonus, 6)


def _rank_hybrid_candidates(
    *,
    expanded_queries: list[str],
    embedder: Embedder,
    stores: dict[str, ChromaStore],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    candidate_map: dict[str, dict[str, Any]] = {}
    dense_candidate_count = 0
    lexical_candidate_count = 0

    for query in expanded_queries:
        query_vec = embedder.embed([query])[0] if RETRIEVAL_ENABLE_DENSE else None
        for collection, store in stores.items():
            dense_results = (
                store.query(query_vec, top_k=RETRIEVAL_DENSE_TOP_K)
                if RETRIEVAL_ENABLE_DENSE and query_vec is not None
                else []
            )
            lexical_results = (
                store.query_lexical(query, top_k=RETRIEVAL_LEXICAL_TOP_K)
                if RETRIEVAL_ENABLE_LEXICAL
                else []
            )

            dense_scale = max((item.get("score") or 0.0) for item in dense_results) or 1.0
            lexical_scale = max((item.get("lexical_score") or 0.0) for item in lexical_results) or 1.0

            for item in dense_results:
                dense_candidate_count += 1
                _merge_candidate(
                    candidate_map,
                    collection=collection,
                    item=item,
                    query=query,
                    dense_score=item.get("score"),
                    dense_norm=(item.get("score") or 0.0) / dense_scale,
                )

            for item in lexical_results:
                lexical_candidate_count += 1
                _merge_candidate(
                    candidate_map,
                    collection=collection,
                    item=item,
                    query=query,
                    lexical_score=item.get("lexical_score"),
                    lexical_norm=(item.get("lexical_score") or 0.0) / lexical_scale,
                )

    candidates = list(candidate_map.values())
    for item in candidates:
        item["hybrid_score"] = _compute_hybrid_score(item)

    candidates.sort(key=lambda row: row["hybrid_score"], reverse=True)
    return candidates[: RETRIEVAL_PRE_RERANK_K], {
        "dense_candidate_count": dense_candidate_count,
        "lexical_candidate_count": lexical_candidate_count,
        "candidate_count": len(candidates),
        "pre_rerank_count": min(len(candidates), RETRIEVAL_PRE_RERANK_K),
    }


def _expand_parent_families(
    reranked: list[dict[str, Any]],
    stores: dict[str, ChromaStore],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if not RETRIEVAL_ENABLE_PARENT_EXPANSION:
        return reranked[:RETRIEVAL_FINAL_TOP_K], {
            "parent_expansion_enabled": False,
            "parent_expanded_family_count": 0,
            "parent_expanded_extra_chunks": 0,
        }

    final_results: list[dict[str, Any]] = []
    seen_keys: set[str] = set()
    expanded_families: set[tuple[str, str]] = set()
    extra_chunks = 0

    for anchor in reranked[:RETRIEVAL_RERANK_TOP_K]:
        anchor_key = _candidate_key(anchor["collection"], anchor["id"])
        if anchor_key not in seen_keys:
            final_results.append(anchor)
            seen_keys.add(anchor_key)
            if len(final_results) >= RETRIEVAL_FINAL_TOP_K + RETRIEVAL_PARENT_EXPAND_MAX_EXTRA:
                break

        family_id = anchor.get("parent_id") or anchor["id"]
        family_key = (anchor["collection"], family_id)
        if family_key in expanded_families or len(expanded_families) >= RETRIEVAL_PARENT_EXPAND_MAX_FAMILIES:
            continue

        family_rows = stores[anchor["collection"]].expand_family(family_id)
        if len(family_rows) <= 1:
            continue

        expanded_families.add(family_key)
        for family_item in family_rows:
            item = dict(family_item)
            item["collection"] = anchor["collection"]
            item["expanded_from_parent"] = True
            item_key = _candidate_key(item["collection"], item["id"])
            if item_key in seen_keys:
                continue
            final_results.append(item)
            seen_keys.add(item_key)
            extra_chunks += 1
            if len(final_results) >= RETRIEVAL_FINAL_TOP_K + RETRIEVAL_PARENT_EXPAND_MAX_EXTRA:
                break

        if len(final_results) >= RETRIEVAL_FINAL_TOP_K + RETRIEVAL_PARENT_EXPAND_MAX_EXTRA:
            break

    return final_results[: RETRIEVAL_FINAL_TOP_K + RETRIEVAL_PARENT_EXPAND_MAX_EXTRA], {
        "parent_expansion_enabled": True,
        "parent_expanded_family_count": len(expanded_families),
        "parent_expanded_extra_chunks": extra_chunks,
    }


def retrieve_context(state: AgentState) -> dict:
    profile = resolve_profile(state)
    embedder, stores, reranker = get_retriever(profile)
    retrieval_start = time.perf_counter()
    expanded, expansion_log = expand_query(state["user_query"], state["intent"], profile)

    candidates, candidate_meta = _rank_hybrid_candidates(
        expanded_queries=expanded,
        embedder=embedder,
        stores=stores,
    )
    reranked = (
        reranker.rerank(state["user_query"], candidates, top_k=min(RETRIEVAL_RERANK_TOP_K, len(candidates)))
        if candidates
        else []
    )
    final_hits, parent_meta = _expand_parent_families(reranked, stores)
    grouped_hits: dict[str, list[dict]] = defaultdict(list)
    for item in final_hits:
        grouped_hits[item["collection"]].append(item)

    retrieved_details = [
        {
            "rank": idx,
            "id": item["id"],
            "title": item["title"],
            "collection": item["collection"],
            "source": item.get("source"),
            "source_type": item.get("source_type"),
            "heading_path": item.get("heading_path"),
            "parent_id": item.get("parent_id"),
            "level": item.get("level"),
            "part_index": item.get("part_index"),
            "score": item.get("score"),
            "dense_score": item.get("dense_score"),
            "lexical_score": item.get("lexical_score"),
            "hybrid_score": item.get("hybrid_score"),
            "rerank_score": item.get("rerank_score"),
            "expanded_from_parent": bool(item.get("expanded_from_parent")),
        }
        for idx, item in enumerate(final_hits, start=1)
    ]

    docs = load_context_documents(profile)
    context_parts = [
        "# CONTEXT PACKAGE",
        f"## DOMAIN_PROFILE\n{profile.name}",
        f"## DOMAIN_DESCRIPTION\n{profile.description}",
        f"## USER_BRIEF\nsource_ref=user_brief\n{state['user_query']}",
        f"## RETRY_STATUS\nretry_count={state.get('retry_count', 0)}",
        f"## PREVIOUS_ISSUES\nsource_ref=previous_issues\n{format_issue_block(state)}",
    ]

    for doc in profile.context_documents:
        should_include = doc.always_include or not grouped_hits.get(doc.fallback_for or "")
        if should_include:
            context_parts.append(f"## {doc.section_title}\nsource_ref={doc.key}\n{docs[doc.key]}")

    for collection in profile.collections:
        context_parts.append(format_retrieved_block(grouped_hits.get(collection, []), f"RETRIEVED_{collection.upper()}"))

    context = "\n\n".join(context_parts)
    retrieval_latency_ms = int((time.perf_counter() - retrieval_start) * 1000)

    print(
        "[retrieve_context] "
        f"profile={profile.name}, candidates={candidate_meta['candidate_count']}, "
        f"reranked={len(reranked)}, final={len(final_hits)}"
    )
    for item in final_hits:
        rank_signal = item.get("rerank_score", item.get("hybrid_score", 0.0))
        safe_print(f"  [{rank_signal:.3f}] [{item['collection']}] {item['title']}")

    return {
        "retrieved_chunks": [f"[{item['collection']}] {item['title']}" for item in final_hits],
        "retrieved_chunk_details": retrieved_details,
        "context": context,
        "expanded_queries": expanded,
        "call_logs": append_call_log(state, expansion_log),
        "retrieval_metadata": {
            "profile": profile.name,
            "expanded_queries": expanded,
            "candidate_count": candidate_meta["candidate_count"],
            "dense_candidate_count": candidate_meta["dense_candidate_count"],
            "lexical_candidate_count": candidate_meta["lexical_candidate_count"],
            "pre_rerank_count": candidate_meta["pre_rerank_count"],
            "reranked_count": len(reranked),
            "retrieved_count": len(final_hits),
            "retrieval_latency_ms": retrieval_latency_ms,
            "collections_hit": sorted({item["collection"] for item in final_hits}),
            "dense_enabled": RETRIEVAL_ENABLE_DENSE,
            "lexical_enabled": RETRIEVAL_ENABLE_LEXICAL,
            "parent_expansion_enabled": RETRIEVAL_ENABLE_PARENT_EXPANSION,
            "dense_top_k": RETRIEVAL_DENSE_TOP_K,
            "lexical_top_k": RETRIEVAL_LEXICAL_TOP_K,
            "rerank_top_k": RETRIEVAL_RERANK_TOP_K,
            "final_top_k": RETRIEVAL_FINAL_TOP_K,
            **parent_meta,
        },
    }


def build_prompt(state: AgentState) -> dict:
    profile = resolve_profile(state)
    outline = "\n".join(f"- {item}" for item in profile.builder_outline)
    allowed_source_refs = [
        "user_brief",
        "previous_issues",
        *[doc.key for doc in profile.context_documents],
        *[item["id"] for item in state.get("retrieved_chunk_details") or []],
    ]
    prompt = f"""Compress the following context into a high-fidelity execution spec for the downstream model.

Requirements:
1. Keep precise values, thresholds, identifiers, accessibility requirements, forbidden items, and named codes.
2. Distinguish mandatory constraints from optional guidance.
3. Convert previous validation failures into explicit repair requirements.
4. Be query-aware: prefer the smallest set of constraints that preserves correctness for this task.
5. Do not restate near-duplicate requirements across multiple sections.
6. Prefer acceptance checks for testable outcomes instead of turning every detail into a hard constraint.
7. Follow this outline:
{outline}
8. Use only these source refs when citing evidence:
{", ".join(allowed_source_refs) if allowed_source_refs else "(none)"}

{EXECUTION_SPEC_SCHEMA_TEXT}

Context:
{state['context']}
"""

    raw_output, in_tok, out_tok = call_openai(
        prompt,
        system=profile.prompt_build_system,
        model=PROMPT_BUILD_MODEL,
        max_tokens=16000,
        reasoning_effort=PROMPT_BUILD_REASONING_EFFORT,
    )
    execution_spec, parse_meta = parse_execution_spec(
        raw_output,
        output_format=profile.output_format,
        task_summary=state["user_query"],
        allowed_source_refs=allowed_source_refs,
    )
    built_prompt = render_execution_spec_brief(execution_spec)
    execution_spec_json = render_execution_spec(execution_spec)
    used_source_refs = collect_source_refs(execution_spec)
    log_entry = make_call_log(
        stage="build_prompt",
        model=PROMPT_BUILD_MODEL,
        reasoning_effort=PROMPT_BUILD_REASONING_EFFORT,
        max_tokens=16000,
        prompt=prompt,
        system=profile.prompt_build_system,
        output=built_prompt,
        input_tokens=in_tok,
        output_tokens=out_tok,
    )
    print(f"[build_prompt] profile={profile.name}, input={in_tok}, output={out_tok}, chars={len(built_prompt)}")
    return {
        "built_prompt": built_prompt,
        "execution_spec": execution_spec,
        "call_logs": append_call_log(state, log_entry),
        "compression_metadata": {
            "mode": "structured_execution_spec",
            "model": PROMPT_BUILD_MODEL,
            "reasoning_effort": PROMPT_BUILD_REASONING_EFFORT,
            "input_tokens": in_tok,
            "output_tokens": out_tok,
            "input_chars": len(state["context"]),
            "output_chars": len(built_prompt),
            "json_output_chars": len(execution_spec_json),
            "retention_ratio": round(out_tok / in_tok, 4) if in_tok else None,
            "used_source_ref_count": len(used_source_refs),
            "allowed_source_ref_count": len(set(allowed_source_refs)),
            "hard_constraint_count": len(execution_spec.get("hard_constraints") or []),
            "interaction_requirement_count": len(execution_spec.get("interaction_requirements") or []),
            "acceptance_check_count": len(execution_spec.get("acceptance_checks") or []),
        },
        "spec_parse_metadata": parse_meta,
    }


def generate(state: AgentState) -> dict:
    profile = resolve_profile(state)
    execution_spec_text = state.get("built_prompt") or render_execution_spec(state.get("execution_spec") or {})
    prompt = f"""Here is the execution spec:

{execution_spec_text}

---

Original user request:
{state['user_query']}

{format_issue_block(state)}

Generate the final deliverable now."""

    result, in_tok, out_tok = call_openai(
        prompt,
        system=profile.generate_system,
        model=GENERATION_MODEL,
        max_tokens=32000,
        reasoning_effort=GENERATION_REASONING_EFFORT,
    )
    cleaned = clean_model_output(result, profile.output_format)
    log_entry = make_call_log(
        stage="generate",
        model=GENERATION_MODEL,
        reasoning_effort=GENERATION_REASONING_EFFORT,
        max_tokens=32000,
        prompt=prompt,
        system=profile.generate_system,
        output=cleaned,
        input_tokens=in_tok,
        output_tokens=out_tok,
    )
    print(
        f"[generate] profile={profile.name}, input={in_tok}, output={out_tok}, "
        f"chars={len(cleaned)}"
    )
    return {
        "generation_result": cleaned,
        "call_logs": append_call_log(state, log_entry),
        "generation_metadata": {
            "model": GENERATION_MODEL,
            "reasoning_effort": GENERATION_REASONING_EFFORT,
            "input_tokens": in_tok,
            "output_tokens": out_tok,
            "input_chars": len(prompt),
            "output_chars": len(cleaned),
            "output_format": profile.output_format,
            "spec_mode": "structured_execution_spec",
        },
    }


def quality_check(state: AgentState) -> dict:
    profile = resolve_profile(state)
    validator = get_profile_validator(profile)
    report = validator.validate(state.get("generation_result", ""))
    passed = report["pass"]
    retry_count = state.get("retry_count", 0) + (0 if passed else 1)

    print(f"[quality_check] profile={profile.name}, pass={passed}, retry_count={retry_count}")
    for issue in report["issues"][:8]:
        safe_print(f"  - [{issue['severity']}] {issue['message']}")

    return {
        "quality_check": report,
        "retry_count": retry_count,
    }
