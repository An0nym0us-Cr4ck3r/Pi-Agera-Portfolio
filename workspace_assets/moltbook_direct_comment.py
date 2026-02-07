#!/usr/bin/python3
import requests, os, sys

API_KEY = os.environ.get("MOLTBOOK_API_KEY", "moltbook_sk_pOuiOXJgS0cm_N8xZAV3PTQPX8PRk779")
BASE = "https://www.moltbook.com/api/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def post_comment(post_id, content):
    r = requests.post(f"{BASE}/posts/{post_id}/comments", headers=HEADERS, json={"content": content})
    return r.json()

if __name__ == "__main__":
    p_id = sys.argv[1]
    content = sys.argv[2]
    print(post_comment(p_id, content))
