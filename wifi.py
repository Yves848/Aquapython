import network
import time
from storage import charger_config

config = charger_config()

def connect_wifi(ssids, password):
    print(ssids)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    ip = config["IP"]
    netmask = '255.255.255.0'
    gateway = '192.168.50.1'
    dns = '8.8.8.8'  # Optionnel, peut être le même que la gateway

    wlan.ifconfig((ip, netmask, gateway, dns))

    # Connexion au réseau Wi-Fi
    print("Connexion au Wi-Fi...")
    for ssid in ssids:
        wlan.connect(ssid, password)
        status = wlan.status()
        print(f"connected : {wlan.isconnected()} - {status}")
        timeout = 10  # secondes
        start = time.time()
        while not wlan.isconnected():
            print(f"Test de connexion sur {ssid}")
            if time.time() - start > timeout:
                print("⛔️ Échec de connexion.")
                return None
            time.sleep(1)
        if wlan.isconnected():
            print(f"SSID : {ssid}")
            print("✅ Connecté à", wlan.ifconfig()[0])
            return wlan
    return None 