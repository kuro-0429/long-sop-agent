from typing import Any, Dict, List

import chromadb
from src.indexing.lexical import bm25_rank_documents


class ChromaStore:
    def __init__(self, persist_dir: str = "./chroma_db", collection_name: str = "techniques"):
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )
        self._rows_cache: list[dict[str, Any]] | None = None
        print(f"[ChromaStore] collection='{collection_name}', count={self.collection.count()}")

    def add(self, chunks: List[Dict], embeddings: List[List[float]]) -> None:
        metadatas = []
        for chunk in chunks:
            metadata = {"title": chunk["title"], "source": chunk["source"]}
            for key in ("heading_path", "parent_id", "level", "part_index", "source_type"):
                value = chunk.get(key)
                if value not in (None, "", []):
                    metadata[key] = value
            metadatas.append(metadata)

        self.collection.add(
            ids=[c["id"] for c in chunks],
            documents=[c["content"] for c in chunks],
            embeddings=embeddings,
            metadatas=metadatas,
        )
        self._rows_cache = None
        print(f"[ChromaStore] wrote {len(chunks)} rows, total={self.collection.count()}")

    def clear(self) -> None:
        ids = self.collection.get(include=[])["ids"]
        if ids:
            self.collection.delete(ids=ids)
        self._rows_cache = None
        print(f"[ChromaStore] cleared collection, total={self.collection.count()}")

    def all_rows(self) -> list[dict[str, Any]]:
        if self._rows_cache is not None:
            return [dict(item) for item in self._rows_cache]

        if self.collection.count() == 0:
            self._rows_cache = []
            return []

        results = self.collection.get(include=["documents", "metadatas"])
        rows: list[dict[str, Any]] = []
        ids = results.get("ids") or []
        documents = results.get("documents") or []
        metadatas = results.get("metadatas") or []

        for idx, chunk_id in enumerate(ids):
            metadata = metadatas[idx] or {}
            rows.append(
                {
                    "id": chunk_id,
                    "content": documents[idx],
                    "title": metadata.get("title"),
                    "source": metadata.get("source"),
                    "source_type": metadata.get("source_type"),
                    "heading_path": metadata.get("heading_path"),
                    "parent_id": metadata.get("parent_id"),
                    "level": metadata.get("level"),
                    "part_index": metadata.get("part_index"),
                }
            )

        self._rows_cache = rows
        return [dict(item) for item in rows]

    def query(self, query_vector: List[float], top_k: int = 10) -> List[Dict]:
        if self.collection.count() == 0:
            return []

        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=min(top_k, self.collection.count()),
        )

        chunks = []
        for i in range(len(results["ids"][0])):
            chunks.append(
                {
                    "id": results["ids"][0][i],
                    "content": results["documents"][0][i],
                    "title": results["metadatas"][0][i]["title"],
                    "source": results["metadatas"][0][i].get("source"),
                    "source_type": results["metadatas"][0][i].get("source_type"),
                    "heading_path": results["metadatas"][0][i].get("heading_path"),
                    "parent_id": results["metadatas"][0][i].get("parent_id"),
                    "level": results["metadatas"][0][i].get("level"),
                    "part_index": results["metadatas"][0][i].get("part_index"),
                    "score": 1 - results["distances"][0][i],
                }
            )
        return chunks

    def query_lexical(self, query_text: str, top_k: int = 10) -> List[Dict]:
        return bm25_rank_documents(query_text, self.all_rows(), top_k=top_k)

    def expand_family(self, family_id: str) -> list[dict[str, Any]]:
        if not family_id:
            return []

        rows = [
            row
            for row in self.all_rows()
            if row["id"] == family_id or row.get("parent_id") == family_id
        ]
        rows.sort(
            key=lambda row: (
                0 if row["id"] == family_id else 1,
                int(row.get("part_index") or 1),
                row["id"],
            )
        )
        return rows
