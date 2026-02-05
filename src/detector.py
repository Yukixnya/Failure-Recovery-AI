import joblib
import numpy as np
from src.log_parser import parse_log
from src.vectorizer import vectorize_log

model = joblib.load("models/log_cluster.pkl")

DISTANCE_THRESHOLD = 1.2

def detect_failure(log):
    clean_log = parse_log(log)
    vec = vectorize_log(clean_log)

    cluster = model.predict(vec)[0]
    center = model.cluster_centers_[cluster]

    distance = np.linalg.norm(vec.toarray() - center)
    confidence = max(0, round(1 - distance, 2))

    return {
        "cluster": int(cluster),
        "confidence": confidence,
        "unknown": distance > DISTANCE_THRESHOLD
    }
