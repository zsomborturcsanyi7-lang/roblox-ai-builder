import os
import json
import requests
import uuid
import threading
import google.generativeai as genai
from flask import Flask, request, jsonify
from agent_roles import SYSTEM_PROMPTS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# --- CONFIG ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
ROBLOX_PROJECT_PATH = os.getenv("ROBLOX_PROJECT_PATH", "./src")
CURRENT_PROVIDER = os.getenv("AI_PROVIDER", "deepseek").lower()

if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
    except:
        CURRENT_PROVIDER = "deepseek"

# --- JOB STORAGE ---
jobs = {} # { job_id: { status: "pending"|"completed"|"error", result: [...] } }

# --- MEMORY ---
MEMORY_FILE = "project_memory.json"
def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, 'r') as f: return json.load(f)
        except: return {}
    return {}

def update_memory_key(key, value):
    mem = load_memory()
    mem[key] = value
    with open(MEMORY_FILE, 'w') as f: json.dump(mem, f, indent=2)
    return "Memory updated."

SERVER_TOOLS = {
    "update_memory": update_memory_key,
    "read_memory": lambda: json.dumps(load_memory())
}

import re

# --- AI ENGINES ---
def parse_json(text):
    try:
        text = text.strip()
        # Find the first '[' and last ']' for list, or '{' and '}' for object
        list_match = re.search(r'(\[.*\])', text, re.DOTALL)
        obj_match = re.search(r'(\{.*\})', text, re.DOTALL)
        
        json_text = text
        if list_match:
            json_text = list_match.group(1)
        elif obj_match:
            json_text = obj_match.group(1)
            
        return json.loads(json_text)
    except Exception as e:
        print(f"JSON Parse Error: {e} | Text: {text[:200]}")
        return [{"action": "print", "message": f"AI returned invalid JSON. Check server logs."}]

def generate_ai(system_prompt, user_msg, history):
    global CURRENT_PROVIDER
    if CURRENT_PROVIDER == "gemini":
        try:
            return generate_gemini(system_prompt, user_msg, history)
        except Exception as e:
            print(f"Gemini Error: {e}, falling back to DeepSeek")
            return generate_deepseek(system_prompt, user_msg, history)
    else:
        return generate_deepseek(system_prompt, user_msg, history)

def generate_gemini(system_prompt, user_msg, history):
    model = genai.GenerativeModel('gemini-1.5-flash')
    # Limit history to prevent token overflow
    context = history[-10:] if history else []
    full_prompt = f"{system_prompt}\n\nCONTEXT:\n{json.dumps(context)}\n\nUSER: {user_msg}\n\nIMPORTANT: Return ONLY a valid JSON list of actions. No conversational text."
    response = model.generate_content(full_prompt)
    return parse_json(response.text)

def generate_deepseek(system_prompt, user_msg, history):
    max_retries = 3
    # Limit history
    context = history[-10:] if history else []
    messages = [{"role": "system", "content": system_prompt + "\nIMPORTANT: Return ONLY a valid JSON list of actions. No conversational text."}] + context + [{"role": "user", "content": user_msg}]
    
    for attempt in range(max_retries):
        try:
            r = requests.post(
                "https://api.deepseek.com/chat/completions",
                json={"model": "deepseek-chat", "messages": messages, "temperature": 0.1},
                headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY.strip()}", "Content-Type": "application/json"},
                timeout=60
            )
            if r.status_code == 200:
                return parse_json(r.json()["choices"][0]["message"]["content"])
            elif r.status_code == 429: continue
        except Exception as e: 
            print(f"DeepSeek Attempt {attempt} failed: {e}")
            continue
    return [{"action": "print", "message": "DeepSeek Timeout/Error after retries."}]

# --- BACKGROUND WORKER ---
chat_history = []

def ai_worker(job_id, prompt, role):
    global chat_history, CURRENT_PROVIDER
    try:
        system_prompt = SYSTEM_PROMPTS.get(role, SYSTEM_PROMPTS["MANAGER"])
        print(f"--- JOB {job_id} | ROLE: {role} | PROVIDER: {CURRENT_PROVIDER} ---")
        
        actions = generate_ai(system_prompt, prompt, chat_history)

        print(f"RESPONSE: {json.dumps(actions, indent=2)}")

        final_actions = []
        for action in actions:
            act_type = action.get("action")
            if act_type in SERVER_TOOLS:
                res = SERVER_TOOLS[act_type](**{k:v for k,v in action.items() if k != "action"})
                final_actions.append({"action": "print", "message": f"Server: {res}"})
            elif act_type == "delegate_to":
                new_role = action.get("role")
                task = action.get("task")
                print(f"DELEGATING to {new_role}: {task}")
                # Recursive sub-task (simplified for polling)
                sub_actions = generate_ai(SYSTEM_PROMPTS.get(new_role), task, [])
                final_actions.extend(sub_actions)
            else:
                final_actions.append(action)

        chat_history.append({"role": "user", "content": prompt})
        jobs[job_id] = {"status": "completed", "result": final_actions}
    except Exception as e:
        print(f"Worker Error: {e}")
        jobs[job_id] = {"status": "error", "message": str(e)}

# --- ROUTES ---
@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt', '')
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "pending"}
    
    thread = threading.Thread(target=ai_worker, args=(job_id, prompt, "MANAGER"))
    thread.start()
    
    return jsonify({"job_id": job_id})

@app.route('/poll/<job_id>', methods=['GET'])
def poll(job_id):
    job = jobs.get(job_id)
    if not job: return jsonify({"status": "not_found"}), 404
    return jsonify(job)

@app.route('/clear', methods=['POST'])
def clear():
    global chat_history
    chat_history = []
    return jsonify({"status": "cleared"})

@app.route('/switch', methods=['POST'])
def switch():
    global CURRENT_PROVIDER
    data = request.json
    CURRENT_PROVIDER = data.get("provider", "deepseek")
    return jsonify({"provider": CURRENT_PROVIDER})

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"provider": CURRENT_PROVIDER, "pending_jobs": len([j for j in jobs.values() if j['status'] == 'pending'])})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=6000)
