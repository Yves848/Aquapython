import network
import time

def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    ip = '192.168.50.202'
    netmask = '255.255.255.0'
    gateway = '192.168.50.1'
    dns = '8.8.8.8'  # Optionnel, peut être le même que la gateway

    wlan.ifconfig((ip, netmask, gateway, dns))

    # Connexion au réseau Wi-Fi

    wlan.connect(ssid, password)

    print("Connexion au Wi-Fi...")
    timeout = 10  # secondes
    start = time.time()
    while not wlan.isconnected():
        if time.time() - start > timeout:
            print("⛔️ Échec de connexion.")
            return None
        time.sleep(1)

    print("✅ Connecté à", wlan.ifconfig()[0])
    return wlan