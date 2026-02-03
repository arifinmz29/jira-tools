from jira import JIRA
import re

# Konfigurasi Jira
JIRA_BASE_URL = "https://lionparcel.atlassian.net"
USERNAME = ""
API_TOKEN = ""

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
