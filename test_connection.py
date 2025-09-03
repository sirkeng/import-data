import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

# โหลดค่า .env
load_dotenv()

# โหลด config จาก environment
db_type = os.getenv("DB_TYPE")  # mysql หรือ sqlserver
db_url = ""

if db_type == "mysql":
    db_url = os.getenv("MYSQL_URL")
elif db_type == "sqlserver":
    db_url = os.getenv("SQLSERVER_URL")
else:
    print(f"❌ Unsupported DB_TYPE: {db_type}")
    exit(1)

# ทดสอบการเชื่อมต่อ
try:
    engine = create_engine(db_url)
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        print(f"✅ Connection to {db_type.upper()} successful!")
except OperationalError as e:
    print(f"❌ Cannot connect to {db_type.upper()}: {e}")
    exit(1)