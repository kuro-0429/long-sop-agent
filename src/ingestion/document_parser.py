from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    yaml = None


@dataclass(frozen=True)
class ParsedSection:
    title: str
    level: int
    content: str
    heading_path: tuple[str, ...]
    source_type: str
    metadata: dict[str, Any]


@dataclass(frozen=True)
class ParsedDocument:
    path: str
    source_name: str
    source_type: str
    title: str
    sections: tuple[ParsedSection, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "source_name": self.source_name,
            "source_type": self.source_type,
            "title": self.title,
            "sections": [asdict(section) for section in self.sections],
        }


HEADING_RE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")


def _normalize_text(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.replace("\r\n", "\n").replace("\r", "\n").splitlines()).strip()


def _paragraphs_from_text(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"\n\s*\n", _normalize_text(text)) if part.strip()]


def _truncate_title(title: str, limit: int = 80) -> str:
    text = " ".join(title.split())
    return text if len(text) <= limit else f"{text[: limit - 3]}..."


class _HTMLSectionParser(HTMLParser):
    BLOCK_TAGS = {
        "p",
        "div",
        "section",
        "article",
        "header",
        "footer",
        "main",
        "aside",
        "li",
        "ul",
        "ol",
        "table",
        "tr",
        "td",
        "th",
        "br",
        "pre",
        "code",
    }

    def __init__(self) -> None:
        super().__init__()
        self._sections: list[dict[str, Any]] = []
        self._stack: list[tuple[int, str]] = []
        self._current_lines: list[str] = []
        self._current_title = "Document"
        self._current_level = 1
        self._capture_heading_level: int | None = None
        self._heading_buffer: list[str] = []
        self._skip_tag: str | None = None

    def _append_text(self, text: str) -> None:
        cleaned = re.sub(r"\s+", " ", unescape(text or "")).strip()
        if cleaned:
            self._current_lines.append(cleaned)

    def _flush_section(self) -> None:
        content = _normalize_text("\n".join(self._current_lines))
        if content:
            self._sections.append(
                {
                    "title": self._current_title,
                    "level": self._current_level,
                    "content": content,
                    "heading_path": tuple(title for _, title in self._stack) or (self._current_title,),
                }
            )
        self._current_lines = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in {"script", "style"}:
            self._skip_tag = tag
            return
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self._capture_heading_level = int(tag[1])
            self._heading_buffer = []
            return
        if tag == "br":
            self._current_lines.append("")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if self._skip_tag == tag:
            self._skip_tag = None
            return
        if self._capture_heading_level and tag == f"h{self._capture_heading_level}":
            title = _truncate_title(" ".join(self._heading_buffer).strip()) or f"Section {len(self._sections) + 1}"
            self._flush_section()
            level = self._capture_heading_level
            while self._stack and self._stack[-1][0] >= level:
                self._stack.pop()
            self._stack.append((level, title))
            self._current_title = title
            self._current_level = level
            self._capture_heading_level = None
            self._heading_buffer = []
            return
        if tag in self.BLOCK_TAGS and self._current_lines and self._current_lines[-1] != "":
            self._current_lines.append("")

    def handle_data(self, data: str) -> None:
        if self._skip_tag:
            return
        if self._capture_heading_level:
            self._heading_buffer.append(data)
            return
        self._append_text(data)

    def parsed_sections(self) -> list[dict[str, Any]]:
        self._flush_section()
        return [section for section in self._sections if section["content"].strip()]


def _parse_markdown(path: Path, source_name: str) -> ParsedDocument:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    sections: list[ParsedSection] = []
    stack: list[tuple[int, str]] = []
    current_lines: list[str] = []
    current_title = path.stem
    current_level = 1
    in_fence = False

    def flush_current() -> None:
        nonlocal current_lines, current_title, current_level
        content = _normalize_text("\n".join(current_lines))
        if not content:
            current_lines = []
            return
        sections.append(
            ParsedSection(
                title=current_title,
                level=current_level,
                content=content,
                heading_path=tuple(title for _, title in stack) or (current_title,),
                source_type="markdown",
                metadata={"path": str(path)},
            )
        )
        current_lines = []

    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            current_lines.append(line)
            continue

        match = None if in_fence else HEADING_RE.match(line)
        if match:
            level = len(match.group(1))
            title = _normalize_text(match.group(2))
            flush_current()
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, title))
            current_title = title or path.stem
            current_level = level
            current_lines = [line]
            continue
        current_lines.append(line)

    flush_current()
    title = sections[0].title if sections else path.stem
    return ParsedDocument(
        path=str(path),
        source_name=source_name,
        source_type="markdown",
        title=title,
        sections=tuple(sections),
    )


