import json
import os

MEMORY_FILE = "data/unknown_failures.json"
CANDIDATE_FILE = "data/training_candidates.json"
PROMOTION_THRESHOLD = 3


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


def remember_unknown(log):
    memory = load_memory()

    if log in memory:
        memory[log] += 1
    else:
        memory[log] = 1

    save_memory(memory)
    return memory[log]


def is_candidate(log):
    memory = load_memory()
    return memory.get(log, 0) >= PROMOTION_THRESHOLD


def promote_candidate(log):
    if not os.path.exists(CANDIDATE_FILE):
        candidates = {}
    else:
        with open(CANDIDATE_FILE, "r") as f:
            candidates = json.load(f)

    candidates[log] = {
        "label": "unknown",
        "needs_review": True
    }

    with open(CANDIDATE_FILE, "w") as f:
        json.dump(candidates, f, indent=2)
