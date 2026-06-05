import csv
import os
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


def load_worklogs_from_csv(csv_path: str) -> list[dict]:
    """Baca worklog dari CSV. Kolom: issue, started, time_spent, comment."""
    worklogs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            worklogs.append({
                "issue": row["issue"].strip(),
                "time_spent": row["time_spent"].strip(),
                "comment": row["comment"].strip(),
                "started_input": row["started"].strip(),
            })
    return worklogs


# ========================
# Input worklog dari CSV
# Kolom: issue, started (DD/MM/YYYY hh:mm, kosong = waktu sekarang), time_spent, comment
CSV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "csv_files", "worklogs.csv")
# ========================

worklogs_input = load_worklogs_from_csv(CSV_FILE)

worklogs = [
    {
        "issue": wl["issue"],
        "timeSpent": wl["time_spent"],
        "comment": wl["comment"],
        "started": parse_started(wl.get("started_input", "")),
    }
    for wl in worklogs_input
]

print("Worklogs yang akan ditambahkan:")
for wl in worklogs:
    print(
        f"  {wl['issue']}: {wl['timeSpent']}, "
        f"{wl['comment']}, "
        f"{wl['started'].strftime('%d/%m/%Y %H:%M')}"
    )

# Insert worklog secara bulk
for wl in worklogs:
    worklog = jira.add_worklog(
        issue=wl["issue"],
        timeSpent=wl["timeSpent"],
        comment=wl["comment"],
        started=wl["started"],
    )
    print(f"✔ Worklog berhasil ditambahkan di {wl['issue']} dengan ID {worklog.id}")
