import argparse
import sys

sys.path.insert(0, ".")

from src.chunking.structured_tag import split_by_h2, split_techniques
from src.config import CHROMA_DB_PATH
from src.domain_profiles import get_domain_profile
from src.indexing.chroma_store import ChromaStore
from src.indexing.embedder import Embedder


def build_collection(store: ChromaStore, embedder: Embedder, chunks: list, label: str) -> None:
    print(f"\n--- {label}: {len(chunks)} chunks ---")
    embeddings = embedder.embed([c["content"] for c in chunks])
    store.add(chunks, embeddings)


def maybe_reset(store: ChromaStore, rebuild: bool) -> None:
    if rebuild and store.collection.count() > 0:
        store.clear()


def load_chunks(source):
    if source.splitter == "techniques":
        return split_techniques(source.path)
    if source.splitter == "h2":
        return split_by_h2(source.path, source.source_name)
    raise ValueError(f"Unknown splitter: {source.splitter}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", default=None, help="Domain profile name. Defaults to AGENT_DOMAIN.")
    parser.add_argument("--rebuild", action="store_true", help="Clear existing collections before rebuilding.")
    args = parser.parse_args()

    profile = get_domain_profile(args.domain)
    embedder = Embedder()

    if not profile.index_sources:
        print(f"[info] domain '{profile.name}' has no index sources to build")
        return

    built_stores = []
    for source in profile.index_sources:
        store = ChromaStore(CHROMA_DB_PATH, source.collection)
        maybe_reset(store, args.rebuild)
        if store.collection.count() == 0:
            chunks = load_chunks(source)
            build_collection(store, embedder, chunks, f"{profile.name}:{source.label}")
        else:
            print(f"[skip] {source.collection} already has {store.collection.count()} rows")
        built_stores.append((source.collection, store))

    print("\n=== Retrieval smoke check ===")
    test_query = f"domain={profile.name}; retrieve the most relevant SOP references for a complex generation task"
    query_vec = embedder.embed([test_query])[0]
    for name, store in built_stores:
        results = store.query(query_vec, top_k=3)
        print(f"\n[{name}] top3:")
        for item in results:
            print(f"  [{item['score']:.3f}] {item['title']}")


if __name__ == "__main__":
    main()
