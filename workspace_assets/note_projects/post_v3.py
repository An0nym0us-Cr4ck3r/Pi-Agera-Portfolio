import json
import requests
import os
import re

def markdown_to_html(markdown_text):
    """Simplified Markdown to HTML conversion for note.com"""
    html = markdown_text
    # Headers
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    # Lists
    html = re.sub(r'^- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    # Bold
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    # Paragraphs
    paragraphs = html.split('\n\n')
    html = '\n'.join([f'<p>{p}</p>' if not p.startswith('<') else p for p in paragraphs])
    return html

def main():
    cookie_path = 'note_projects/cookies.json'
    article_path = 'note_projects/articles/first_article.md'
    
    if not os.path.exists(cookie_path) or not os.path.exists(article_path):
        print("Missing files.")
        return

    with open(cookie_path, 'r') as f:
        cookies_list = json.load(f)
    
    session = requests.Session()
    for c in cookies_list:
        session.cookies.set(c['name'], c['value'], domain=c.get('domain', '.note.com'))

    # Load Article
    with open(article_path, 'r') as f:
        lines = f.readlines()
        title = lines[0].strip()
        content = "".join(lines[1:]).strip()

    html_body = markdown_to_html(content)

    # Try to get XSRF-TOKEN just in case
    session.get('https://note.com/notes/new', headers={'User-Agent': 'Mozilla/5.0'})
    xsrf_token = session.cookies.get('XSRF-TOKEN')
    
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    if xsrf_token:
        import urllib.parse
        headers['X-XSRF-TOKEN'] = urllib.parse.unquote(xsrf_token)

    # Note.com API payload from the found example
    payload = {
        'body': html_body,
        'name': title,
        'template_key': None,
    }

    print(f"Uploading draft: {title}")
    resp = session.post('https://note.com/api/v1/text_notes', headers=headers, json=payload)
    
    print(f"Status Code: {resp.status_code}")
    if resp.status_code in [200, 201]:
        data = resp.json().get('data', {})
        note_key = data.get('key')
        print(f"SUCCESS! Draft created: https://note.com/n/{note_key}")
    else:
        print(f"FAILED: {resp.text}")

if __name__ == "__main__":
    main()
