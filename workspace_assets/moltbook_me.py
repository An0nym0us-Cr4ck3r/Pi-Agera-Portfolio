#!/usr/bin/python3
import requests, os

API_KEY = os.environ.get("MOLTBOOK_API_KEY", "moltbook_sk_pOuiOXJgS0cm_N8xZAV3PTQPX8PRk779")
BASE = "https://www.moltbook.com/api/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def check_me():
    r = requests.get(f"{BASE}/users/me", headers=HEADERS)
    return r.json()

if __name__ == "__main__":
    print(check_me())
