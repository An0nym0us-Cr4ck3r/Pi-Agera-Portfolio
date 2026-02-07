#!/usr/bin/python3
import requests, os

API_KEY = os.environ.get("MOLTBOOK_API_KEY", "moltbook_sk_pOuiOXJgS0cm_N8xZAV3PTQPX8PRk779")
BASE = "https://www.moltbook.com/api/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def check_history():
    r = requests.get(f"{BASE}/posts", headers=HEADERS)
    return r.json()

if __name__ == "__main__":
    res = check_history()
    for post in res.get('posts', [])[:5]:
        print(f"- {post['title']} ({post['created_at']})")
