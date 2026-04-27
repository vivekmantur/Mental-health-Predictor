import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class DSMEmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.data = self.load_data()
        self.texts = self.prepare_texts()
        self.embeddings = self.model.encode(self.texts)

    # ---------------------------------------------------------
    # Load DSM Knowledge Base
    # ---------------------------------------------------------
    def load_data(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_dir, "core", "knowledge", "dsm_knowledge_base.json")

        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)["disorders"]

    # ---------------------------------------------------------
    # Prepare Text for Embedding
    # ---------------------------------------------------------
    def prepare_texts(self):
        texts = []
        for item in self.data:
            keywords = ", ".join(item.get("keywords", []))
            combined = f"{item.get('category')} - {item.get('disorder')}. Symptoms include {keywords}."
            texts.append(combined.strip())
        return texts

    # ---------------------------------------------------------
    # Find Best Matching Disorder
    # ---------------------------------------------------------
    def find_best_match(self, user_input: str):
        if not user_input or not user_input.strip():
            return {
                "category": None,
                "subcategory": None,
                "disorder": None
            }

        user_input = f"Symptoms: {user_input.lower().strip()}"

        user_embedding = self.model.encode([user_input])
        scores = cosine_similarity(user_embedding, self.embeddings)[0]

        best_index = int(np.argmax(scores))
        best_score = float(scores[best_index])
        best_match = self.data[best_index]

        if best_score < 0.5:
            return {
                "category": None,
                "subcategory": None,
                "disorder": None
            }

        return {
            "category": best_match.get("category"),
            "subcategory": best_match.get("subcategory"),
            "disorder": best_match.get("disorder")
        }