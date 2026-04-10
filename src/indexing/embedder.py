# src/indexing/embedder.py
from sentence_transformers import SentenceTransformer
from typing import List

class Embedder:
    def __init__(self, model_name: str = "BAAI/bge-large-zh-v1.5"):
        print(f"[Embedder] 加载模型 {model_name}...")
        self.model = SentenceTransformer(model_name)
        print("[Embedder] 模型加载完成")

    def embed(self, texts: List[str]) -> List[List[float]]:
        """把文本列表转成向量列表"""
        vectors = self.model.encode(
            texts,
            normalize_embeddings=True,  # 归一化，余弦相似度更准
            show_progress_bar=True,
        )
        return vectors.tolist()
