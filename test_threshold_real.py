import requests
import time
from datetime import datetime, timezone
from playwright.sync_api import sync_playwright

S_URL = "https://vlrdiajxxnangawfcgvk.supabase.co"
S_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZscmRpYWp4eG5hbmdhd2ZjZ3ZrIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2OTkxNzYyNiwiZXhwIjoyMDg1NDkzNjI2fQ.WJGxW0o_NFa9lgu_tJ1otsxjxI8-3O6RPIkjLMFRYEg"

print("="*60)
print("Step 1: Testing table access and inserting 20 records")
print("="*60)

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
                "source": "Automated_Threshold_Test",
                "created_at": datetime.now(timezone.utc).isoformat()
            },
            timeout=10
        )
        
        if response.status_code == 201:
            success_count += 1
            if i < 5 or i == 19:
                print(f"??Record {i+1}/20: Inserted successfully")
        else:
            fail_count += 1
            print(f"??Record {i+1}/20: Failed - Status {response.status_code}")
            if i < 3:
                print(f"  Response: {response.text[:200]}")
    except Exception as e:
        fail_count += 1
        print(f"??Record {i+1}/20: Error - {str(e)[:100]}")

print(f"\nInsertion Summary: {success_count} successful, {fail_count} failed")

if success_count == 0:
    print("\n??ERROR: No records inserted. Please check:")
    print("  1. RLS policies are correctly set")
    print("  2. API key has correct permissions")
    exit(1)

print("\n" + "="*60)
print("Step 2: Waiting 5 seconds for data to sync...")
print("="*60)
time.sleep(5)

print("\n" + "="*60)
print("Step 3: Checking monitor page for threshold trigger")
print("="*60)
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
    
    print(f"\nMonitor Page Results:")
    print(f"  Total count displayed: {total}")
    print(f"  Has green color class: {has_green}")
    print(f"  Success message visible: {success_visible}")
    if success_text:
        print(f"  Success message text: {success_text}")
    
    try:
        count_num = int(total.replace(",", ""))
        print(f"\n" + "="*60)
        if count_num >= 20:
            if has_green and success_visible:
                print("??SUCCESS! Threshold triggered!")
                print("??Count >= 20, green color and success message displayed!")
                print("="*60)
            else:
                print("???  WARNING: Count >= 20 but:")
                if not has_green:
                    print("  ??Green color not applied")
                if not success_visible:
                    print("  ??Success message not visible")
                print("="*60)
        else:
            print(f"???  INFO: Count is {count_num} (<20)")
            print("   Threshold will trigger when count reaches 20")
            print("="*60)
    except Exception as e:
        print(f"\n??ERROR: Could not parse count: {total}")
        print(f"   Error: {e}")
    
    browser.close()

print("\n" + "="*60)
print("Test completed!")
print("="*60)
