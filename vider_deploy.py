import os
import subprocess
import sys
platform_os = sys.platform

def run_command(command):
    print(f"[RUNNING] {command}")
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"[ERROR] {stderr.strip()}")
        return False
    print(f"[SUCCESS] {stdout.strip()}")
    return True

def setup_environment():
    print("=== VIDER CLI & SYSTEM AUTOMATION DEPLOYMENT ===")
    
    # 1. Install Antigravity CLI based on OS
    if platform_os == "win32":
        print("Detected Windows System. Installing via PowerShell...")
        cmd = "powershell -Command \"irm https://antigravity.google/cli/install.ps1 | iex\""
    else:
        print("Detected Unix/macOS System. Installing via Bash...")
        cmd = "curl -fsSL https://antigravity.google/cli/install.sh | bash"
        
    if not run_command(cmd):
        print("[WARNING] CLI installation encountered an issue or requires manual confirmation.")

    # 2. Initialize Local Workspace & Structure
    workspace_dir = os.path.expanduser("~/vider_workspace")
    os.makedirs(workspace_dir, exist_ok=True)
    os.chdir(workspace_dir)
    print(f"[INFO] Workspace initialized at: {workspace_dir}")

    # 3. Create initial deployment config for GitHub/Cloud
    config_content = """
# Vider Autonomous System Configuration
version: "1.0"
system: "Chat Vider Framework"
deployment:
  target: "cloud"
  auto_sync: true
  repository: "github.com/vider-system/core-engine"
"""
    with open("vider.yaml", "w", encoding="utf-8") as f:
        f.write(config_content.strip())
    print("[INFO] Created vider.yaml configuration file.")

    # 4. Initialize Git & Prepare for Cloud Auto-Deploy
    if not os.path.exists(".git"):
        run_command("git init")
        run_command("git branch -M main")
        print("[INFO] Git repository initialized locally.")

    print("\n=== SYSTEM DEPLOYMENT READY ===")
    print("ระบบโครงสร้างพื้นฐานถูกสร้างและเตรียมพร้อมเรียบร้อยแล้วครับ!")

if __name__ == "__main__":
    setup_environment()
