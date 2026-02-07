import json
import requests
import os
import sys

def post_note():
    cookie_path = 'note_projects/cookies.json'
    article_path = 'note_projects/articles/first_article.md'
    
    if not os.path.exists(cookie_path) or not os.path.exists(article_path):
        print(f"Error: Required files missing.")
        return

    # Load Cookies
    with open(cookie_path, 'r') as f:
        cookies_list = json.load(f)
    
    session = requests.Session()
    for c in cookies_list:
        session.cookies.set(c['name'], c['value'], domain=c.get('domain', '.note.com'))

    # Get XSRF-TOKEN and Verify Session
    print("Connecting to note.com...")
    # Get the token from a page that definitely sets it
    r = session.get('https://note.com/settings/account', headers={'User-Agent': 'Mozilla/5.0'})
    
    xsrf_token = None
    for cookie in session.cookies:
        if cookie.name == 'XSRF-TOKEN':
            xsrf_token = cookie.value
            break
            
    if not xsrf_token:
        print("XSRF-TOKEN not in cookies, checking response headers...")
        # Sometimes it's set in the response headers of certain actions
        r = session.get('https://note.com/notes/new')
        for cookie in session.cookies:
            if cookie.name == 'XSRF-TOKEN':
                xsrf_token = cookie.value
                break

    if not xsrf_token:
        print("Error: Still no XSRF-TOKEN. Printing available cookies:")
        for c in session.cookies:
            print(f"{c.name}: {c.value[:10]}...")
        return
    
    import urllib.parse
    xsrf_token = urllib.parse.unquote(xsrf_token)

    # Read Article
    with open(article_path, 'r') as f:
        lines = f.readlines()
        title = lines[0].strip()
        body = "".join(lines[1:]).strip()

    # Note.com Draft API (v2 endpoint is more common now)
    # Testing /api/v2/notes
    headers = {
        'X-XSRF-TOKEN': xsrf_token,
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Referer': 'https://note.com/notes/new'
    }

    payload = {
        "title": title,
        "body": body,
        "status": "draft",
        "type": "TextNote"
    }

    print(f"Uploading draft: {title}")
    # Try V2 first
    resp = session.post('https://note.com/api/v2/notes', headers=headers, json=payload)
    
    if resp.status_code == 404:
        print("V2 endpoint 404, falling back to V1...")
        resp = session.post('https://note.com/api/v1/notes', headers=headers, json={"note": payload})

    if resp.status_code in [200, 201]:
        data = resp.json().get('data', {})
        key = data.get('key')
        print(f"SUCCESS! Draft created: https://note.com/n/{key}")
    else:
        print(f"Failed with status {resp.status_code}")
        print(resp.text)

if __name__ == "__main__":
    post_note()
