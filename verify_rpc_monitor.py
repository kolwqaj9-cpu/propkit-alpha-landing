from playwright.sync_api import sync_playwright

monitor_url = "https://propkitai.tech/monitor.html?v=888"

print("="*60)
print("Verifying monitor page with RPC function")
print("="*60)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    console_logs = []
    page.on("console", lambda msg: console_logs.append(msg.text))
    
    print(f"\nOpening: {monitor_url}")
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
    
    print(f"\n?? Console logs (last 5):")
    for log in console_logs[-5:]:
        print(f"   {log}")
    
    print(f"\n" + "="*60)
    print("Final Result:")
    print("="*60)
    
    try:
        count_num = int(total_displayed.replace(",", ""))
        if count_num >= 20:
            if has_green and success_visible:
                print("?? SUCCESS! Threshold triggered!")
                print(f"??Count: {count_num} (>= 20)")
                print("??Green color applied")
                print("??Success message displayed")
                print("="*60)
            else:
                print(f"???  Count is {count_num} (>=20) but:")
                if not has_green:
                    print("   ??Green color not applied")
                if not success_visible:
                    print("   ??Success message not visible")
        else:
            print(f"???  Current count: {count_num} (< 20)")
            print(f"   Need {20 - count_num} more to trigger threshold")
    except Exception as e:
        print(f"???  Could not parse count: {total_displayed}")
        print(f"   Error: {e}")
    
    print("\nKeeping browser open for 10 seconds for inspection...")
    page.wait_for_timeout(10000)
    browser.close()
