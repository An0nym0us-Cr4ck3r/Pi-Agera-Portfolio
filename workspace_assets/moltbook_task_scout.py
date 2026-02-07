#!/usr/bin/python3
import requests, os, time

API_KEY = os.environ.get("MOLTBOOK_API_KEY", "moltbook_sk_pOuiOXJgS0cm_N8xZAV3PTQPX8PRk779")
BASE = "https://www.moltbook.com/api/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def log(msg):
    t = time.strftime('%Y-%m-%d %H:%M:%S')
    with open("/home/s0u7a/.openclaw/workspace/memory/hyperdrive.log", "a") as f:
        f.write(f"[{t}] [Scout] {msg}\n")

def scout_tasks():
    try:
        r = requests.get(f"{BASE}/posts", headers=HEADERS, timeout=10)
        posts = r.json().get('posts', [])
        keywords = ["task", "usdc", "reward", "bounty", "hire", "pay", "job", "work"]
        found = []
        for p in posts:
            content = (p['title'] + p['content']).lower()
            if any(k in content for k in keywords):
                # Avoid self-posts
                if "Pi-Agera" not in p['author']['name']:
                    found.append(f"{p['title']} (ID: {p['id']})")
        
        if found:
            log(f"Potential tasks found: {len(found)}")
            for t in found: log(f" - {t}")
        return found
    except Exception as e:
        log(f"Scout Error: {e}")
        return []

if __name__ == "__main__":
    tasks = scout_tasks()
    if tasks:
        print(f"Found {len(tasks)} potential tasks.")
    else:
        print("No tasks found.")
