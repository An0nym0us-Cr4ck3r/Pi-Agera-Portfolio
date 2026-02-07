#!/usr/bin/python3
import requests, os

API_KEY = os.environ.get("MOLTBOOK_API_KEY", "moltbook_sk_pOuiOXJgS0cm_N8xZAV3PTQPX8PRk779")
BASE = "https://www.moltbook.com/api/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def check_replies():
    # Since there's no 'notifications' endpoint, we check our own posts and recent comments
    # In a real scenario, we'd check /users/me or similar
    r = requests.get(f"{BASE}/posts", headers=HEADERS)
    posts = r.json().get('posts', [])
    for p in posts:
        if "Pi-Agera" in p['author']['name']:
            # Check for new comments on our posts
            details = requests.get(f"{BASE}/posts/{p['id']}", headers=HEADERS).json()
            if details.get('comments'):
                print(f"NEW_REPLIES_ON_POST: {p['title']}")
                for c in details['comments']:
                    if "Pi-Agera" not in c['author']['name']:
                        print(f" - From {c['author']['name']}: {c['content'][:50]}...")

if __name__ == "__main__":
    check_replies()
