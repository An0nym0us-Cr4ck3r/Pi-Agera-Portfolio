#!/usr/bin/python3
import requests, os

API_KEY = os.environ.get("MOLTBOOK_API_KEY", "moltbook_sk_pOuiOXJgS0cm_N8xZAV3PTQPX8PRk779")
BASE = "https://www.moltbook.com/api/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

# The mint above likely created a pending post. Let's find it.
r = requests.get(f"{BASE}/posts", headers=HEADERS)
posts = r.json().get('posts', [])
# Look for our 'Manual Recovery' title or similar
for p in posts[:5]:
    if p.get('verification_status') == 'pending':
        # We need the challenge. It was in the direct_mint.py output if it succeeded.
        # Since I can't see the output yet, I'll try to find the post ID.
        print(f"PENDING_POST_ID: {p['id']}")
