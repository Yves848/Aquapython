import ujson
import os

FICHIER_ETAT = 'etat.json'
FICHIER_CONFIG = 'config.json'

def charger_etat():
    if FICHIER_ETAT in os.listdir():
        with open(FICHIER_ETAT, 'r') as f:
            return ujson.load(f)
    return {"state": "day", "interval" : 3}

def sauver_etat(etat):
    with open(FICHIER_ETAT, 'w') as f:
        ujson.dump(etat, f)
        
def charger_config():
    if FICHIER_CONFIG in os.listdir():
        with open(FICHIER_CONFIG,'r') as f:
            return ujson.load(f)
    return {"PIN1": 27, "PIN2": 26, "PIN3": 25, "PIN4": 33, "LED_PIN": 2}