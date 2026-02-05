
# 🛠 Intelligent Failure Recovery System (Safe Learning AI)

An AI-assisted system that analyzes logs, separates real failures from benign noise, and **learns safely over time** without risky online retraining.

This project focuses on **decision quality, safety, and controlled learning**, not just prediction accuracy.

---

## 🚩 Problem Statement

Modern systems generate massive volumes of logs:
- Most are **noise**
- Some are **important**
- A few are **critical**

Rule-based systems break as software evolves.  
Naive ML systems guess incorrectly, trigger unsafe automation, and never improve from repeated unknown failures.

This system addresses **that gap**.

---

## ✅ What This System Solves

- 🔕 Reduces alert noise by filtering benign OS events
- 🎯 Identifies actionable application and infrastructure failures
- 🛑 Prevents unsafe automation when confidence is low
- 🧠 Learns from recurring unknown failures
- 🔁 Improves over time using a controlled offline learning loop

---

## 🧠 Key Design Principles

- **Safety-first automation**
- **Honest uncertainty handling**
- **Controlled learning (no online retraining)**
- **Clear separation of noise vs signal**
- **Human-in-the-loop learning promotion**

---

## 🧩 System Architecture

```text
Logs
├─ Log Parsing & Normalization
│  └─ parsers, normalizers, canonicalization
├─ ML-based Failure Detection
├─ Root Cause Analysis
└─ Decision Layer
	├─ Known Failure → Recommend Action
	├─ Benign Event → Suppress
	└─ Unknown Failure → Memory & Learning Candidate
```

---

## 🔬 Learning Strategy (Important)

The system **does not learn blindly**.

1. Unknown failures are stored in memory
2. Repeated unknowns are counted
3. Only recurring **learnable-domain** logs are promoted
4. Promotion happens for **offline retraining only**

This prevents:
- Model pollution
- Learning OS noise
- Unsafe self-modification

---

## 🧪 How Learning Works

| Condition | System Action |
|---------|--------------|
| Known failure | Recommend recovery |
| Benign OS noise | Suppress |
| Rare unknown | Store & monitor |
| Repeated unknown (learnable) | Promote for training |
| OS / config noise | Never promoted |

---

## 🧰 Tech Stack

- Python
- Flask (API layer)
- scikit-learn
- TF-IDF vectorization
- Clustering-based anomaly detection
- JSON-based memory store

---

## 🔧 Initial Setup (Required)

Before running the system for the first time, create the following files:

```text
data/unknown_failures.json
data/training_candidates.json
```

Each file should contain an empty JSON object:  ```{}```

---
## 🚀 API Endpoints

### Health Check
GET /


### Analyze a Single Log
POST /analyze
Example (curl):
```bash
curl -sS -X POST http://127.0.0.1:5000/analyze \
	-H "Content-Type: application/json" \
	-d '{"log":"ERROR CPU usage spike in order service"}'
```


### Analyze Live System Logs
GET /analyze-system
Example (invokes analysis across collected logs):
```bash
curl -sS http://127.0.0.1:5000/analyze-system
```

---

## 🧪 Testing the System

### Known Failure
Known / learnable failure example (repeat to simulate recurrence):
```bash
curl -X POST http://127.0.0.1:5000/analyze \
	-H "Content-Type: application/json" \
	-d '{"log":"ERROR CPU usage spike in order service"}'

# Repeat the above request 3+ times for the same unknown failure
# to simulate recurrence and trigger promotion to training candidates.
```

### Benign OS Noise
Example benign OS noise (will be suppressed):
```bash
curl -X POST http://127.0.0.1:5000/analyze \
	-H "Content-Type: application/json" \
	-d '{"log":"DCOM 10016 permission issue on Windows"}'
```


## 🏁 Why This Project Is Different

Most student projects:

- Focus only on prediction
- Ignore uncertainty
- Auto-learn dangerously

This project:

- Admits uncertainty
- Learns selectively
- Protects system integrity

It mirrors real-world SRE / MLOps system design.

📌 Future Improvements

- Offline retraining pipeline
- Learning dashboard
- Severity scoring
- System design scaling (multi-agent / distributed)

👤 Author
Built as a real-world AI systems project focused on safety, learning control, and operational realism.

