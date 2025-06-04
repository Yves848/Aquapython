import ujson
import os

FICHIER_ETAT = 'etat.json'

def charger_etat():
    if FICHIER_ETAT in os.listdir():
        with open(FICHIER_ETAT, 'r') as f:
            return ujson.load(f)
    return {"state": "day", "interval" : 300}

def sauver_etat(etat):
    with open(FICHIER_ETAT, 'w') as f:
        ujson.dump(etat, f)