import requests

S_URL = "https://vlrdiajxxnangawfcgvk.supabase.co"
S_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZscmRpYWp4eG5hbmdhd2ZjZ3ZrIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2OTkxNzYyNiwiZXhwIjoyMDg1NDkzNjI2fQ.WJGxW0o_NFa9lgu_tJ1otsxjxI8-3O6RPIkjLMFRYEg"

print("Testing RPC function...")
try:
    res = requests.post(
        f"{S_URL}/rest/v1/rpc/get_purchase_intents_count",
        headers={
            "apikey": S_KEY,
            "Authorization": f"Bearer {S_KEY}",
            "Content-Type": "application/json"
        },
        json={},
        timeout=10
    )
    print(f"Status: {res.status_code}")
    if res.status_code == 200:
        print(f"??RPC works! Count: {res.json()}")
    else:
        print(f"??Error: {res.text[:200]}")
except Exception as e:
    print(f"??Exception: {e}")
