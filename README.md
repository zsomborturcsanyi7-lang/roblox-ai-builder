# RobloxAI — Multi-Agent Roblox Game Builder

**A multi-agent system (Manager + Architect + Coder) that automatically generates Roblox games using the Gemini and DeepSeek APIs.**

## 🤖 Description

RobloxAI is a multi-agent system that builds Roblox games using three specialized AI agents:

- **🧭 Manager** — Task decomposition, requirements analysis, workflow orchestration
- **🏗️ Architect** — Game design, level structure, game mechanics definition
- **💻 Coder** — Lua code generation, Roblox Studio plugin, implementation

### API Support

- **Google Gemini API** — `gemini-2.0-flash`
- **DeepSeek API** — `deepseek-chat`
- Automatic provider fallback on error

### Plugin

`plugin.lua` is a Roblox Studio plugin that provides a direct connection between the server and Roblox Studio.

## 📁 File Structure

```
RobloxAI/
├── server.py                    # Flask server (184 lines)
├── agent_roles.py               # AI agent roles and prompts
├── plugin.lua                   # Roblox Studio plugin
├── project_memory.json          # Project memory
├── memory.json                  # General memory
├── test_connection.py           # Connection tester
├── test_memory.py               # Memory test
├── test_integration.py          # Integration test
├── list_models.py               # Available model listing
├── check_models.js              # Model checker (JS)
├── check_api.py                 # API checker
├── requirements.txt             # Dependencies
├── .env                         # Environment variables (API keys)
└── sessions/                    # Saved sessions
    ├── 1b81aebd.json
    ├── 2dffe64b.json
    └── de45239b.json
```

## 🚀 Usage

### Environment setup

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
DEEPSEEK_API_KEY=your_deepseek_api_key
AI_PROVIDER=deepseek
ROBLOX_PROJECT_PATH=./src
```

### Starting the server

```bash
# Install dependencies
pip install -r requirements.txt

# Start server
python server.py
```

The server starts at `http://localhost:5000`.

### API Endpoints

```bash
# Create a new game project
curl -X POST http://localhost:5000/create \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Build an obby course with checkpoints"}'

# Query task status
curl http://localhost:5000/status/<job_id>

# Retrieve result
curl http://localhost:5000/result/<job_id>
```

### Testing the connection

```bash
python test_connection.py
python check_api.py
```

### Roblox Studio Plugin

1. Open Roblox Studio
2. Load the `plugin.lua` file
3. Set the server URL
4. Use the plugin buttons for game generation

## 📦 Dependencies

```bash
pip install flask google-generativeai python-dotenv requests
```

- **Python 3.10+**
- **Flask** — web server
- **google-generativeai** — Gemini API client
- **python-dotenv** — environment variables
- **requests** — HTTP client (DeepSeek API)

## 🔄 Workflow

```
User → "Build an obby course"
    ↓
[MANAGER] Task analysis
    ├── Level: obby style
    ├── Mechanics: checkpoint, respawn
    ├── Difficulty: medium
    └── Assets: platforms, ladders
    ↓
[ARCHITECT] Game design
    ├── Level map
    ├── Object list
    └── Gameplay flow
    ↓
[CODER] Lua code generation
    ├── Map generator script
    ├── Checkpoint system
    ├── Respawn logic
    └── Plugin commands
    ↓
Roblox Studio plugin executes the code
    ↓
FINISHED GAME 🎮
```

## 🎯 Agent Roles

### Manager prompt (excerpt)

```
You are an experienced game development project manager.
Decompose the task into sub-units.
Identify the required components.
Prioritize the tasks.
```

### Architect prompt (excerpt)

```
You are a Roblox game designer.
Design the level structure.
Define the game mechanics.
Create a detailed plan for the coder.
```

### Coder prompt (excerpt)

```
You are a Roblox Lua developer.
Generate clean, working Lua code.
Follow Roblox best practices.
Create modular, reusable code.
```

## ⚙️ Configuration

The `.env` file variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | — |
| `DEEPSEEK_API_KEY` | DeepSeek API key | — |
| `AI_PROVIDER` | AI provider (`gemini` / `deepseek`) | `deepseek` |
| `ROBLOX_PROJECT_PATH` | Generated files location | `./src` |

## Author
Zsombi & Hermes Agent (Nous Research)
