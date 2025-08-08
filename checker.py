from data_fetcher import get_weekly_sales, get_wished_skins, find_matches
from plyer import notification

def run_check():
    print("----- Starte wöchentlichen Skinsale-Check -----")
    
    sale_skins = get_weekly_sales()
    wished_skins = get_wished_skins()

    if sale_skins and wished_skins:
        found_matches = find_matches(sale_skins, wished_skins)
        
        if found_matches:
            print("\n------------------- TREFFER -------------------")

            title = "LoL Skin Sale Alarm: Treffer!"
            message = "Im Angebot:\n" + "\n".join(found_matches)
            
            print(message)
            
            try:
                #Benachrichtigung
                notification.notify(
                    title=title,
                    message=message,
                    app_name="LoL Skin Sale Alarm",
                    timeout=10
                )
                print("Desktop-Benachrichtigung gesendet.")
            except Exception as e:
                print(f"Fehler beim Senden der Desktop-Benachrichtigung: {e}")

        else:
            print("\nKein Skin im Angebot.")
    else:
        print("\nEntweder Skinliste oder Salesliste leer")

    print("------------- Check abgeschlossen -------------")

if __name__ == "__main__":
    run_check()