import time
from datetime import datetime
from config import load_config, get_today_schedule, is_manual_mode
from relay_controller import get_status, send_command

CHECK_INTERVAL = 60  # secondes

def main_loop():
    print("🐠 Démarrage du service d’éclairage...")

    while True:
        config = load_config()

        if is_manual_mode(config):
            print("[MODE] Manuel actif — aucune action.")
        else:
            now = datetime.now()
            now_str = now.strftime("%H:%M")

            schedule = get_today_schedule(config)
            print(schedule)
            if not schedule:
                print(f"[ERREUR] Aucun horaire trouvé pour aujourd’hui.")
            else:
                current_status = get_status()
                print(current_status)
                if current_status:
                    light_status = current_status.get("Day")
                    print(f"Light Status : {light_status}")
                    if now_str >= schedule["on"] and light_status != "On":
                        print(f"[ACTION] Allumage programmé ({now_str})")
                        send_command("/day")

                    elif now_str >= schedule["off"] and light_status != "Off":
                        print(f"[ACTION] Extinction programmée ({now_str})")
                        send_command("/night")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main_loop()