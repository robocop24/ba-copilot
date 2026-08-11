import numpy as np


class SemanticSearch:
    
    @staticmethod
    def cosine_similarity(v1, v2):
        v1 = np.asarray(v1)
        v2 = np.asarray(v2)
        if v2.ndim == 1:
            return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        return np.dot(v1, v2.T) / (np.linalg.norm(v1) * np.linalg.norm(v2, axis=1))