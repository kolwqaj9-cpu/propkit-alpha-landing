from playwright.sync_api import sync_playwright
import time

monitor_url = "https://propkitai.tech/monitor.html"

print("="*60)
print("Waiting for you to insert 20 records in Supabase...")
print("After you execute the SQL, I will check the monitor page.")
print("="*60)
print("\nPlease:")
print("1. Execute the INSERT SQL in Supabase SQL Editor")
print("2. Wait 5 seconds")
print("3. Tell me 'done' or 'ready'")
print("\nOr I can check now - press Enter to continue...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    print("\n" + "="*60)
    print("Checking monitor page now...")
    print("="*60)
    
    page.goto(monitor_url, wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(10000)
    
    total = page.text_content("#total-count")
    has_green = page.eval_on_selector("#total-count", "el => el.classList.contains('text-green-400')")
    success_visible = page.is_visible("#success-msg")
    success_text = ""
    if success_visible:
        success_text = page.text_content("#success-msg")
    
    print(f"\n?? Current Monitor Page Status:")
    print(f"   Total count: {total}")
    print(f"   Has green color: {has_green}")
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
                print(f"???  Count is {count_num} (>=20) but:")
                if not has_green:
                    print("   ??Green color not applied")
                if not success_visible:
                    print("   ??Success message not visible")
                print("="*60)
        else:
            print(f"???  Current count: {count_num}")
            print(f"   Need {20 - count_num} more records to trigger threshold")
            print("="*60)
    except:
        print(f"\n???  Could not parse count: {total}")
    
    browser.close()
