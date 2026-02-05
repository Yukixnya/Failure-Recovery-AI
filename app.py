from flask import Flask, request, jsonify

from src.detector import detect_failure
from src.root_cause import find_root_cause, is_learnable
from src.recovery import recommend_action
from src.log_collector import collect_system_logs
from src.memory import remember_unknown, is_candidate, promote_candidate
from src.root_cause import is_learnable

app = Flask(__name__)

# -------------------------
@app.route("/")
def home():
    return "Failure Recovery AI is running"
# -------------------------

# Analyze single log (API)
@app.route("/analyze", methods=["POST"])
def analyze():
    log = request.json["log"]

    result = detect_failure(log)
    root_cause = find_root_cause(log)

    # UNKNOWN → remember & possibly promote
    if result["unknown"] or root_cause is None:
        count = remember_unknown(log)

        if is_candidate(log) and is_learnable(log):
            promote_candidate(log)
            return jsonify({
                "status": "learning_candidate",
                "occurrences": count,
                "confidence": result["confidence"]
            })

        return jsonify({
            "status": "unknown_failure",
            "occurrences": count,
            "confidence": result["confidence"]
        })

    # BENIGN EVENT
    if root_cause and "benign" in root_cause.lower():
        return jsonify({
            "status": "benign_event",
            "root_cause": root_cause,
            "confidence": result["confidence"]
        })

    # KNOWN FAILURE
    action = recommend_action(root_cause)
    return jsonify({
        "status": "known_failure",
        "failure_cluster": result["cluster"],
        "root_cause": root_cause,
        "recommended_action": action,
        "confidence": result["confidence"]
    })

# Analyze real system logs
@app.route("/analyze-system", methods=["GET"])
def analyze_system():
    logs = collect_system_logs()
    results = []

    for log in logs:
        result = detect_failure(log)
        root_cause = find_root_cause(log)

        # UNKNOWN → remember & maybe promote
        if result["unknown"] or root_cause is None:
            count = remember_unknown(log)

            if is_candidate(log) and is_learnable(log):
                promote_candidate(log)
                results.append({
                    "log": log,
                    "status": "learning_candidate",
                    "occurrences": count,
                    "confidence": result["confidence"]
                })
            else:
                results.append({
                    "log": log,
                    "status": "unknown_failure",
                    "occurrences": count,
                    "confidence": result["confidence"]
                })
            continue

        # BENIGN EVENT
        if root_cause and "benign" in root_cause.lower():
            results.append({
                "log": log,
                "status": "benign_event",
                "root_cause": root_cause,
                "confidence": result["confidence"]
            })
            continue

        # KNOWN FAILURE
        action = recommend_action(root_cause)
        results.append({
            "log": log,
            "status": "known_failure",
            "root_cause": root_cause,
            "recommended_action": action,
            "confidence": result["confidence"]
        })

    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)