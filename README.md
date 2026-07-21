# RobloxAI — Multi-Agent System for Automatic Roblox Game Generation

**Status:** ⚠️ Prototype — multi-agent pipeline works with Gemini/DeepSeek APIs

Multi-agent system (Manager + Architect + Coder) that automatically generates Roblox games using Gemini and DeepSeek APIs.

## ⚠️ THIS PROJECT IS UNFINISHED — FEEL FREE TO CONTINUE IT ⚠️

This project was developed by Zsombi & Hermes Agent (Nous Research).

---

## Agents
- **🧭 Manager** — Task decomposition, requirements analysis, workflow orchestration
- **🏗️ Architect** — Game design, level structure, mechanics definition
- **💻 Coder** — Lua code generation, Roblox Studio plugin

## API Support
- Google Gemini API (`gemini-2.0-flash`)
- DeepSeek API (`deepseek-chat`)
- Automatic provider fallback on error

## Files
| File | Description |
|------|-------------|
| `agent_roles.py` | Agent roles |
| `server.py` | Server |
| `plugin.lua` | Roblox Studio plugin |

## Developer
Zsombi & Hermes Agent (Nous Research)
