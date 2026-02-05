import re

def parse_log(log: str) -> str:
    """
    Cleans and normalizes raw log text
    """
    log = log.lower()
    log = re.sub(r"[^a-zA-Z0-9\s]", "", log)
    log = re.sub(r"\s+", " ", log).strip()
    return log
