import os
import sys
import subprocess
import sqlite3
import datetime

WORKSPACE_DIR = os.path.expanduser("~/vider_workspace")
DB_PATH = os.path.join(WORKSPACE_DIR, "data", "vider_core.db")

def run_cmd(command):
    print(f"[CMD] {command}")
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"[WARNING] {result.stderr.strip()}")
        return False
    print(result.stdout.strip())
    return True

def master_system_engine():
    print("=== CHAT VIDER FRAMEWORK: MASTER AUTOMATION ENGINE ===")
    
    # 1. ติดตั้ง / ตรวจสอบ CLI และระบบแวดล้อม
    platform_os = sys.platform
    if platform_os == "win32":
        print("[INFO] กำลังติดตั้ง Antigravity CLI บน Windows...")
        run_cmd("powershell -Command \"irm https://antigravity.google/cli/install.ps1 | iex\"")
    else:
        print("[INFO] กำลังติดตั้ง Antigravity CLI บน Unix/macOS...")
        run_cmd("curl -fsSL https://antigravity.google/cli/install.sh | bash")

    # 2. สร้างโครงสร้างโฟลเดอร์เวิร์กสเปซ
    folders = ["data", "logs", "config", "cache", "modules"]
    os.makedirs(WORKSPACE_DIR, exist_ok=True)
    for folder in folders:
        path = os.path.join(WORKSPACE_DIR, folder)
        os.makedirs(path, exist_ok=True)
        print(f"[FOLDER] สร้าง/ตรวจสอบโฟลเดอร์: {path}")
    os.chdir(WORKSPACE_DIR)

    # 3. สร้างและเชื่อมต่อฐานข้อมูล SQLite พร้อมตาราง Log
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            action_type TEXT,
            details TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_metadata (
            key TEXT PRIMARY KEY,
            value TEXT,
            updated_at TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print(f"[DATABASE] สร้างฐานข้อมูล SQLite สำเร็จที่: {DB_PATH}")

    # บันทึก Log เริ่มต้นระบบ
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO system_logs (timestamp, action_type, details) VALUES (?, ?, ?)",
                   (ts, "MASTER_INIT", "Chat Vider master engine initialized successfully"))
    conn.commit()
    conn.close()

    # 4. สร้างไฟล์คอนฟิกหลัก vider.yaml
    config_path = os.path.join(WORKSPACE_DIR, "vider.yaml")
    if not os.path.exists(config_path):
        with open(config_path, "w", encoding="utf-8") as f:
            f.write('version: "1.0"\nsystem: "Chat Vider Framework"\nauto_sync: true\n')
        print("[CONFIG] สร้างไฟล์ vider.yaml เรียบร้อย")

    # 5. Git Auto-Sync, Commit และ Cloud Deployment
    if not os.path.exists(".git"):
        run_cmd("git init")
        run_cmd("git branch -M main")
    
    run_cmd("git add .")
    status_check = subprocess.run("git status --porcelain", shell=True, text=True, capture_output=True)
    if status_check.stdout.strip():
        commit_msg = f"Master auto-sync state at {ts}"
        run_cmd(f'git commit -m "{commit_msg}"')
        run_cmd("git push -u origin main")
    else:
        print("[GIT] ไม่พบการเปลี่ยนแปลงไฟล์ใหม่ ระบบอัปเดตเป็นปัจจุบันแล้ว")

    print("\n=== CHAT VIDER FULL SYSTEM READY & CLOUD DEPLOYED ===")

if __name__ == "__main__":
    master_system_engine()
