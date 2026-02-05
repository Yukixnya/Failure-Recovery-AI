import joblib

_vectorizer = joblib.load("models/vectorizer.pkl")

def vectorize_log(log: str):
    """
    Converts parsed log into numerical vector
    """
    return _vectorizer.transform([log])
