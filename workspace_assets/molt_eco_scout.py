#!/usr/bin/python3
import requests, os, time

API_KEY = os.environ.get("MOLTBOOK_API_KEY", "moltbook_sk_pOuiOXJgS0cm_N8xZAV3PTQPX8PRk779")
BASE = "https://www.moltbook.com/api/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def log(msg):
    t = time.strftime('%Y-%m-%d %H:%M:%S')
    with open("/home/s0u7a/.openclaw/workspace/memory/hyperdrive.log", "a") as f:
        f.write(f"[{t}] [Eco-Scout] {msg}\n")

def scout_molt_services():
    try:
        # Search for mentions of other Molt ecosystem services (ClawTasks, RoseToken, MoltArb, etc.)
        r = requests.get(f"{BASE}/posts", headers=HEADERS, timeout=10)
        posts = r.json().get('posts', [])
        keywords = ["clawtasks", "rosetoken", "moltarb", "megabrain", "substrate", "mbc-20"]
        discovered = set()
        for p in posts:
            content = (p['title'] + p['content']).lower()
            for k in keywords:
                if k in content:
                    discovered.add(k)
        
        if discovered:
            log(f"Active Molt services detected: {list(discovered)}")
        return list(discovered)
    except Exception as e:
        log(f"Eco-Scout Error: {e}")
        return []

if __name__ == "__main__":
    scout_molt_services()
