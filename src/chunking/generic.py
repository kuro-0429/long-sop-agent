from __future__ import annotations

import re
from pathlib import Path

from src.chunking.fixed_window import merge_paragraphs_with_budget, split_text_with_overlap

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
TECHNIQUE_ID_RE = re.compile(r"\bT-\d+\b")


def _normalize_title(raw: str) -> str:
    return raw.strip().strip("#").strip()


def _extract_technique_id(title: str) -> str | None:
    match = TECHNIQUE_ID_RE.search(title)
    return match.group(0) if match else None


def _make_chunk_id(
    *,
    source_name: str,
    section_index: int,
    title: str,
    part_index: int = 1,
) -> str:
    base = _extract_technique_id(title) or f"{source_name}-{section_index:03d}"
    return base if part_index == 1 else f"{base}-p{part_index:02d}"


def _split_section_with_budget(
    *,
    section_text: str,
    title: str,
    source_name: str,
    section_index: int,
    heading_path: list[str],
    level: int,
    max_chars: int,
    overlap_chars: int,
) -> list[dict]:
    text = section_text.strip()
    if not text:
        return []

    lines = text.splitlines()
    title_line = lines[0].strip() if lines else title
    body = "\n".join(lines[1:]).strip()

    if len(text) <= max_chars:
        return [
            {
                "id": _make_chunk_id(
                    source_name=source_name,
                    section_index=section_index,
                    title=title,
                ),
                "title": title,
                "content": text,
                "source": source_name,
                "heading_path": " > ".join(heading_path),
                "parent_id": "",
                "level": level,
                "part_index": 1,
            }
        ]

    paragraphs = body.split("\n\n") if body else []
    body_chunks = merge_paragraphs_with_budget(
        paragraphs,
        max_chars=max(800, max_chars - len(title_line) - 16),
        overlap_paragraphs=1,
    )
    if not body_chunks:
        body_chunks = split_text_with_overlap(body or text, max_chars=max_chars, overlap_chars=overlap_chars)

    parent_id = _make_chunk_id(
        source_name=source_name,
        section_index=section_index,
        title=title,
    )
    chunks: list[dict] = []
    for part_index, body_chunk in enumerate(body_chunks, start=1):
        content = f"{title_line}\n\n{body_chunk}".strip()
        chunks.append(
            {
                "id": _make_chunk_id(
                    source_name=source_name,
                    section_index=section_index,
                    title=title,
                    part_index=part_index,
                ),
                "title": title if part_index == 1 else f"{title} (Part {part_index})",
                "content": content,
                "source": source_name,
                "heading_path": " > ".join(heading_path),
                "parent_id": parent_id,
                "level": level,
                "part_index": part_index,
            }
        )
    return chunks


def split_markdown_headings(
    filepath: str,
    source_name: str,
    *,
    split_heading_level: int = 2,
    include_root_chunk: bool = True,
    max_chars: int = 5000,
    overlap_chars: int = 400,
) -> list[dict]:
    text = Path(filepath).read_text(encoding="utf-8")
    lines = text.splitlines()

    chunks: list[dict] = []
    root_title = source_name
    preamble_lines: list[str] = []
    current_lines: list[str] = []
    current_title = ""
    current_path: list[str] = []
    section_index = 0

    def flush_current() -> None:
        nonlocal current_lines, current_title, current_path, section_index, chunks
        section_text = "\n".join(current_lines).strip()
        if not section_text or not current_title:
            current_lines = []
            return
        chunks.extend(
            _split_section_with_budget(
                section_text=section_text,
                title=current_title,
                source_name=source_name,
                section_index=section_index,
                heading_path=current_path or [current_title],
                level=split_heading_level,
                max_chars=max_chars,
                overlap_chars=overlap_chars,
            )
        )
        current_lines = []

    for line in lines:
        match = HEADING_RE.match(line)
        if match:
            level = len(match.group(1))
            title = _normalize_title(match.group(2))
            if level == 1 and title:
                root_title = title
            if level == split_heading_level:
                flush_current()
                if current_title or preamble_lines:
                    section_index += 1
                current_title = title
                current_path = [root_title, title] if root_title and root_title != title else [title]
                current_lines = [line]
                continue

        if current_lines:
            current_lines.append(line)
        else:
            preamble_lines.append(line)

    flush_current()

    preamble_text = "\n".join(preamble_lines).strip()
    if include_root_chunk and preamble_text:
        preamble_chunks = _split_section_with_budget(
            section_text=preamble_text,
            title=root_title,
            source_name=source_name,
            section_index=0,
            heading_path=[root_title],
            level=1,
            max_chars=max_chars,
            overlap_chars=overlap_chars,
        )
        chunks = preamble_chunks + chunks

    return chunks
