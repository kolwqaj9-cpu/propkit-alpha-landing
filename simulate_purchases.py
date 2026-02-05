from playwright.sync_api import sync_playwright
import time

index_url = "https://propkitai.tech/index.html"
monitor_url = "https://propkitai.tech/monitor.html"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    print("=== Step 1: Opening index.html ===")
    page.goto(index_url, wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(3000)
    
    btn = page.query_selector("#purchase-btn")
    if not btn:
        print("ERROR: Purchase button not found!")
        browser.close()
        exit(1)
    
    print("Purchase button found. Starting to simulate 20 clicks...")
    
    for i in range(20):
        try:
            page.click("#purchase-btn")
            print(f"Click {i+1}/20: Button clicked")
            page.wait_for_timeout(500)
            try:
                page.wait_for_event("dialog", timeout=1000)
                dialog = page.get_by_role("dialog")
                if dialog:
                    dialog.accept()
            except:
                pass
        except Exception as e:
            print(f"Click {i+1}/20 failed: {e}")
        time.sleep(0.3)
    
    print("\n=== Step 2: Waiting for data to sync (10 seconds) ===")
    time.sleep(10)
    
    print("\n=== Step 3: Checking monitor page ===")
    monitor_page = browser.new_page()
    monitor_page.goto(monitor_url, wait_until="domcontentloaded", timeout=30000)
    monitor_page.wait_for_timeout(8000)
    
    total = monitor_page.text_content("#total-count")
    has_green = monitor_page.eval_on_selector("#total-count", "el => el.classList.contains('text-green-400')")
    success_visible = monitor_page.is_visible("#success-msg")
    success_text = ""
    if success_visible:
        success_text = monitor_page.text_content("#success-msg")
    
    print(f"\n=== Results ===")
    print(f"Total count: {total}")
    print(f"Has green color: {has_green}")
    print(f"Success message visible: {success_visible}")
    if success_text:
        print(f"Success message: {success_text}")
    
    try:
        count_num = int(total.replace(",", ""))
        if count_num >= 20:
            if has_green and success_visible:
                print("\nSUCCESS: Threshold triggered! Count >= 20, green color and success message displayed!")
            else:
                print(f"\nWARNING: Count is {count_num} (>=20) but green color or success message not visible")
        else:
            print(f"\nINFO: Count is {count_num} (<20), threshold not reached yet")
    except:
        print(f"\nCould not parse count: {total}")
    
    print("\nKeeping browser open for 5 seconds for manual inspection...")
    time.sleep(5)
    browser.close()