def _parse_html(path: Path, source_name: str) -> ParsedDocument:
    parser = _HTMLSectionParser()
    parser.feed(path.read_text(encoding="utf-8", errors="ignore"))
    raw_sections = parser.parsed_sections()
    sections = tuple(
        ParsedSection(
            title=section["title"],
            level=section["level"],
            content=section["content"],
            heading_path=tuple(section["heading_path"]),
            source_type="html",
            metadata={"path": str(path)},
        )
        for section in raw_sections
    )
    title = sections[0].title if sections else path.stem
    return ParsedDocument(
        path=str(path),
        source_name=source_name,
        source_type="html",
        title=title,
        sections=sections,
    )


def _flatten_mapping(value: Any, prefix: tuple[str, ...] = ()) -> list[tuple[tuple[str, ...], Any]]:
    if isinstance(value, dict):
        items: list[tuple[tuple[str, ...], Any]] = []
        for key, child in value.items():
            items.extend(_flatten_mapping(child, prefix + (str(key),)))
        return items
    if isinstance(value, list):
        if all(not isinstance(item, (dict, list)) for item in value):
            return [(prefix, value)]
        items: list[tuple[tuple[str, ...], Any]] = []
        for idx, child in enumerate(value):
            items.extend(_flatten_mapping(child, prefix + (f"[{idx}]",)))
        return items
    return [(prefix, value)]


def _parse_structured(path: Path, source_name: str, source_type: str) -> ParsedDocument:
    raw_text = path.read_text(encoding="utf-8")
    if source_type == "json":
        payload = json.loads(raw_text)
    else:
        if yaml is None:
            raise RuntimeError("PyYAML is required to parse YAML documents.")
        payload = yaml.safe_load(raw_text)

    flattened = _flatten_mapping(payload)
    sections: list[ParsedSection] = []
    for idx, (path_parts, value) in enumerate(flattened, start=1):
        title = " > ".join(path_parts) if path_parts else path.stem
        if isinstance(value, list):
            content = "\n".join(f"- {item}" for item in value)
        elif isinstance(value, (dict, list)):
            content = json.dumps(value, ensure_ascii=False, indent=2)
        else:
            content = str(value)
        content = _normalize_text(content)
        if not content:
            continue
        sections.append(
            ParsedSection(
                title=_truncate_title(title or f"{path.stem}-{idx}"),
                level=max(1, len(path_parts) or 1),
                content=content,
                heading_path=tuple(path_parts) if path_parts else (path.stem,),
                source_type=source_type,
                metadata={"path": str(path)},
            )
        )

    return ParsedDocument(
        path=str(path),
        source_name=source_name,
        source_type=source_type,
        title=path.stem,
        sections=tuple(sections),
    )


def _parse_text(path: Path, source_name: str) -> ParsedDocument:
    paragraphs = _paragraphs_from_text(path.read_text(encoding="utf-8", errors="ignore"))
    sections = tuple(
        ParsedSection(
            title=f"{path.stem} paragraph {idx}",
            level=1,
            content=paragraph,
            heading_path=(path.stem, f"paragraph {idx}"),
            source_type="text",
            metadata={"path": str(path)},
        )
        for idx, paragraph in enumerate(paragraphs, start=1)
    )
    return ParsedDocument(
        path=str(path),
        source_name=source_name,
        source_type="text",
        title=path.stem,
        sections=sections,
    )


def parse_document(filepath: str, source_name: str) -> ParsedDocument:
    path = Path(filepath)
    suffix = path.suffix.lower()
    if suffix in {".md", ".markdown"}:
        return _parse_markdown(path, source_name)
    if suffix in {".html", ".htm"}:
        return _parse_html(path, source_name)
    if suffix == ".json":
        return _parse_structured(path, source_name, "json")
    if suffix in {".yaml", ".yml"}:
        return _parse_structured(path, source_name, "yaml")
    return _parse_text(path, source_name)
