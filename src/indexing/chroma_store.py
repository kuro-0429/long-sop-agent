from typing import Dict, List

import chromadb


class ChromaStore:
    def __init__(self, persist_dir: str = "./chroma_db", collection_name: str = "techniques"):
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )
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
        print(f"[ChromaStore] wrote {len(chunks)} rows, total={self.collection.count()}")

    def clear(self) -> None:
        ids = self.collection.get(include=[])["ids"]
        if ids:
            self.collection.delete(ids=ids)
        print(f"[ChromaStore] cleared collection, total={self.collection.count()}")

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
