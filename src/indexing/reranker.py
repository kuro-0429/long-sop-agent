# src/indexing/reranker.py
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from typing import List, Dict

class Reranker:
    def __init__(self, model_name: str = "BAAI/bge-reranker-v2-m3"):
        print(f"[Reranker] 加载模型 {model_name}...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.model.eval()
        print("[Reranker] 加载完成")

    def rerank(self, query: str, chunks: List[Dict], top_k: int = 5) -> List[Dict]:
        pairs = [[query, c["content"][:512]] for c in chunks]
        inputs = self.tokenizer(
            pairs,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors="pt",
        )
        with torch.no_grad():
            scores = self.model(**inputs).logits.squeeze(-1)
            scores = torch.sigmoid(scores).tolist()

        if isinstance(scores, float):
            scores = [scores]

        for i, chunk in enumerate(chunks):
            chunk["rerank_score"] = scores[i]

        reranked = sorted(chunks, key=lambda x: x["rerank_score"], reverse=True)
        return reranked[:top_k]
