from playwright.sync_api import sync_playwright
import requests
import time

S_URL = "https://vlrdiajxxnangawfcgvk.supabase.co"
S_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZscmRpYWp4eG5hbmdhd2ZjZ3ZrIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2OTkxNzYyNiwiZXhwIjoyMDg1NDkzNjI2fQ.WJGxW0o_NFa9lgu_tJ1otsxjxI8-3O6RPIkjLMFRYEg"

print("="*60)
print("Step 1: Testing RPC function")
print("="*60)

try:
    rpc_res = requests.post(
        f"{S_URL}/rest/v1/rpc/get_purchase_intents_count",
        headers={
            "apikey": S_KEY,
            "Authorization": f"Bearer {S_KEY}",
            "Content-Type": "application/json"
        },
        json={},
        timeout=10
    )
    
    if rpc_res.status_code == 200:
        count = rpc_res.json()
        print(f"??RPC function works! Current count: {count}")
    else:
        print(f"??RPC function failed: Status {rpc_res.status_code}")
        print(f"   Response: {rpc_res.text[:200]}")
        count = 0
except Exception as e:
    print(f"??RPC function error: {e}")
    count = 0

print("\n" + "="*60)
print("Step 2: Opening monitor.html in browser")
print("="*60)

monitor_url = "https://propkitai.tech/monitor.html"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    console_logs = []
    page.on("console", lambda msg: console_logs.append(msg.text))
    
    page.goto(monitor_url, wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(12000)
    
    total_displayed = page.text_content("#total-count")
    has_green = page.eval_on_selector("#total-count", "el => el.classList.contains('text-green-400')")
    success_visible = page.is_visible("#success-msg")
    success_text = ""
    if success_visible:
        success_text = page.text_content("#success-msg")
    
    print(f"\n?? Monitor Page Results:")
    print(f"   Displayed count: {total_displayed}")
    print(f"   Has green color: {has_green}")
    print(f"   Success message visible: {success_visible}")
    if success_text:
        print(f"   Success message: {success_text}")
    
    print(f"\n?? Console logs (last 3):")
    for log in console_logs[-3:]:
        print(f"   {log}")
    
    print(f"\n" + "="*60)
    print("Final Diagnosis:")
    print("="*60)
    
    try:
        count_num = int(total_displayed.replace(",", ""))
        if count_num >= 20:
            if has_green and success_visible:
                print("?? SUCCESS! Threshold triggered!")
                print("??Count >= 20")
                print("??Green color applied")
                print("??Success message displayed")
            else:
                print(f"???  Count is {count_num} (>=20) but threshold not fully triggered")
        else:
            print(f"???  Current count: {count_num}")
            if count_num > 0:
                print(f"   Progress: {count_num}/20")
                print(f"   Need {20 - count_num} more to trigger threshold")
    except:
        print(f"???  Could not parse count: {total_displayed}")
    
    print("\nKeeping browser open for 5 seconds...")
    page.wait_for_timeout(5000)
    browser.close()
