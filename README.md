# Jira Tools

Kumpulan script Python untuk otomasi task-task di Jira, khususnya untuk update Story Points dan insert Worklog secara bulk.

## 📋 Daftar Isi

- [Prerequisites](#prerequisites)
- [Konfigurasi](#konfigurasi)
- [Script yang Tersedia](#script-yang-tersedia)
  - [1. Update Story Point dari CSV](#1-update-story-point-dari-csv)
  - [2. Insert Worklog](#2-insert-worklog)

---

## Prerequisites

Sebelum menggunakan script ini, pastikan sudah terinstall:

- **Python 3.x**
- **Library yang dibutuhkan:**
  ```bash
  pip install requests jira
  ```

## Konfigurasi

### Mendapatkan Jira API Token

1. Login ke Jira (https://lionparcel.atlassian.net)
2. Buka **Account Settings** → **Security** → **API Tokens**
3. Klik **Create API Token**
4. Copy token yang dihasilkan

### Setup Credentials

Setiap script memerlukan konfigurasi `JIRA_BASE_URL`, `USERNAME`, dan `API_TOKEN`.

1. Duplikat file `.env.example` menjadi `.env` di root direktori project:
   ```bash
   cp .env.example .env
   ```
2. Buka file `.env` dan isi dengan detail credential Jira Anda:
   ```env
   # Konfigurasi Jira
   JIRA_BASE_URL="https://lionparcel.atlassian.net"
   USERNAME="email-kamu@lionparcel.com"
   API_TOKEN="api-token-kamu"
   ```

---

## Script yang Tersedia

### 1. Update Story Point dari CSV

**File:** `update_story_point_from_csv.py`

Script ini digunakan untuk update Story Points secara bulk dari file CSV.

#### 📝 Cara Penggunaan

1. **Siapkan file CSV** di folder `csv_files/` dengan format:
   ```csv
   issue_key,story_points
   GQA-5127,0.5
   GQA-5128,1.0
   GQA-5129,2.0
   ```

2. **Setup Credentials**: Pastikan file `.env` sudah terisi dengan benar.
3. **Atur Path CSV** di dalam script `update_story_point_from_csv.py` (jika berbeda):
   ```python
   CSV_FILE = "/path/to/csv_files/list_sp_all.csv"
   ```

4. **Jalankan script:**
   ```bash
   python update_story_point_from_csv.py
   ```

#### ⚙️ Konfigurasi Custom Field

Jika custom field Story Points berbeda, ubah nilai:
```python
STORY_POINT_FIELD_ID = "customfield_10016"  # Default untuk Jira Cloud
```

#### ✅ Output

```
✅ GQA-5127 updated to 0.5 story points.
✅ GQA-5128 updated to 1.0 story points.
❌ Failed to update GQA-5129: 404 - Issue not found
```

---

### 2. Insert Worklog

**File:** `insert_worklog.py`

Script ini digunakan untuk menambahkan worklog secara bulk ke multiple Jira tickets sekaligus.

#### 📝 Cara Penggunaan

1. **Setup Credentials**: Pastikan file `.env` sudah terisi dengan benar.

2. **Atur input ticket dan worklog** di dalam script `insert_worklog.py`:
   ```python
   ticket_input = "[GQA-4379][GQA-4380][GQA-4381]"
   time_spent = "5m"
   comment = "[REVIEW PR]"
   ```

3. **Jalankan script:**
   ```bash
   python insert_worklog.py
   ```

#### 📌 Format Input

**Metode 1: String dengan bracket (Otomatis)**
```python
ticket_input = "[GQA-4379][GQA-4380][GQA-4381][GQA-4382]"
time_spent = "5m"
comment = "[REVIEW PR]"
```

**Metode 2: Manual list (Commented)**
```python
worklogs = [
    {"issue": "GQA-4175", "timeSpent": "10m", "comment": "[REVIEW PR]"},
    {"issue": "GQA-4176", "timeSpent": "10m", "comment": "[REVIEW PR]"},
]
```

#### ⏱️ Format Time Spent

- `5m` = 5 menit
- `1h` = 1 jam
- `1h 30m` = 1 jam 30 menit
- `1d` = 1 hari (8 jam)

#### ✅ Output

```
Worklogs yang akan ditambahkan:
{'issue': 'GQA-4379', 'timeSpent': '5m', 'comment': '[REVIEW PR]'}
{'issue': 'GQA-4380', 'timeSpent': '5m', 'comment': '[REVIEW PR]'}
✔ Worklog berhasil ditambahkan di GQA-4379 dengan ID 12345
✔ Worklog berhasil ditambahkan di GQA-4380 dengan ID 12346
```

---

## 📁 Struktur Folder

```
jira-tools/
├── README.md
├── .gitignore
├── .env.example
├── .env                  # File credentials Anda (diabaikan oleh git)
├── update_story_point_from_csv.py
├── insert_worklog.py
└── csv_files/
    ├── list_sp.csv
    ├── list_sp_alLsample.csv
    └── list_sp_all.csv
```

---

## 🔒 Security Notes

- **Jangan commit API Token** ke repository
- Gunakan environment variables atau `.env` file untuk credentials
- Pastikan file CSV tidak berisi data sensitif sebelum di-commit

---

## 🐛 Troubleshooting

### Error: "Failed to update issue"
- Pastikan API Token valid
- Cek apakah issue key benar
- Pastikan user memiliki permission untuk edit issue

### Error: "Custom field not found"
- Cek `STORY_POINT_FIELD_ID` sesuai dengan Jira instance kamu
- Bisa dicek via Jira REST API: `/rest/api/3/field`

### Error: "Module not found"
- Install dependencies: `pip install requests jira`

---

## 📝 License

MIT License - Feel free to use and modify

---

## 👤 Author

Muhammad Arifin