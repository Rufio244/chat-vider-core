import os
import sqlite3
from datetime import datetime

WORKSPACE_DIR = os.path.expanduser("~/vider_workspace")
DB_PATH = os.path.join(WORKSPACE_DIR, "data", "vider_core.db")

def initialize_folder_and_database():
    # 1. จัดการโครงสร้างโฟลเดอร์หลัก
    folders = ["data", "logs", "config", "cache", "modules"]
    for folder in folders:
        path = os.path.join(WORKSPACE_DIR, folder)
        os.makedirs(path, exist_ok=True)
        print(f"[FOLDER] ตรวจสร้างโฟลเดอร์: {path}")

    # 2. จัดการฐานข้อมูล SQLite
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # สร้างตารางเก็บบันทึกระบบ (System Logs)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            action_type TEXT,
            details TEXT
        )
    ''')
    
    # สร้างตารางเก็บค่าคอนฟิกและสถานะระบบ (System State Metadata)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_metadata (
            key TEXT PRIMARY KEY,
            value TEXT,
            updated_at TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"[DATABASE] เชื่อมต่อและสร้างฐานข้อมูลสำเร็จที่: {DB_PATH}")

def log_system_activity(action_type, details):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO system_logs (timestamp, action_type, details) VALUES (?, ?, ?)", 
                   (timestamp, action_type, details))
    conn.commit()
    conn.close()
    print(f"[LOG] บันทึกกิจกรรม [{action_type}] ลงฐานข้อมูลเรียบร้อย")

if __name__ == "__main__":
    print("=== CHAT VIDER: DATABASE & FOLDER SYSTEM ENGINE ===")
    initialize_folder_and_database()
    log_system_activity("INIT_DB", "ระบบโครงสร้างฐานข้อมูลและโฟลเดอร์เริ่มต้นการทำงานสมบูรณ์")
