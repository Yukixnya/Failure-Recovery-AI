import subprocess
import platform

def collect_system_logs():
    system = platform.system().lower()
    if system == "windows":
        command = [
            "powershell",
            "-Command",
            "Get-EventLog -LogName System -Newest 10 | Select-Object -ExpandProperty Message"
        ]

        result = subprocess.run(command, capture_output=True, text=True)
        logs = [log.strip() for log in result.stdout.split("\n") if log.strip()]

        return list(dict.fromkeys(logs))

    return [
        "ERROR cache eviction failure in recommendation service",
        "ERROR CPU usage spike in order service",
        "WARNING retry limit exceeded in auth service"
    ]
