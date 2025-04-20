import json
from datetime import datetime
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "data" / "schedule.json"

def load_config():
    """Charge la configuration depuis le fichier JSON"""
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Fichier de configuration introuvable : {CONFIG_PATH}")
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(config):
    """Sauvegarde la configuration dans le fichier JSON"""
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def get_today_schedule(config):
    """Retourne les horaires (on/off) du jour courant"""
    day = datetime.now().strftime("%A").lower()
    return config["days"].get(day)

def is_manual_mode(config):
    """Vérifie si on est en mode manuel"""
    mode = config.get("mode", "auto")
    override = config.get("manual_override", {})
    if override.get("active"):
        until = override.get("until")
        if until:
            try:
                until_dt = datetime.fromisoformat(until)
                if datetime.now() < until_dt:
                    return True
                else:
                    override["active"] = False
                    override["until"] = None
                    save_config(config)
            except Exception:
                pass
    return mode == "manual"