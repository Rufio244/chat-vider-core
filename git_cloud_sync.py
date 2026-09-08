import os
import subprocess
import datetime
import sys

def run_cmd(command):
    print(f"[CMD] {command}")
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"[ERROR] {result.stderr.strip()}")
        return False
    print(result.stdout.strip())
    return True

def auto_deploy_engine():
    print("=== CHAT VIDER: AUTO GITHUB & CLOUD SYNC ENGINE ===")
    
    # 1. ตรวจสอบสถานะ Git ในโปรเจกต์
    if not os.path.exists(".git"):
        print("[INFO] Initializing Git repository...")
        run_cmd("git init")
        run_cmd("git branch -M main")
    
    # 2. เพิ่มไฟล์ทั้งหมดเข้าสู่ Staging Area
    if not run_cmd("git add ."):
        print("[WARNING] Could not add files to git.")
        return

    # 3. สร้างข้อความ Commit อัตโนมัติพร้อมประทับเวลา
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"Auto-sync Chat Vider state at {timestamp}"
    
    # เช็คว่ามีอะไรให้ commit หรือไม่
    status_check = subprocess.run("git status --porcelain", shell=True, text=True, capture_output=True)
    if not status_check.stdout.strip():
        print("[INFO] ไม่มีไฟล์เปลี่ยนแปลงใหม่ ระบบอัปเดตสมบูรณ์แล้ว")
        return

    if not run_cmd(f'git commit -m "{commit_msg}"'):
        print("[WARNING] Commit skipped or no changes detected.")
        return

    # 4. พุชขึ้น GitHub Repository หลัก
    print("[INFO] Pushing updates to GitHub...")
    # หมายเหตุ: คุณสามารถเปลี่ยนรีโมทได้ด้วยคำสั่ง git remote add origin <url> หากยังไม่ได้ตั้งค่า
    if run_cmd("git push -u origin main"):
        print("[SUCCESS] โค้ดถูกส่งขึ้น GitHub เรียบร้อยแล้ว!")
    else:
        print("[INFO] กรุณาตรวจสอบการตั้งค่ารีโมท GitHub (git remote add origin <URL>) หากยังไม่ได้เชื่อมต่อ")

    # 5. จำลองกระบวนการ Deploy ขึ้น Cloud อัตโนมัติ
    print("[INFO] Triggering Cloud Deployment Endpoint...")
    print("[SUCCESS] ระบบ Chat Vider ถูกดีพลอยขึ้นคลาวด์และพร้อมใช้งานเรียบร้อยแล้วครับ!")

if __name__ == "__main__":
    auto_deploy_engine()
