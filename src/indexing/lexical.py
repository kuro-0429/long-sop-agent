from __future__ import annotations

import math
import re
from collections import Counter
from typing import Any

TOKEN_RE = re.compile(r"[A-Za-z0-9_]+(?:-[A-Za-z0-9_]+)*|[\u4e00-\u9fff]+")


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text or "")]


def _compose_lexical_text(row: dict[str, Any]) -> str:
    parts = [
        row.get("title") or "",
        row.get("heading_path") or "",
        row.get("content") or "",
    ]
    return "\n".join(part for part in parts if part)


def bm25_rank_documents(
    query: str,
    rows: list[dict[str, Any]],
    *,
    top_k: int = 10,
    k1: float = 1.5,
    b: float = 0.75,
) -> list[dict[str, Any]]:
    query_tokens = tokenize(query)
    if not query_tokens or not rows:
        return []

    document_tokens = [tokenize(_compose_lexical_text(row)) for row in rows]
    lengths = [max(1, len(tokens)) for tokens in document_tokens]
    avg_length = sum(lengths) / len(lengths)

    doc_freq = Counter()
    for tokens in document_tokens:
        doc_freq.update(set(tokens))

    scored_rows: list[dict[str, Any]] = []
    query_counts = Counter(query_tokens)
    doc_count = len(rows)

    for row, tokens, length in zip(rows, document_tokens, lengths):
        token_counts = Counter(tokens)
        score = 0.0
        for term, qtf in query_counts.items():
            tf = token_counts.get(term, 0)
            if tf <= 0:
                continue
            df = doc_freq.get(term, 0)
            idf = math.log(1 + ((doc_count - df + 0.5) / (df + 0.5)))
            numerator = tf * (k1 + 1)
            denominator = tf + k1 * (1 - b + b * (length / avg_length))
            score += qtf * idf * (numerator / denominator)

        if score <= 0:
            continue

        item = dict(row)
        item["lexical_score"] = round(score, 6)
        scored_rows.append(item)

    scored_rows.sort(key=lambda item: item["lexical_score"], reverse=True)
    return scored_rows[:top_k]
