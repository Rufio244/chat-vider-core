import os
import requests

# ดึง GitHub Token ที่ตั้งค่าถาวรไว้บน Cloud
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = "your-github-username"  # ใส่ชื่อยูสเซอร์ GitHub ของคุณ

def create_github_repo_automatically(repo_name):
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    payload = {
        "name": repo_name,
        "private": False,
        "description": "Auto-generated project by Chat Vider Enterprise AGI Engine"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 201:
        return response.json().get("html_url")
    return None
