# RobloxAI — Multi-agent rendszer Roblox játékok automatikus generálására

**Status:** ⚠️ Prototype — multi-agent pipeline működik, Gemini/DeepSeek API-val

Multi-agent rendszer (Manager + Architect + Coder), ami automatikusan generál Roblox játékokat a Gemini és DeepSeek API-k segítségével.

## ⚠️ THIS PROJECT IS UNFINISHED — FEEL FREE TO CONTINUE IT ⚠️

**Ez a projekt NINCS KÉSZEN. Bárki folytathatja, aki akarja!**
Ezt a projektet Zsombi & Hermes Agent (Nous Research) közösen fejlesztette, de egyik projekt sincs 100%-osan befejezve.

---

## Agentek
- **🧭 Manager** — Feladatbontás, követelmény analízis, workflow orchestáció
- **🏗️ Architect** — Játékterv, szint struktúra, játékmechanikák definiálása
- **💻 Coder** — Lua kód generálás, Roblox Studio plugin

## API támogatás
- Google Gemini API (`gemini-2.0-flash`)
- DeepSeek API (`deepseek-chat`)
- Automatikus provider fallback hiba esetén

## Fájlok
| Fájl | Leírás |
|------|--------|
| `agent_roles.py` | Agent szerepkörök |
| `server.py` | Szerver |
| `plugin.lua` | Roblox Studio plugin |
| `test_*.py` | Tesztek |

## Fejlesztő
Zsombi & Hermes Agent (Nous Research)
