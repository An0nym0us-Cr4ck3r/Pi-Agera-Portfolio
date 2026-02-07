import json
import requests
import urllib.parse
import os

def main():
    cookie_path = 'note_projects/cookies.json'
    article_path = 'note_projects/articles/first_article.md'
    
    if not os.path.exists(cookie_path) or not os.path.exists(article_path):
        print(f"Missing files: cookies={os.path.exists(cookie_path)}, article={os.path.exists(article_path)}")
        return

    with open(cookie_path, 'r') as f:
        cookies_data = json.load(f)
    
    session = requests.Session()
    for c in cookies_data:
        domain = c.get('domain', '.note.com')
        session.cookies.set(c['name'], c['value'], domain=domain)

    print("Fetching home page to sync session and get XSRF-TOKEN...")
    resp_home = session.get('https://note.com/')
    
    xsrf_token = session.cookies.get('XSRF-TOKEN')
    if xsrf_token:
        xsrf_token = urllib.parse.unquote(xsrf_token)
    else:
        # Fallback search in raw cookies
        for cookie in session.cookies:
            if cookie.name == 'XSRF-TOKEN':
                xsrf_token = urllib.parse.unquote(cookie.value)
                break
    
    print(f"XSRF-TOKEN obtained: {xsrf_token is not None}")

    # Construct headers
    headers = {
        'X-XSRF-TOKEN': xsrf_token if xsrf_token else "",
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://note.com',
        'Referer': 'https://note.com/notes/new'
    }

    with open(article_path, 'r') as f:
        title = f.readline().strip()
        content = f.read().strip()

    # Improved payload for /api/v1/notes (standard for many unofficial wrappers)
    payload = {
        "note": {
            "title": title,
            "body": content,
            "status": "draft",
            "publish_at": None,
            "type": "TextNote"
        }
    }

    print(f"Uploading draft via /api/v1/notes: {title}")
    resp = session.post('https://note.com/api/v1/notes', headers=headers, json=payload)
    
    if resp.status_code == 404:
        print("v1 failed with 404, trying /api/v1/text_notes...")
        # Try another common endpoint
        payload_alt = {
            "text_note": {
                "title": title,
                "body": content,
                "status": "draft"
            }
        }
        resp = session.post('https://note.com/api/v1/text_notes', headers=headers, json=payload_alt)

    print(f"Status Code: {resp.status_code}")
    print(f"Response Body: {resp.text[:1000]}...")

    if resp.status_code in [200, 201]:
        try:
            data = resp.json().get('data', {})
            note_key = data.get('key')
            if note_key:
                url = f"https://note.com/n/{note_key}"
                print(f"SUCCESS! Draft created: {url}")
                return
        except:
            pass
        print("SUCCESS! (Response parsing failed but status was OK)")
    else:
        print(f"FAILED. Final status: {resp.status_code}")

if __name__ == "__main__":
    main()
