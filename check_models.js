
const https = require('https');

const API_KEY = 'AIzaSyC2pKz7wcVXJQ6hTjnE-Pc1waump7kyKdo';
const url = `https://generativelanguage.googleapis.com/v1beta/models?key=${API_KEY}`;

console.log("Lekérdezés indítása...");

https.get(url, (res) => {
    let data = '';

    res.on('data', (chunk) => {
        data += chunk;
    });

    res.on('end', () => {
        try {
            const response = JSON.parse(data);
            if (response.error) {
                console.error("API HIBA:", response.error.message);
                return;
            }

            console.log("\n--- ELÉRHETŐ GENERATÍV MODELLEK ---");
            const models = response.models || [];
            let found = 0;

            models.forEach(m => {
                // Csak azokat listázzuk, amik tudnak szöveget generálni
                if (m.supportedGenerationMethods.includes('generateContent')) {
                    const shortName = m.name.replace('models/', '');
                    console.log(`ID: ${shortName.padEnd(30)} | Név: ${m.displayName}`);
                    found++;
                }
            });

            if (found === 0) console.log("Nem található kompatibilis modell.");
            console.log("-----------------------------------\n");
            
        } catch (e) {
            console.error("JSON feldolgozási hiba:", e.message);
        }
    });

}).on("error", (err) => {
    console.error("Hálózati hiba: " + err.message);
});