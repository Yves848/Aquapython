from microdot import Microdot, Response
from wifi import connect_wifi
from storage import charger_etat, sauver_etat
import machine
import neopixel
import time
import uasyncio as asyncio
from machine import Pin

# Configuration LED RGB (par ex. broche 48, 1 LED)
LED_PIN = 48
np = neopixel.NeoPixel(machine.Pin(LED_PIN), 1)

# Stockage état
etat = charger_etat()
relais = {}
relais[0] = Pin(9, Pin.OUT)
relais[1] = Pin(10, Pin.OUT)
relais[2] = Pin(11, Pin.OUT)
relais[3] = Pin(12, Pin.OUT)
delais = etat["interval"] # récupérer le délais dans le fichier json.  Par défaut, il est initialisé à 300
print(f"Délais entre lampe : {delais} secondes")
# Animation non-bloquante
async def animate_led(from_color, to_color, duration=1.0):
    steps = 20
    delay = duration / steps
    for i in range(steps):
        r = int(from_color[0] + (to_color[0] - from_color[0]) * i / steps)
        g = int(from_color[1] + (to_color[1] - from_color[1]) * i / steps)
        b = int(from_color[2] + (to_color[2] - from_color[2]) * i / steps)
        np[0] = (r, g, b)
        np.write()
        await asyncio.sleep(delay)
    np[0] = (0, 0, 0)  # Éteint après animation
    np.write()

# Microdot setup
app = Microdot()
Response.default_content_type = 'application/json'

@app.post('/day')
async def handle_day(request):
    print("[/day] Reçu !")
    etat["state"] = "day"
    #etat["Delais"] = delais
    print(f"Délais : {delais}")
    for c in range(4):
        relais[c].value(1)
        await asyncio.sleep(delais)
    sauver_etat(etat)
    asyncio.create_task(animate_led((0, 0, 255), (255, 255, 0), 2.0))  # bleu → jaune
    return {"message": "Day mode activé."}

@app.post('/night')
async def handle_night(request):
    print("[/night] Reçu !")
    etat["state"] = "night"
    #etat["Night"] = "On"
    #etat["Delais"] = delais
    print(f"Délais : {delais}")
    
    for c in range(4):
        relais[c].value(0)
        await asyncio.sleep(delais)
    sauver_etat(etat)
    asyncio.create_task(animate_led((255, 255, 0), (0, 0, 50), 2.0))  # jaune → bleu foncé
    return {"message": "Night mode activé."}

@app.get('/data')
def handle_data(request):
    print("[/data] Requête reçue")
    etat_actuel = charger_etat()
    asyncio.create_task(animate_led((0, 255, 0), (0, 50, 0), 0.5))  # flash vert
    return etat

@app.post('/delay')
async def handle_delay(request):
    print("[/delay] Reçu !")
    data = request.json
    if data is None:
        return "Invalid or missing json",400
    
    print(data)
    global delais
    delais = int(data.get('delais'))
    etat["interval"] = delais
    sauver_etat(etat)
    return f"Délais entre lampes fixé à {delais} secondes."

@app.get('/endpoints')
async def handle_endpoints(request):
    print("[/endpoints] Reçu !")
    # asyncio.create_task(animate_led((255, , 0), (127, 0, 0), 0.5))  # flash vert
    asyncio.create_task(animate_led((0, 255, 0), (0, 50, 0), 0.5))  # flash vert
    return {"endpoints":["/data","/day","/night","/delay"]}
         
# Lancement
def main():
    connect_wifi("continentalcircus", "the a la menthe")
    app.run(host="0.0.0.0", port=80)

# Lancer le tout
main()