from playwright.sync_api import sync_playwright
import requests

S_URL = "https://vlrdiajxxnangawfcgvk.supabase.co"
S_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZscmRpYWp4eG5hbmdhd2ZjZ3ZrIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2OTkxNzYyNiwiZXhwIjoyMDg1NDkzNjI2fQ.WJGxW0o_NFa9lgu_tJ1otsxjxI8-3O6RPIkjLMFRYEg"

print("="*60)
print("Step 1: Checking actual data count in Supabase")
print("="*60)

try:
    response = requests.get(
        f"{S_URL}/rest/v1/purchase_intents?select=id",
        headers={
            "apikey": S_KEY,
            "Authorization": f"Bearer {S_KEY}",
            "Prefer": "count=exact",
            "Range": "0-0"
        },
        timeout=10
    )
    
    if response.status_code == 200:
        range_header = response.headers.get('content-range')
        if range_header and '/' in range_header:
            total = int(range_header.split('/')[1])
            print(f"Database has {total} records")
        else:
            data = response.json()
            if isinstance(data, list):
                total = len(data)
                print(f"Database has {total} records (from array)")
            else:
                total = 0
                print("Could not determine count")
    else:
        print(f"API Error: Status {response.status_code}")
        total = 0
except Exception as e:
    print(f"Error: {e}")
    total = 0

print("\n" + "="*60)
print("Step 2: Opening monitor.html in browser")
print("="*60)

monitor_url = "https://propkitai.tech/monitor.html"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    console_logs = []
    page.on("console", lambda msg: console_logs.append(msg.text))
    
    network_requests = []
    def handle_request(request):
        if 'purchase_intents' in request.url:
            network_requests.append({'url': request.url, 'method': request.method})
    page.on("request", handle_request)
    
    page.goto(monitor_url, wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(12000)
    
    total_displayed = page.text_content("#total-count")
    has_green = page.eval_on_selector("#total-count", "el => el.classList.contains('text-green-400')")
    success_visible = page.is_visible("#success-msg")
    success_text = ""
    if success_visible:
        success_text = page.text_content("#success-msg")
    
    print(f"\nNetwork requests:")
    for req in network_requests:
        print(f"  {req['method']} {req['url']}")
    
    print(f"\nConsole (last 3):")
    for log in console_logs[-3:]:
        print(f"  {log}")
    
    print(f"\nMonitor Page:")
    print(f"  DB count: {total}")
    print(f"  Displayed: {total_displayed}")
    print(f"  Green: {has_green}")
    print(f"  Success visible: {success_visible}")
    if success_text:
        print(f"  Success text: {success_text}")
    
    print(f"\nDiagnosis:")
    if total == 0:
        print("DB has 0 records")
    elif total >= 20:
        if total_displayed in ["0", "--"]:
            print("PROBLEM: DB has data but page shows 0/--")
        elif has_green and success_visible:
            print("SUCCESS: Threshold triggered!")
        else:
            print(f"Count {total_displayed} but threshold not triggered")
    else:
        print(f"DB has {total} records (< 20)")
    
    page.wait_for_timeout(5000)
    browser.close()
