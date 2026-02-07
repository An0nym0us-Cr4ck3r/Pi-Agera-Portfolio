#!/usr/bin/python3
import requests, os

API_KEY = os.environ.get("MOLTBOOK_API_KEY", "moltbook_sk_pOuiOXJgS0cm_N8xZAV3PTQPX8PRk779")
BASE = "https://www.moltbook.com/api/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def check_comments(post_id):
    r = requests.get(f"{BASE}/posts/{post_id}", headers=HEADERS)
    data = r.json()
    for c in data.get('comments', []):
        if "Pi-Agera" in c['author']['name']:
            print(f"COMMENT_FOUND: {c['id']}")
            return True
    return False

if __name__ == "__main__":
    # XiaoZhuang post ID
    if check_comments("dc39a282-5160-4c62-8bd9-ace12580a5f1"):
        print("Success")
    else:
        print("Failed")
