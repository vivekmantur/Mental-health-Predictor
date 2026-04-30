"""
DSM Embedding Service

This module provides semantic matching between user input (notes/symptoms)
and a predefined DSM knowledge base.

It uses:
- SentenceTransformers for embedding generation
- Cosine similarity for semantic matching

Purpose:
- Map user symptoms → DSM category / disorder
- Enhance PHQ-9 results with clinical context
"""

import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class DSMEmbeddingService:
    """
    Service for semantic matching of user symptoms against DSM knowledge base.

    Workflow:
        1. Load DSM dataset
        2. Convert each disorder into descriptive text
        3. Generate embeddings for all entries
        4. Compare user input embedding using cosine similarity
        5. Return best matching disorder (if confidence threshold met)
    """

    def __init__(self):
        """
        Initialize embedding model and precompute embeddings.

        Notes:
            - Model is loaded once per instance
            - Embeddings are precomputed for performance
        """

        # Pretrained lightweight embedding model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

        # Load DSM knowledge base
        self.data = self.load_data()

        # Prepare text corpus for embedding
        self.texts = self.prepare_texts()

        # Precompute embeddings for all DSM entries
        self.embeddings = self.model.encode(self.texts)

    # ---------------------------------------------------------
    # Load DSM Knowledge Base
    # ---------------------------------------------------------
    def load_data(self):
        """
        Load DSM knowledge base from JSON file.

        Returns:
            list: List of disorder entries

        File Structure:
            {
                "disorders": [
                    {
                        "category": "...",
                        "subcategory": "...",
                        "disorder": "...",
                        "keywords": [...]
                    }
                ]
            }
        """

        # Navigate to project root → core/knowledge folder
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(
            base_dir,
            "core",
            "knowledge",
            "dsm_knowledge_base.json"
        )

        # Load JSON data
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)["disorders"]

    # ---------------------------------------------------------
    # Prepare Text for Embedding
    # ---------------------------------------------------------
    def prepare_texts(self):
        """
        Convert structured DSM data into embedding-friendly text.

        Returns:
            list[str]: List of combined textual descriptions

        Example Output:
            "Depression - Major Depressive Disorder. Symptoms include sadness, fatigue, insomnia."
        """

        texts = []

        for item in self.data:
            keywords = ", ".join(item.get("keywords", []))

            # Combine category, disorder, and symptoms into one sentence
            combined = (
                f"{item.get('category')} - {item.get('disorder')}. "
                f"Symptoms include {keywords}."
            )

            texts.append(combined.strip())

        return texts

    # ---------------------------------------------------------
    # Find Best Matching Disorder
    # ---------------------------------------------------------
    def find_best_match(self, user_input: str):
        """
        Find the closest DSM disorder based on user input.

        Args:
            user_input (str): Free-text input (user notes/symptoms)

        Returns:
            dict:
                - category (str | None)
                - subcategory (str | None)
                - disorder (str | None)

        Logic:
            - Convert input into embedding
            - Compute cosine similarity against DSM embeddings
            - Select highest scoring match
            - Apply threshold to avoid weak matches

        Threshold:
            - If similarity < 0.5 → return None values
        """

        # Handle empty input case
        if not user_input or not user_input.strip():
            return {
                "category": None,
                "subcategory": None,
                "disorder": None
            }

        # Normalize input (helps embedding quality)
        user_input = f"Symptoms: {user_input.lower().strip()}"

        # Generate embedding for user input
        user_embedding = self.model.encode([user_input])

        # Compute cosine similarity with DSM embeddings
        scores = cosine_similarity(user_embedding, self.embeddings)[0]

        # Identify best match
        best_index = int(np.argmax(scores))
        best_score = float(scores[best_index])
        best_match = self.data[best_index]

        # Apply confidence threshold
        if best_score < 0.5:
            return {
                "category": None,
                "subcategory": None,
                "disorder": None
            }

        # Return matched DSM classification
        return {
            "category": best_match.get("category"),
            "subcategory": best_match.get("subcategory"),
            "disorder": best_match.get("disorder")
        }