from __future__ import annotations

from typing import Iterable


def split_text_with_overlap(
    text: str,
    *,
    max_chars: int = 5000,
    overlap_chars: int = 400,
) -> list[str]:
    text = (text or "").strip()
    if not text:
        return []
    if len(text) <= max_chars:
        return [text]

    chunks: list[str] = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = min(start + max_chars, text_len)
        if end < text_len:
            window = text[start:end]
            split_at = max(
                window.rfind("\n\n"),
                window.rfind("\n"),
                window.rfind(". "),
                window.rfind("。"),
                window.rfind("；"),
                window.rfind(";"),
                window.rfind(" "),
            )
            if split_at > max_chars // 2:
                end = start + split_at

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end >= text_len:
            break
        start = max(end - overlap_chars, start + 1)

    return chunks


def merge_paragraphs_with_budget(
    paragraphs: Iterable[str],
    *,
    max_chars: int = 5000,
    overlap_paragraphs: int = 1,
) -> list[str]:
    parts = [p.strip() for p in paragraphs if p and p.strip()]
    if not parts:
        return []

    chunks: list[str] = []
    current: list[str] = []
    current_len = 0

    for paragraph in parts:
        add_len = len(paragraph) + (2 if current else 0)
        if current and current_len + add_len > max_chars:
            chunks.append("\n\n".join(current).strip())
            overlap = current[-overlap_paragraphs:] if overlap_paragraphs > 0 else []
            current = list(overlap)
            current_len = sum(len(item) for item in current) + max(0, 2 * (len(current) - 1))

        current.append(paragraph)
        current_len += add_len if len(current) > 1 else len(paragraph)

    if current:
        chunks.append("\n\n".join(current).strip())

    return chunks
