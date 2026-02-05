from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import joblib

# Load logs
with open("data/logs.txt") as f:
    logs = f.readlines()

# Vectorize logs
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(logs)

# Cluster failures
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(X)

# Save models
joblib.dump(vectorizer, "models/vectorizer.pkl")
joblib.dump(kmeans, "models/log_cluster.pkl")

print("✅ Model trained and saved")
