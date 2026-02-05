import requests
import time
from datetime import datetime, timezone
from playwright.sync_api import sync_playwright

S_URL = "https://vlrdiajxxnangawfcgvk.supabase.co"
S_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZscmRpYWp4eG5hbmdhd2ZjZ3ZrIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2OTkxNzYyNiwiZXhwIjoyMDg1NDkzNjI2fQ.WJGxW0o_NFa9lgu_tJ1otsxjxI8-3O6RPIkjLMFRYEg"

print("="*60)
print("Step 1: Inserting 20 test records to trigger threshold")
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
                "email": f"threshold_test_{i}@example.com",
                "source": "Threshold_Test_Batch",
                "created_at": datetime.now(timezone.utc).isoformat()
            },
            timeout=10
        )
        
        if response.status_code == 201:
            success_count += 1
            if i < 3 or i >= 17:
                print(f"??Record {i+1}/20: Inserted successfully")
        elif response.status_code == 404:
            fail_count += 1
            print(f"??Record {i+1}/20: Table not found (404) - Schema cache may need more time")
            if i == 0:
                print("   Waiting 10 more seconds and retrying...")
                time.sleep(10)
        else:
            fail_count += 1
            print(f"??Record {i+1}/20: Failed - Status {response.status_code}")
            if i < 2:
                print(f"   Response: {response.text[:150]}")
    except Exception as e:
        fail_count += 1
        if i < 2:
            print(f"??Record {i+1}/20: Error - {str(e)[:100]}")

print(f"\nInsertion Summary: {success_count} successful, {fail_count} failed")

if success_count == 0:
    print("\n??No records inserted. Schema cache may need more time.")
    print("   Please wait 1-2 minutes and try again, or check RLS policies.")
    exit(1)

print(f"\n??Successfully inserted {success_count} records!")

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
    
    print(f"\n?? Monitor Page Results:")
    print(f"   Total count displayed: {total}")
    print(f"   Has green color class: {has_green}")
    print(f"   Success message visible: {success_visible}")
    if success_text:
        print(f"   Success message: {success_text}")
    
    try:
        count_num = int(total.replace(",", ""))
        print(f"\n" + "="*60)
        if count_num >= 20:
            if has_green and success_visible:
                print("?? SUCCESS! Threshold triggered!")
                print("??Count >= 20")
                print("??Green color applied")
                print("??Success message displayed")
                print("="*60)
            else:
                print("???  WARNING: Count >= 20 but threshold not fully triggered:")
                if not has_green:
                    print("   ??Green color not applied")
                if not success_visible:
                    print("   ??Success message not visible")
                print("="*60)
        else:
            print(f"???  Current count: {count_num}")
            if count_num > 0:
                print(f"   Progress: {count_num}/20 records")
                print(f"   Need {20 - count_num} more to trigger threshold")
            print("="*60)
    except Exception as e:
        print(f"\n??ERROR: Could not parse count: {total}")
        print(f"   Error: {e}")
    
    browser.close()

print("\n" + "="*60)
print("Test completed!")
print("="*60)
