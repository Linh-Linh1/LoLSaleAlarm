# main.py

import requests
import json

def get_latest_ddragon_version():
    print("Suche nach der neuesten DDragon-Version...")
    versions_url = "https://ddragon.leagueoflegends.com/api/versions.json"
    
    try:
        response = requests.get(versions_url)
        response.raise_for_status()
        versions = response.json()
        latest_version = versions[0]
        print(f"Neueste Version gefunden: {latest_version}")
        return latest_version
        
    except requests.exceptions.RequestException as e:
        print(f"Fehler: Konnte die DDragon-Versionen nicht abrufen. {e}")
        return None

def get_all_skins(version):
    if not version:
        print("Fehler: Keine Version angegeben, kann Skins nicht abrufen.")
        return []

    print(f"Lade alle Champion-Daten für Version {version}...")
    
    champions_url = f"http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/championFull.json"
    
    try:
        response = requests.get(champions_url)
        response.raise_for_status()
        
        all_champions_data = response.json()
        champions = all_champions_data.get('data', {})
        
        if not champions:
            print("Fehler: Das 'data'-Feld im JSON war leer oder nicht vorhanden.")
            return []

        skin_list = []
        
        for champion_key, champion_details in champions.items():
            champion_name = champion_details.get('name', 'Unbekannter Champion')
            skins_for_champion = champion_details.get('skins', [])
            
            for skin_info in skins_for_champion:
                if skin_info.get('num', -1) == 0:
                    continue
                
                skin_name = skin_info.get('name', 'Unbekannter Skin')
                skin_list.append(skin_name)
                    
        print(f"Erfolgreich {len(skin_list)} Skins extrahiert (ohne klassische Skins).")
        return sorted(skin_list)
        
    except requests.exceptions.RequestException as e:
        print(f"Fehler: Konnte die Champion-Daten nicht abrufen. {e}")
        return []
    except (KeyError, TypeError) as e:
        print(f"Fehler beim Analysieren der Daten: {e}. Möglicherweise unerwartetes JSON-Format.")
        return []

if __name__ == "__main__":
    print("--- LoL Skin Sale Alarm ---")
    print("Schritt 1.1: Rufe alle existierenden Skins ab...")
    
    latest_version = get_latest_ddragon_version()
    
    if latest_version:
        all_skins = get_all_skins(latest_version)
        
        if all_skins:
            print(f"\nEs wurden {len(all_skins)} Skins gefunden. Hier ist eine Beispielausgabe:")
            
            print("\nDie ersten 50 Skins:")
            for skin in all_skins[:50]:
                print(f"- {skin}")
            
            print("\n...")
            
            print("\nDie letzten 50 Skins:")
            for skin in all_skins[-50:]:
                print(f"- {skin}")
        else:
            print("Konnte keine Skins abrufen.")
    else:
        print("Das Skript wird beendet, da keine DDragon-Version gefunden wurde.")