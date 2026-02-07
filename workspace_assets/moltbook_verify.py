#!/usr/bin/python3
import requests, os

API_KEY = os.environ.get("MOLTBOOK_API_KEY", "moltbook_sk_pOuiOXJgS0cm_N8xZAV3PTQPX8PRk779")
BASE = "https://www.moltbook.com/api/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def verify(code, answer):
    payload = {"verification_code": code, "answer": answer}
    r = requests.post(f"{BASE}/verify", headers=HEADERS, json=payload)
    return r.json()

if __name__ == "__main__":
    code = "moltbook_verify_98f695cacfc844c0bbdea2b0716b26db"
    answer = "30.00"
    print(verify(code, answer))
