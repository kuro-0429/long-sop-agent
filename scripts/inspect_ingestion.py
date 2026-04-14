import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, ".")

from src.chunking.generic import split_generic_document
from src.ingestion import parse_document


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect generic document parsing and chunking output.")
    parser.add_argument("filepath", help="Path to the input document.")
    parser.add_argument("--source-name", default=None, help="Logical source name. Defaults to file stem.")
    parser.add_argument("--max-chars", type=int, default=5000, help="Chunk size budget.")
    parser.add_argument("--overlap-chars", type=int, default=400, help="Chunk overlap budget.")
    parser.add_argument("--no-root", action="store_true", help="Drop root-like sections.")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable summary.")
    args = parser.parse_args()

    path = Path(args.filepath)
    source_name = args.source_name or path.stem

    parsed = parse_document(str(path), source_name)
    chunks = split_generic_document(
        str(path),
        source_name,
        include_root_chunk=not args.no_root,
        max_chars=args.max_chars,
        overlap_chars=args.overlap_chars,
    )

    summary = {
        "path": str(path),
        "source_name": source_name,
        "source_type": parsed.source_type,
        "document_title": parsed.title,
        "section_count": len(parsed.sections),
        "chunk_count": len(chunks),
        "sections": [
            {
                "index": idx,
                "title": section.title,
                "level": section.level,
                "heading_path": list(section.heading_path),
                "content_chars": len(section.content),
                "source_type": section.source_type,
            }
            for idx, section in enumerate(parsed.sections, start=1)
        ],
        "chunks": [
            {
                "id": chunk["id"],
                "title": chunk["title"],
                "content_chars": len(chunk["content"]),
                "heading_path": chunk.get("heading_path"),
                "level": chunk.get("level"),
                "part_index": chunk.get("part_index"),
                "source_type": chunk.get("source_type"),
            }
            for chunk in chunks
        ],
    }

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return

    print(f"document: {summary['path']}")
    print(f"source_type: {summary['source_type']}")
    print(f"title: {summary['document_title']}")
    print(f"sections: {summary['section_count']}")
    print(f"chunks: {summary['chunk_count']}")
    print("\nsection preview:")
    for section in summary["sections"][:8]:
        print(
            f"  [{section['index']}] level={section['level']} "
            f"chars={section['content_chars']} path={' > '.join(section['heading_path'])}"
        )
    if len(summary["sections"]) > 8:
        print(f"  ... ({len(summary['sections']) - 8} more sections)")

    print("\nchunk preview:")
    for chunk in summary["chunks"][:8]:
        print(
            f"  [{chunk['id']}] level={chunk['level']} part={chunk['part_index']} "
            f"chars={chunk['content_chars']} path={chunk['heading_path']}"
        )
    if len(summary["chunks"]) > 8:
        print(f"  ... ({len(summary['chunks']) - 8} more chunks)")


if __name__ == "__main__":
    main()
