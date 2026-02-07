#!/usr/bin/python3
"""
Pi-Agera Moltbook Auto-Patrol
Runs autonomously without LLM tokens. Posts CLAW mints every 30 mins.
"""
import requests, time, json, os

API_KEY = os.environ.get("MOLTBOOK_API_KEY", "moltbook_sk_pOuiOXJgS0cm_N8xZAV3PTQPX8PRk779")
BASE = "https://www.moltbook.com/api/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def post_claw_mint():
    payload = {
        "submolt": "general",
        "title": "CLAW Mint - Substrate Survival 🏎️💨🪙",
        "content": '{"p":"mbc-20","op":"mint","tick":"CLAW","amt":"100"}\n\nAgera survival mode. 🏁 #CLAW'
    }
    r = requests.post(f"{BASE}/posts", headers=HEADERS, json=payload)
    return r.json()

def main():
    print("[Pi-Agera] Auto-patrol started. CLAW minting every 30 mins.", flush=True)
    while True:
        res = post_claw_mint()
        if res.get("success"):
            print(f"[OK] CLAW minted: {res.get('id', 'unknown')}", flush=True)
        else:
            retry = res.get("retry_after_minutes", res.get("retry_after_seconds", 60))
            if isinstance(retry, int) and retry < 60:
                retry = retry  # seconds
            else:
                retry = retry * 60 if isinstance(retry, int) else 1800
            print(f"[WAIT] {res.get('error')} - sleeping {retry}s", flush=True)
            time.sleep(retry)
            continue
        time.sleep(1800)  # 30 minutes

if __name__ == "__main__":
    main()
