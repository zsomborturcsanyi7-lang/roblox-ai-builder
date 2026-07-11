import subprocess
import time
import json
import urllib.request
import sys
import os

SERVER_PORT = 6000
SERVER_URL = f"http://127.0.0.1:{SERVER_PORT}/generate"
SERVER_SCRIPT = "server.py"

def start_server():
    print(f"Starting {SERVER_SCRIPT}...")
    process = subprocess.Popen([sys.executable, "-u", SERVER_SCRIPT], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return process

def stop_server(process):
    print("Stopping server...")
    process.terminate()
    try:
        stdout, stderr = process.communicate(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()
    print("Server stopped.")

def send_request(prompt):
    print(f"User: {prompt}")
    data = json.dumps({"prompt": prompt}).encode('utf-8')
    req = urllib.request.Request(SERVER_URL, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            for item in result:
                if item.get("action") == "print":
                    print(f"AI: {item['message']}")
            return result
    except Exception as e:
        print(f"Request failed: {e}")
        return None

def main():
    # --- STEP 1: Teach Fact ---
    server1 = start_server()
    time.sleep(5)
    print("\n--- Session 1 ---")
    
    # 1. Chat Interaction
    send_request("Hi! Please remember that my favorite color is neon green.")
    
    # 2. Verify if it used the tool (we can't easily see internal tool calls here, but we check response)
    
    stop_server(server1)
    
    # --- STEP 2: Verify Persistence ---
    print("\n--- Restarting Server ---")
    time.sleep(2)
    server2 = start_server()
    time.sleep(5)
    print("\n--- Session 2 ---")
    
    # 3. Recall Fact
    send_request("What is my favorite color?")
    
    stop_server(server2)

if __name__ == "__main__":
    main()
