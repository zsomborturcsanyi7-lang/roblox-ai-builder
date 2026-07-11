# RobloxAI — Multi-Agent Roblox Játéképítő

**Több AI ágensből álló rendszer (Menedzser + Építész + Kódoló), amely automatikusan generál Roblox játékokat a Gemini és DeepSeek API segítségével.**

## 🤖 Leírás

A RobloxAI egy multi-agent rendszer, amely három specializált AI ágens segítségével épít Roblox játékokat:

- **🧭 Menedzser (Manager)** — Feladat felbontása, követelmények elemzése, munkafolyamat irányítása
- **🏗️ Építész (Architect)** — Játéktervezés, pálya struktúra, játékmechanika definiálása
- **💻 Kódoló (Coder)** — Lua kód generálása, Roblox Studio plugin, implementáció

### API támogatás

- **Google Gemini API** — `gemini-2.0-flash`
- **DeepSeek API** — `deepseek-chat`
- Automatikus provider váltás hiba esetén

### Plugin

A `plugin.lua` egy Roblox Studio plugin, amely közvetlen kapcsolatot biztosít a szerver és a Roblox Studio között.

## 📁 Fájlszerkezet

```
RobloxAI/
├── server.py                    # Flask szerver (184 sor)
├── agent_roles.py               # AI ágens szerepkörök és promptok
├── plugin.lua                   # Roblox Studio plugin
├── project_memory.json          # Projekt memória
├── memory.json                  # Általános memória
├── test_connection.py           # Kapcsolat tesztelő
├── test_memory.py               # Memória teszt
├── test_integration.py          # Integrációs teszt
├── list_models.py               # Elérhető modellek listázása
├── check_models.js              # Modellek ellenőrzése (JS)
├── check_api.py                 # API ellenőrzés
├── requirements.txt             # Függőségek
├── .env                         # Környezeti változók (API kulcsok)
└── sessions/                    # Mentett munkamenetek
    ├── 1b81aebd.json
    ├── 2dffe64b.json
    └── de45239b.json
```

## 🚀 Használat

### Környezet beállítása

Hozz létre egy `.env` fájlt:

```env
GEMINI_API_KEY=your_gemini_api_key
DEEPSEEK_API_KEY=your_deepseek_api_key
AI_PROVIDER=deepseek
ROBLOX_PROJECT_PATH=./src
```

### Szerver indítása

```bash
# Függőségek telepítése
pip install -r requirements.txt

# Szerver indítása
python server.py
```

A szerver a `http://localhost:5000` címen indul.

### API végpontok

```bash
# Új játék projekt indítása
curl -X POST http://localhost:5000/create \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Készíts egy obby pályát checkpointokkal"}'

# Feladat státusz lekérdezése
curl http://localhost:5000/status/<job_id>

# Eredmény lekérése
curl http://localhost:5000/result/<job_id>
```

### Kapcsolat tesztelése

```bash
python test_connection.py
python check_api.py
```

### Roblox Studio plugin

1. Nyisd meg a Roblox Studio-t
2. Töltsd be a `plugin.lua` fájlt
3. Állítsd be a szerver URL-jét
4. Használd a plugin gombjait a játék generálásához

## 📦 Függőségek

```bash
pip install flask google-generativeai python-dotenv requests
```

- **Python 3.10+**
- **Flask** — web szerver
- **google-generativeai** — Gemini API kliens
- **python-dotenv** — környezeti változók
- **requests** — HTTP kliens (DeepSeek API)

## 🔄 Munkafolyamat

```
Felhasználó → "Készíts egy obby pályát"
    ↓
[MANAGER] Feladat elemzése
    ├── Pálya: obby stílus
    ├── Mechanika: checkpoint, respawn
    ├── Nehézség: közepes
    └── Eszközök: platformok, létrák
    ↓
[ARCHITECT] Játékterv készítése
    ├── Pályatérkép
    ├── Objektum lista
    └── Játékmenet flow
    ↓
[CODER] Lua kód generálása
    ├── Map generátor script
    ├── Checkpoint rendszer
    ├── Respawn logika
    └── Plugin parancsok
    ↓
Roblox Studio plugin futtatja a kódot
    ↓
KÉSZ JÁTÉK 🎮
```

## 🎯 Ágens szerepkörök

### Manager prompt (részlet)

```
Te egy tapasztalt játékfejlesztési projektmenedzser vagy.
Bontsd fel a feladatot részegységekre.
Határozd meg a szükséges komponenseket.
Priorizáld a feladatokat.
```

### Architect prompt (részlet)

```
Te egy Roblox játéktervező vagy.
Tervezd meg a pálya struktúráját.
Definiáld a játékmechanikákat.
Készíts részletes tervet a kódolónak.
```

### Coder prompt (részlet)

```
Te egy Roblox Lua fejlesztő vagy.
Generálj tiszta, működő Lua kódot.
Kövessd a Roblox best practice-eket.
Készíts moduláris, újrafelhasználható kódot.
```

## ⚙️ Konfiguráció

A `.env` fájl változói:

| Változó | Leírás | Alapértelmezett |
|---------|--------|-----------------|
| `GEMINI_API_KEY` | Google Gemini API kulcs | — |
| `DEEPSEEK_API_KEY` | DeepSeek API kulcs | — |
| `AI_PROVIDER` | AI szolgáltató (`gemini` / `deepseek`) | `deepseek` |
| `ROBLOX_PROJECT_PATH` | Generált fájlok helye | `./src` |
