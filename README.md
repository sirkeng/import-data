# 📦 Import Data to MySQL from TXT (.csv-like) Files

This project is a Python script to **import data from TXT files (pipe-delimited)** into **MySQL tables**, automatically creating tables if they don't exist.

---

## 📁 Project Structure

import-data/

├── main.py # Script to read TXT files and import into MySQL

├── test_connection.py # Script to test DB connection (MySQL or SQL Server)

├── .env # Configuration file (env vars for connection)

├── requirements.txt # Python dependencies

├── import_log-\*.txt # Auto-generated logs from imports

├── txt_data/ # Folder containing .txt (pipe-separated) files

└── venv/ # (Optional) Virtual environment

---

## ⚙️ Setup & Requirements

### 📦 Install Dependencies

````bash
pip install -r requirements.txt


⸻

🧪 Test DB Connection

Run:

python test_connection.py

Expected output:

✅ Connection to MYSQL successful!

If connection fails, you’ll see:

❌ Cannot connect to MYSQL: ...


⸻

🚀 Run the Import Script

python main.py

It will:
	•	Load all .txt files in txt_data/
	•	Clean and transform data
	•	Auto-create MySQL tables
	•	Insert rows
	•	Log success/failure in import_log-01.txt

⸻

🗃️ Table Naming Convention

Tables will be created as:

TEMP_<filename>.txt → lowercase
Example: CUSTOMER.txt → TEMP_customer


⸻

📄 .env File Format

# General Config
FOLDER_PATH=./txt_data
LOG_FILE=import_log.txt

# DB Config
DB_TYPE=mysql
MYSQL_URL=mysql+pymysql://username:password@host:port/dbname

# Optional: For SQL Server
# SQLSERVER_URL=mssql+pyodbc://username:password@host:port/dbname?driver=ODBC+Driver+17+for+SQL+Server


⸻

📝 Git Commit Message Suggestion

When adding new helper/test files and documentation:

git commit -m 'chore: add test_connection script and project README with setup guide'

✅ Tip: Use commit prefixes like feat:, fix:, chore:, docs:, refactor:, etc.
(Optionally follow Conventional Commits)

⸻

📌 Notes
	•	Assumes all .txt files are | pipe-delimited.
	•	All columns created as VARCHAR(255) for simplicity.
	•	You can customize table schema inference or validations later.

⸻

🤝 Contributions

Feel free to fork and improve. PRs welcome.

---

หากพร้อมแล้วลองรันคำสั่งนี้เพื่อเช็กว่าติดตั้งครบหรือยัง:

```bash
pip install -r requirements.txt
````
