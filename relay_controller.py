import requests

ESP32_BASE_URL = "http://192.168.50.202"  # à adapter à ton réseau

def send_command(endpoint):
    """Envoie une commande simple à l’ESP32 (ex: /day ou /night)"""
    url = f"{ESP32_BASE_URL}{endpoint}"
    try:
        response = requests.post(url, timeout=3)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"[ERREUR] Commande {endpoint} échouée : {e}")
        return False

def get_status():
    """Récupère l’état courant via /data"""
    try:
        response = requests.get(f"{ESP32_BASE_URL}/data", timeout=3)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"[ERREUR] Impossible d’interroger /data : {e}")
        return None