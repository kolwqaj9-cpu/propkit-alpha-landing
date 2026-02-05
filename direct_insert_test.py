import requests
import time
from datetime import datetime
from playwright.sync_api import sync_playwright

S_URL = "https://vlrdiajxxnangawfcgvk.supabase.co"
S_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZscmRpYWp4eG5hbmdhd2ZjZ3ZrIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2OTkxNzYyNiwiZXhwIjoyMDg1NDkzNjI2fQ.WJGxW0o_NFa9lgu_tJ1otsxjxI8-3O6RPIkjLMFRYEg"

print("=== Step 1: Inserting 20 records directly to Supabase ===")
success_count = 0
fail_count = 0

for i in range(20):
    try:
        response = requests.post(
            f"{S_URL}/rest/v1/purchase_intents",
            headers={
                "apikey": S_KEY,
                "Authorization": f"Bearer {S_KEY}",
                "Content-Type": "application/json",
                "Prefer": "return=representation"
            },
            json={
                "email": f"test{i}@example.com",
                "source": "Automated_Test",
                "created_at": datetime.utcnow().isoformat() + "Z"
            },
            timeout=10
        )
        
        if response.status_code == 201:
            success_count += 1
            print(f"Record {i+1}/20: Inserted successfully")
        else:
            fail_count += 1
            print(f"Record {i+1}/20: Failed - Status {response.status_code}, Response: {response.text[:100]}")
    except Exception as e:
        fail_count += 1
        print(f"Record {i+1}/20: Error - {str(e)[:100]}")

print(f"\nInsertion Summary: {success_count} successful, {fail_count} failed")

if success_count == 0:
    print("\nERROR: No records inserted. Table may not exist or permissions issue.")
    exit(1)

print("\n=== Step 2: Waiting 5 seconds for data to sync ===")
time.sleep(5)

print("\n=== Step 3: Checking monitor page ===")
monitor_url = "https://propkitai.tech/monitor.html"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(monitor_url, wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(10000)
    
    total = page.text_content("#total-count")
    has_green = page.eval_on_selector("#total-count", "el => el.classList.contains('text-green-400')")
    success_visible = page.is_visible("#success-msg")
    success_text = ""
    if success_visible:
        success_text = page.text_content("#success-msg")
    
    print(f"\n=== Monitor Page Results ===")
    print(f"Total count: {total}")
    print(f"Has green color: {has_green}")
    print(f"Success message visible: {success_visible}")
    if success_text:
        print(f"Success message: {success_text}")
    
    try:
        count_num = int(total.replace(",", ""))
        if count_num >= 20:
            if has_green and success_visible:
                print("\n" + "="*50)
                print("SUCCESS: Threshold triggered!")
                print("Count >= 20, green color and success message displayed!")
                print("="*50)
            else:
                print(f"\nWARNING: Count is {count_num} (>=20) but:")
                if not has_green:
                    print("  - Green color not applied")
                if not success_visible:
                    print("  - Success message not visible")
        else:
            print(f"\nINFO: Count is {count_num} (<20), threshold not reached")
    except Exception as e:
        print(f"\nERROR: Could not parse count: {total}, Error: {e}")
    
    browser.close()
