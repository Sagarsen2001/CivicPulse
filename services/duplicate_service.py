"""
=========================================
CivicPulse Duplicate Detection Service
=========================================

Detects potential duplicate complaints
using text similarity, category matching,
and location proximity.

Uses TF-IDF + cosine similarity as a
lightweight fallback. Can be upgraded to
use Sentence Transformers (SBERT) when
available.

Author : Sagar Sen
Project: CivicPulse
"""

import math
import logging

logger = logging.getLogger(__name__)

# ==========================================
# Try to use sklearn for TF-IDF similarity
# ==========================================

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    logger.info(
        "scikit-learn not installed. "
        "Using basic text similarity fallback."
    )


# ==========================================
# Try to use Sentence Transformers (SBERT)
# ==========================================

try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
    HAS_SBERT = True
except ImportError:
    HAS_SBERT = False
    logger.info(
        "sentence-transformers not installed. "
        "Using TF-IDF or basic fallback."
    )


class DuplicateDetectionService:

    # ==========================================
    # Configuration
    # ==========================================

    TEXT_SIMILARITY_THRESHOLD = 0.5
    LOCATION_PROXIMITY_METRES = 100
    MAX_CANDIDATES = 50
    MAX_DUPLICATES = 5

    # Lazy-loaded SBERT model
    _sbert_model = None

    @classmethod
    def _get_sbert_model(cls):
        """Lazy-load SBERT model."""

        if cls._sbert_model is None and HAS_SBERT:
            try:
                cls._sbert_model = SentenceTransformer(
                    "all-MiniLM-L6-v2"
                )
                logger.info("SBERT model loaded successfully.")
            except Exception as error:
                logger.warning(
                    "Failed to load SBERT model: %s. "
                    "Falling back to TF-IDF.",
                    str(error)
                )

        return cls._sbert_model

    # ==========================================
    # Haversine Distance (metres)
    # ==========================================

    @staticmethod
    def haversine_distance(lat1, lon1, lat2, lon2):
        """
        Calculate the great-circle distance
        between two points in metres.
        """

        if any(v is None for v in [lat1, lon1, lat2, lon2]):
            return None

        try:
            lat1 = float(lat1)
            lon1 = float(lon1)
            lat2 = float(lat2)
            lon2 = float(lon2)
        except (TypeError, ValueError):
            return None

        R = 6371000  # Earth radius in metres

        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        d_phi = math.radians(lat2 - lat1)
        d_lambda = math.radians(lon2 - lon1)

        a = (
            math.sin(d_phi / 2) ** 2
            + math.cos(phi1)
            * math.cos(phi2)
            * math.sin(d_lambda / 2) ** 2
        )

        c = 2 * math.atan2(
            math.sqrt(a),
            math.sqrt(1 - a)
        )

        return R * c

    # ==========================================
    # Basic Text Similarity (fallback)
    # ==========================================

    @staticmethod
    def _basic_text_similarity(text1, text2):
        """
        Simple word-overlap similarity (Jaccard).
        Used when sklearn is not available.
        """

        if not text1 or not text2:
            return 0.0

        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        if not words1 or not words2:
            return 0.0

        intersection = words1 & words2
        union = words1 | words2

        return len(intersection) / len(union)

    # ==========================================
    # TF-IDF Similarity
    # ==========================================

    @classmethod
    def _tfidf_similarity(cls, new_text, candidate_texts):
        """
        Compute TF-IDF cosine similarity between
        new_text and each candidate text.
        Returns list of similarity scores.
        """

        if not HAS_SKLEARN or not candidate_texts:
            return [
                cls._basic_text_similarity(new_text, t)
                for t in candidate_texts
            ]

        try:
            all_texts = [new_text] + candidate_texts

            vectorizer = TfidfVectorizer(
                stop_words="english",
                max_features=5000
            )

            tfidf_matrix = vectorizer.fit_transform(all_texts)

            similarities = cosine_similarity(
                tfidf_matrix[0:1],
                tfidf_matrix[1:]
            )[0]

            return similarities.tolist()

        except Exception as error:
            logger.warning(
                "TF-IDF error: %s. Falling back.",
                str(error)
            )
            return [
                cls._basic_text_similarity(new_text, t)
                for t in candidate_texts
            ]

    # ==========================================
    # SBERT Similarity
    # ==========================================

    @classmethod
    def _sbert_similarity(cls, new_text, candidate_texts):
        """
        Compute SBERT cosine similarity.
        Returns list of similarity scores.
        """

        model = cls._get_sbert_model()

        if model is None or not candidate_texts:
            return cls._tfidf_similarity(
                new_text, candidate_texts
            )

        try:
            all_texts = [new_text] + candidate_texts

            embeddings = model.encode(
                all_texts,
                convert_to_numpy=True
            )

            new_emb = embeddings[0:1]
            cand_embs = embeddings[1:]

            # Cosine similarity
            from numpy.linalg import norm

            scores = []
            for emb in cand_embs:
                sim = float(
                    np.dot(new_emb[0], emb)
                    / (norm(new_emb[0]) * norm(emb) + 1e-10)
                )
                scores.append(sim)

            return scores

        except Exception as error:
            logger.warning(
                "SBERT error: %s. Falling back to TF-IDF.",
                str(error)
            )
            return cls._tfidf_similarity(
                new_text, candidate_texts
            )

    # ==========================================
    # Find Potential Duplicates
    # ==========================================

    @classmethod
    def find_duplicates(
        cls,
        title,
        description,
        category_id,
        latitude=None,
        longitude=None,
        exclude_statuses=None
    ):
        """
        Find potential duplicate complaints.

        Returns list of dicts:
        [
            {
                "complaint_id": int,
                "title": str,
                "category_name": str,
                "status": str,
                "location": str,
                "similarity_score": float,
                "distance_metres": float or None,
                "reasons": [str]
            }
        ]
        """

        from database.connection import get_connection

        if exclude_statuses is None:
            exclude_statuses = ["Rejected"]

        connection = None
        cursor = None

        try:
            connection = get_connection()
            if connection is None:
                return []

            cursor = connection.cursor()

            # Build exclusion clause
            exclude_placeholders = ", ".join(
                f":excl_{i}"
                for i in range(len(exclude_statuses))
            )

            params = {
                "category_id": category_id
            }

            for i, status in enumerate(exclude_statuses):
                params[f"excl_{i}"] = status

            sql = f"""
                SELECT
                    C.COMPLAINT_ID,
                    C.TITLE,
                    C.DESCRIPTION,
                    C.CATEGORY_ID,
                    IC.CATEGORY_NAME,
                    C.STATUS,
                    C.LOCATION,
                    C.LATITUDE,
                    C.LONGITUDE
                FROM COMPLAINTS C
                JOIN ISSUE_CATEGORIES IC
                    ON C.CATEGORY_ID = IC.CATEGORY_ID
                WHERE C.STATUS NOT IN ({exclude_placeholders})
                ORDER BY C.CREATED_AT DESC
                FETCH FIRST {cls.MAX_CANDIDATES} ROWS ONLY
            """

            cursor.execute(sql, params)
            candidates = cursor.fetchall()

            if not candidates:
                return []

            # Prepare texts for similarity
            new_text = f"{title} {description}"

            candidate_texts = [
                f"{row[1]} {row[2]}"
                for row in candidates
            ]

            # Compute text similarities
            if HAS_SBERT:
                text_scores = cls._sbert_similarity(
                    new_text, candidate_texts
                )
            else:
                text_scores = cls._tfidf_similarity(
                    new_text, candidate_texts
                )

            # Score each candidate
            duplicates = []

            for i, row in enumerate(candidates):
                cand_id = row[0]
                cand_title = row[1]
                cand_category_id = row[3]
                cand_category_name = row[4]
                cand_status = row[5]
                cand_location = row[6]
                cand_lat = row[7]
                cand_lon = row[8]

                text_sim = text_scores[i]
                reasons = []
                bonus = 0.0

                # Category match bonus
                if cand_category_id == category_id:
                    bonus += 0.1
                    reasons.append("Same category")

                # Location proximity bonus
                distance = cls.haversine_distance(
                    latitude, longitude,
                    cand_lat, cand_lon
                )

                if distance is not None:
                    if distance <= cls.LOCATION_PROXIMITY_METRES:
                        bonus += 0.15
                        reasons.append(
                            f"Within {int(distance)}m"
                        )
                    elif distance <= 500:
                        bonus += 0.05
                        reasons.append(
                            f"Within {int(distance)}m"
                        )

                # Combined score
                combined_score = min(
                    text_sim + bonus, 1.0
                )

                if combined_score >= cls.TEXT_SIMILARITY_THRESHOLD:
                    if text_sim >= 0.3:
                        reasons.insert(
                            0,
                            f"Text similarity: {text_sim:.0%}"
                        )

                    duplicates.append({
                        "complaint_id": cand_id,
                        "title": cand_title,
                        "category_name": cand_category_name,
                        "status": cand_status,
                        "location": cand_location or "Not specified",
                        "similarity_score": round(
                            combined_score, 2
                        ),
                        "distance_metres": (
                            round(distance, 1)
                            if distance is not None
                            else None
                        ),
                        "reasons": reasons
                    })

            # Sort by score, return top N
            duplicates.sort(
                key=lambda x: x["similarity_score"],
                reverse=True
            )

            return duplicates[:cls.MAX_DUPLICATES]

        except Exception as error:
            logger.error(
                "Duplicate detection error: %s",
                str(error)
            )
            return []

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

