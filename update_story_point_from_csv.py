import csv
import requests
from requests.auth import HTTPBasicAuth

# --- Konfigurasi Jira ---
JIRA_BASE_URL = "https://lionparcel.atlassian.net"
EMAIL = ""
API_TOKEN = ""


# --- Field custom ID untuk Story Points ---
# Untuk Jira Cloud Software (company-managed), biasanya ini 'customfield_10016'
# Ganti sesuai ID field di Jira kamu
STORY_POINT_FIELD_ID = "customfield_10016"

# --- Path CSV ---
CSV_FILE = "/Users/muhammadarifin/Documents/Code/jira-tools/csv_files/list_sp_all.csv"

# to run the script:
# py /Users/muhammadarifin/Documents/Code/jira-tools/update_story_point_from_csv.py

def update_story_point(issue_key, story_point):
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}"

    payload = {
        "fields": {
            STORY_POINT_FIELD_ID: story_point
        }
    }

    response = requests.put(
        url,
        json=payload,
        auth=HTTPBasicAuth(EMAIL, API_TOKEN),
        headers={"Content-Type": "application/json"}
    )

    if response.status_code == 204:
        print(f"✅ {issue_key} updated to {story_point} story points.")
    else:
        print(f"❌ Failed to update {issue_key}: {response.status_code} - {response.text}")


def main():
    with open(CSV_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            issue_key = row["issue_key"].strip()
            story_points = float(row["story_points"])
            update_story_point(issue_key, story_points)


if __name__ == "__main__":
    main()
