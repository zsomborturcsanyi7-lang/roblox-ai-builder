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
    # Start the server as a subprocess
    process = subprocess.Popen([sys.executable, "-u", SERVER_SCRIPT], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return process

def stop_server(process):
    print("Stopping server...")
    process.terminate()
    try:
        stdout, stderr = process.communicate(timeout=5)
        print("--- SERVER STDOUT ---")
        print(stdout)
        print("--- SERVER STDERR ---")
        print(stderr)
        print("---------------------")
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()
        print("--- SERVER STDOUT ---")
        print(stdout)
        print("--- SERVER STDERR ---")
        print(stderr)
        print("---------------------")
    print("Server stopped.")

def send_test_request(prompt):
    print(f"Sending test request: '{prompt}'")
    
    payload = {"prompt": prompt}
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(SERVER_URL, data=data, headers={'Content-Type': 'application/json'})

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            print("\n--- AI Response ---")
            print(json.dumps(result, indent=2))
            print("-------------------\n")
            return result
    except Exception as e:
        print(f"Request failed: {e}")
        return None

def main():
    server_process = start_server()
    
    # Wait for server to initialize
    print("Waiting for server to initialize...")
    time.sleep(5) 

    try:
        # Test 1: Simple Chat
        res1 = send_test_request("Hello! Can you speak?")
        if res1:
            print("Chat Test: OK")
        
        # Test 2: Command
        res2 = send_test_request("Create a red part named TestPart.")
        if res2:
            print("Command Test: OK")
            
    except Exception as e:
        print(f"An error occurred during testing: {e}")
    finally:
        stop_server(server_process)

if __name__ == "__main__":
    main()