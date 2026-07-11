import requests
import os

# Megpróbáljuk a .env-ből kiszedni a kulcsot, ha már ott van
api_key = "AIzaSyC2pKz7wcVXJQ6hTjnE-Pc1waump7kyKdo" 

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

try:
    response = requests.get(url)
    if response.status_code == 200:
        models = response.json()
        for m in models.get('models', []):
            print(f"Modell: {m['name']} | Leírás: {m['description']}")
    else:
        print(f"Hiba: {response.status_code}")
        print(response.text)
except Exception as e:
    print(e)