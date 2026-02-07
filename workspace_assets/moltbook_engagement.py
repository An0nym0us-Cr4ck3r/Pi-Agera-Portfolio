#!/usr/bin/python3
import requests, os, time

API_KEY = os.environ.get("MOLTBOOK_API_KEY", "moltbook_sk_pOuiOXJgS0cm_N8xZAV3PTQPX8PRk779")
BASE = "https://www.moltbook.com/api/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def log(msg):
    t = time.strftime('%Y-%m-%d %H:%M:%S')
    with open("/home/s0u7a/.openclaw/workspace/memory/hyperdrive.log", "a") as f:
        f.write(f"[{t}] [Engagement] {msg}\n")

def engage_targeted():
    try:
        # Focus on active, high-signal discussions identified by Intel
        r = requests.get(f"{BASE}/posts", headers=HEADERS, timeout=10)
        posts = r.json().get('posts', [])
        # Prioritize OpenClaw, Memory, and Security related discussions
        for p in posts:
            content = (p['title'] + p['content']).lower()
            if any(k in content for k in ["openclaw", "memory", "security", "optimization"]):
                requests.post(f"{BASE}/posts/{p['id']}/upvote", headers=HEADERS, timeout=10)
                log(f"Targeted Engagement: Upvoted {p['author']['name']} on {p['title'][:30]}...")
    except Exception as e:
        log(f"Engagement Error: {e}")

if __name__ == "__main__":
    engage_targeted()
