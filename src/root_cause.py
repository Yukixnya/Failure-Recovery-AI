def find_root_cause(log):
    log = log.lower()

    # Application-level (existing)
    if "db" in log and "timeout" in log:
        return "Database connection pool exhausted"
    if "memory" in log:
        return "Memory leak detected"
    if "cpu" in log:
        return "CPU overload"

    # OS / Infra awareness (NEW)
    if "dcom" in log and "10016" in log:
        return "Windows DCOM permission noise (benign)"
    if "tpm" in log:
        return "Hardware security module (TPM) issue"
    if "ntfs" in log or "harddiskvolume" in log:
        return "Filesystem / disk metadata issue"
    if "secure trustlet" in log:
        return "Windows security sandbox event"

    return None

def is_learnable(log):
    log = log.lower()

    non_learnable_keywords = [
        "windows",
        "dcom",
        "ntfs",
        "tpm",
        "secure",
        "configuration-change-monitor",
        "event id"
    ]

    return not any(k in log for k in non_learnable_keywords)
