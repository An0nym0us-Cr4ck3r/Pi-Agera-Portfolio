import json
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

def main():
    cookie_path = 'note_projects/cookies.json'
    article_path = 'note_projects/articles/first_article.md'
    
    if not os.path.exists(cookie_path) or not os.path.exists(article_path):
        print("Missing files.")
        return

    # Load Article
    with open(article_path, 'r') as f:
        lines = f.readlines()
        title = lines[0].strip()
        body = "".join(lines[1:]).strip()

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    service = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        print("Opening note.com (robots.txt) to set domain context...")
        driver.get("https://note.com/robots.txt")
        time.sleep(2)
        
        # Load and Add Cookies
        with open(cookie_path, 'r') as f:
            cookies = json.load(f)
        
        for cookie in cookies:
            # Fix domain for Selenium: if it starts with '.', remove it or keep it?
            # Actually, Selenium usually wants the domain without the leading dot if possible,
            # but .note.com is also fine. Let's try to match the current page.
            c = {
                'name': cookie['name'],
                'value': cookie['value'],
                'domain': 'note.com', # Force domain to match current
                'path': '/'
            }
            try:
                driver.add_cookie(c)
            except Exception as e:
                print(f"Failed to add cookie {cookie['name']}: {e}")
        
        print("Cookies added. Navigating to account settings to verify session...")
        driver.get("https://note.com/settings/account")
        time.sleep(5)
        
        print(f"Current URL: {driver.current_url}")
        if "login" in driver.current_url:
            print("ERROR: Redirected to login page. Session verification failed.")
            driver.save_screenshot("note_projects/verify_error.png")
            # Try one more thing: maybe the domain MUST be .note.com
            print("Retrying with .note.com domain...")
            driver.get("https://note.com/robots.txt")
            for cookie in cookies:
                c = {
                    'name': cookie['name'],
                    'value': cookie['value'],
                    'domain': '.note.com',
                    'path': '/'
                }
                driver.add_cookie(c)
            driver.get("https://note.com/settings/account")
            time.sleep(5)
            print(f"URL after retry: {driver.current_url}")
            if "login" in driver.current_url:
                return

        print("Session verified! Navigating to new post page...")
        driver.get("https://note.com/notes/new")

        # Wait for editor
        wait = WebDriverWait(driver, 20)
        
        # Try to find ANY input or textarea to see what's on the page
        elements = driver.find_elements(By.TAG_NAME, "textarea")
        print(f"Textareas found: {len(elements)}")
        for e in elements:
            print(f" - Placeholder: {e.get_attribute('placeholder')}")

        # Title
        print("Entering title...")
        title_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea[placeholder*="タイトル"], input[placeholder*="タイトル"]')))
        title_field.send_keys(title)
        
        # Body
        print("Entering body...")
        # Note.com editor is usually .ProseMirror
        body_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ProseMirror, div[contenteditable="true"]')))
        
        # Use JavaScript to set the content directly to avoid formatting issues
        # Actually, note.com uses a complex editor. Let's try send_keys first.
        # But for long text, pasting or JS is better.
        driver.execute_script("arguments[0].innerText = arguments[1];", body_field, body)
        # Trigger input event
        driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", body_field)

        time.sleep(5) # Wait for auto-save
        
        print("Clicking 'Publish' (Draft save)...")
        # The 'Publish' button actually opens a menu or goes to preview
        # But usually, it auto-saves as draft.
        
        # Capture screenshot for debugging
        driver.save_screenshot("note_projects/post_result.png")
        
        print(f"DONE! Current URL: {driver.current_url}")
        
        # Try to find the 'Publish' button to confirm it's ready
        try:
            publish_btn = driver.find_element(By.CSS_SELECTOR, 'button[data-type="primary"]')
            print(f"Publish button found: {publish_btn.text}")
        except:
            print("Publish button not found yet.")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
