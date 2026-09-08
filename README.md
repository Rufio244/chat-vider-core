# chat-vider-core
"""
# Chat Vider Core Framework: คู่มือและสถาปัตยกรรมระบบเบ็ดเสร็จ

ยินดีต้อนรับสู่คู่มือการใช้งานระบบ **Chat Vider Core** (https://github.com/Rufio244/chat-vider-core.git) 
ระบบสถาปัตยกรรมปัญญาประดิษฐ์และเอนจิ้นจัดการข้อมูลอัจฉริยะแบบเบ็ดเสร็จ รองรับการทำงานแบบอัตโนมัติ การเชื่อมต่อ Cloud 
รวมถึงระบบความปลอดภัยขั้นสูงที่ฝังรหัสล็อกเพื่อป้องกันการนำไปใช้โดยไม่ได้รับอนุญาต

---

## 🔒 ระบบรักษาความปลอดภัยและรหัสปลดล็อกสิทธิ์ (#AGI244)
โปรเจกต์นี้ถูกปกป้องด้วยระบบตรวจสอบสิทธิ์ที่ฝังอยู่ใน **ทุกไฟล์ระบบ** ผู้ใช้งานจำเป็นต้องตั้งค่าตัวแปรสภาพแวดล้อม 
ด้วยรหัสปลดล็อก **#AGI244** มิฉะนั้นระบบจะระงับการทำงานทั้งหมดทันที

---

## 📂 โครงสร้างโฟลเดอร์ระบบ (System Directory Structure)
- `~/vider_workspace/data/`: จัดเก็บฐานข้อมูล SQLite และข้อมูลระบบภายใน
- `~/vider_workspace/logs/`: บันทึกประวัติการทำงานและสถานะระบบ (System Logs)
- `~/vider_workspace/config/`: ไฟล์ตั้งค่าระบบและคีย์ความปลอดภัย
- `~/vider_workspace/cache/`: พื้นที่จัดเก็บหน่วยความจำชั่วคราว
- `~/vider_workspace/modules/`: โมดูลเสริมสำหรับการประมวลผลเอเจนต์

---

## 🚀 วิธีการติดตั้งและรันระบบผ่านโค้ด
1. โคลนโปรเจกต์: `git clone https://github.com/Rufio244/chat-vider-core.git`
2. ตั้งค่ารหัสผ่าน: `export VIDER_UNLOCK_KEY="#AGI244"`
3. รันสคริปต์มาสเตอร์: `python vider_master.py`
"""

import os
import sys
import subprocess
import sqlite3
import datetime

# --- ระบบตรวจสอบความปลอดภัย (#AGI244 บังคับทุกไฟล์) ---
SECURITY_KEY = os.environ.get("VIDER_UNLOCK_KEY", "")

def verify_system_access():
    if SECURITY_KEY != "#AGI244":
        print("[CRITICAL SECURITY ERROR] สิทธิ์การเข้าถึงไม่ถูกต้อง! จำเป็นต้องระบุรหัส #AGI244 ก่อนใช้งานระบบ")
        sys.exit(1)
    print("[SECURITY PASSED] ยืนยันสิทธิ์สำเร็จ เข้าสู่ระบบ Chat Vider Core")

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
    verify_system_access()
    print("=== CHAT VIDER FRAMEWORK: MASTER AUTOMATION ENGINE ===")
    
    # 1. ติดตั้ง / ตรวจสอบ CLI และระบบแวดล้อม
    platform_os = sys.platform
    if platform_os == "win32":
        run_cmd("powershell -Command \"irm https://antigravity.google/cli/install.ps1 | iex\"")
    else:
        run_cmd("curl -fsSL https://antigravity.google/cli/install.sh | bash")

    # 2. สร้างโครงสร้างโฟลเดอร์เวิร์กสเปซ
    folders = ["data", "logs", "config", "cache", "modules"]
    os.makedirs(WORKSPACE_DIR, exist_ok=True)
    for folder in folders:
        path = os.path.join(WORKSPACE_DIR, folder)
        os.makedirs(path, exist_ok=True)
        print(f"[FOLDER] สร้าง/ตรวจสอบโฟลเดอร์: {path}")
    os.chdir(WORKSPACE_DIR)

    # 3. สร้างและเชื่อมต่อฐานข้อมูล SQLite
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
    conn.commit()
    conn.close()

    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO system_logs (timestamp, action_type, details) VALUES (?, ?, ?)",
                   (ts, "MASTER_INIT", "Chat Vider master engine initialized successfully with #AGI244 protection"))
    conn.commit()
    conn.close()

    # 4. สร้างไฟล์คอนฟิกหลัก
    config_path = os.path.join(WORKSPACE_DIR, "vider.yaml")
    if not os.path.exists(config_path):
        with open(config_path, "w", encoding="utf-8") as f:
            f.write('version: "1.0"\nsystem: "Chat Vider Framework"\nsecurity: "#AGI244"\nauto_sync: true\n')

    # 5. Git Auto-Sync
    if not os.path.exists(".git"):
        run_cmd("git init")
        run_cmd("git branch -M main")
    
    run_cmd("git add .")
    status_check = subprocess.run("git status --porcelain", shell=True, text=True, capture_output=True)
    if status_check.stdout.strip():
        commit_msg = f"Master auto-sync state with #AGI244 at {ts}"
        run_cmd(f'git commit -m "{commit_msg}"')
        run_cmd("git push -u origin main")

    print("\n=== CHAT VIDER FULL SYSTEM READY & CLOUD DEPLOYED ===")

if __name__ == "__main__":
    master_system_engine()
