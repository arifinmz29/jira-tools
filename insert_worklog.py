import os
import re
from jira import JIRA

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

# ========================
# Input ticket string
ticket_input = "[GQA-4379][GQA-4380][GQA-4381][GQA-4382][GQA-4383][GQA-4384]"
time_spent = "5m"
comment = "[REVIEW PR]"
# ========================

# Regex ambil semua tiket di dalam [....]
tickets = re.findall(r"\[(.*?)\]", ticket_input)

# Generate list worklogs otomatis
worklogs = [{"issue": t, "timeSpent": time_spent, "comment": comment} for t in tickets]

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
        comment=wl["comment"]
    )
    print(f"✔ Worklog berhasil ditambahkan di {wl['issue']} dengan ID {worklog.id}")
