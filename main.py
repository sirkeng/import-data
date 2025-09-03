import os
import pandas as pd
import pymysql  # ✅ สำคัญ
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from tqdm import tqdm
import logging
from dotenv import load_dotenv
load_dotenv()

# --- CONFIG ---
FOLDER_PATH = os.getenv('FOLDER_PATH')
MYSQL_URL = os.getenv('MYSQL_URL')
LOG_FILE = os.getenv('LOG_FILE')

# --- LOGGING ---
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

# --- CONNECT TO MYSQL ---
try:
    engine = create_engine(MYSQL_URL)
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        print("✅ Successfully connected to MySQL")
except OperationalError as e:
    print(f"❌ Cannot connect to MySQL: {e}")
    logging.error(f"Cannot connect to MySQL: {e}")
    exit(1)

# --- LOOP IMPORT FILES ---
for filename in tqdm(os.listdir(FOLDER_PATH)):
    if not filename.endswith('.txt'):
        continue

    filepath = os.path.join(FOLDER_PATH, filename)
    print(f'📥 Importing: {filename}')

    try:
        df = pd.read_csv(filepath, sep='|', dtype=str, encoding='utf-8', on_bad_lines='skip')
        df.fillna('', inplace=True)
        df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]

        # ป้องกัน column ซ้ำ
        if df.columns.duplicated().any():
            df = df.loc[:, ~df.columns.duplicated()]
        
        # Strip ค่าในแต่ละ cell
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

        table_name = 'TEMP_' + filename.replace('.txt', '').lower()

        # --- CREATE TABLE IF NOT EXISTS ---
        with engine.connect() as conn:
            if not engine.dialect.has_table(conn, table_name):
                columns = [f'`{col}` VARCHAR(255)' for col in df.columns]
                create_sql = f"CREATE TABLE `{table_name}` ({', '.join(columns)})"
                conn.execute(text(create_sql))
                logging.info(f'✅ Created table with VARCHAR only: {table_name}')
            else:
                logging.info(f'ℹ️ Table already exists: {table_name}')

        # --- INSERT DATA ---
        df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
        logging.info(f'✅ Imported: {filename} into table {table_name}')
    
    except Exception as e:
        logging.error(f'❌ Failed to import {filename}: {e}')
        print(f'❌ Error: {filename} - {e}')