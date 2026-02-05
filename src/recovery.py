def recommend_action(root_cause):
    actions = {
        "Database connection pool exhausted": "Restart DB service & increase pool size",
        "Memory leak detected": "Restart service & monitor memory",
        "CPU overload": "Scale service horizontally"
    }

    return actions.get(root_cause, "Escalate to engineer")
