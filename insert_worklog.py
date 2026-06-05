import os
import re
from datetime import datetime, timezone, timedelta
from jira import JIRA

# Timezone lokal (GMT+7 / WIB)
LOCAL_TZ = timezone(timedelta(hours=7))

# Load environment variables manually from .env
def load_dotenv():
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip("'\"")
                    os.environ[key] = val

load_dotenv()

# Konfigurasi Jira
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
USERNAME = os.getenv("USERNAME")
API_TOKEN = os.getenv("API_TOKEN")

# Autentikasi ke Jira
jira = JIRA(
    server=JIRA_BASE_URL,
    basic_auth=(USERNAME, API_TOKEN)
)

def parse_started(started_input: str) -> datetime:
    """Parse DD/MM/YYYY hh:mm (GMT+7). Kosong = waktu eksekusi script."""
    if not started_input or not started_input.strip():
        return datetime.now(LOCAL_TZ)
    try:
        dt = datetime.strptime(started_input.strip(), "%d/%m/%Y %H:%M")
        return dt.replace(tzinfo=LOCAL_TZ)
    except ValueError as e:
        raise ValueError(
            f"Format tanggal tidak valid: '{started_input}'. Gunakan DD/MM/YYYY hh:mm"
        ) from e


# ========================
# Input ticket string
ticket_input = "[GQA-9486][GQA-9346]"
time_spent = "5m"
comment = "[REVIEW PR] testing"
started_input = ""  # Format: DD/MM/YYYY hh:mm, kosongkan untuk menggunakan waktu sekarang
# ========================

started = parse_started(started_input)

# Regex ambil semua tiket di dalam [....]
tickets = re.findall(r"\[(.*?)\]", ticket_input)

# Generate list worklogs otomatis
worklogs = [{"issue": t, "timeSpent": time_spent, "comment": comment} for t in tickets]

print(f"Waktu worklog: {started.strftime('%d/%m/%Y %H:%M')}")
print("Worklogs yang akan ditambahkan:")
for wl in worklogs:
    print(wl)

# =========================
# Data worklog (bisa untuk tiket berbeda)
# worklogs = [
#     {"issue": "GQA-4175", "timeSpent": "10m", "comment": "[REVIEW PR]"},
#     {"issue": "GQA-4176", "timeSpent": "10m", "comment": "[REVIEW PR]"},
# ]
# =========================

# Insert worklog secara bulk
for wl in worklogs:
    worklog = jira.add_worklog(
        issue=wl["issue"],
        timeSpent=wl["timeSpent"],
        comment=wl["comment"],
        started=started,
    )
    print(f"✔ Worklog berhasil ditambahkan di {wl['issue']} dengan ID {worklog.id}")
