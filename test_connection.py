import requests
import time
import json

BASE_URL = "http://127.0.0.1:6000"

def test_connection():
    print("Testing /status...")
    try:
        r = requests.get(f"{BASE_URL}/status")
        print(f"Status: {r.status_code}, Response: {r.json()}")
    except Exception as e:
        print(f"Status check failed: {e}")
        return

    print("\nTesting /generate...")
    try:
        r = requests.post(f"{BASE_URL}/generate", json={"prompt": "Hello, say hi!"})
        if r.status_code != 200:
            print(f"Generate failed: {r.status_code}")
            return
        job_id = r.json().get("job_id")
        print(f"Job ID: {job_id}")
    except Exception as e:
        print(f"Generate request failed: {e}")
        return

    print("\nPolling for results...")
    for _ in range(30):
        try:
            r = requests.get(f"{BASE_URL}/poll/{job_id}")
            data = r.json()
            status = data.get("status")
            print(f"Polling... status: {status}")
            if status == "completed":
                print("Success! Result:")
                print(json.dumps(data.get("result"), indent=2))
                return
            elif status == "error":
                print(f"Job error: {data.get('message')}")
                return
        except Exception as e:
            print(f"Polling failed: {e}")
            break
        time.sleep(2)
    print("Polling timed out.")

if __name__ == "__main__":
    test_connection()
