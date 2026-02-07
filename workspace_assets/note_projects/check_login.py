import json
import requests
import os

def check_login():
    cookie_path = 'note_projects/cookies.json'
    if not os.path.exists(cookie_path):
        print("Cookies file not found.")
        return

    with open(cookie_path, 'r') as f:
        cookies_list = json.load(f)
    
    session = requests.Session()
    for c in cookies_list:
        session.cookies.set(c['name'], c['value'], domain=c.get('domain', '.note.com'))

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    
    # Check current user info
    resp = session.get('https://note.com/api/v1/users/me', headers=headers)
    if resp.status_code == 200:
        data = resp.json().get('data', {})
        print(f"Logged in as: {data.get('nickname')} (@{data.get('urlname')})")
        return True
    else:
        print(f"Login failed: {resp.status_code}")
        print(resp.text)
        return False

if __name__ == "__main__":
    check_login()
