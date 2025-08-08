# main.py

import requests
import json
from bs4 import BeautifulSoup

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
        return []
    print(f"Lade alle Champion-Daten für Version {version}...")
    champions_url = f"http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/championFull.json"
    try:
        response = requests.get(champions_url)
        response.raise_for_status()
        all_champions_data = response.json()
        champions = all_champions_data.get('data', {})
        if not champions:
            return []
        skin_list = []
        for champion_key, champion_details in champions.items():
            skins_for_champion = champion_details.get('skins', [])
            for skin_info in skins_for_champion:
                if skin_info.get('num', -1) == 0:
                    continue
                skin_name = skin_info.get('name', 'Unbekannter Skin')
                skin_list.append(skin_name)
        print(f"Erfolgreich {len(skin_list)} Skins extrahiert (ohne klassische Skins).")
        return sorted(skin_list)
    except (requests.exceptions.RequestException, KeyError, TypeError) as e:
        print(f"Fehler beim Abrufen oder Analysieren der Skin-Daten: {e}")
        return []

def get_weekly_sales():
    print("\nSuche nach wöchentlichen Skin-Sales...")
    sales_url = "https://turbosmurfs.gg/lol-weekly-sale"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(sales_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        sales_container = soup.find('div', class_='container-new')
        if not sales_container:
            print("Fehler: Konnte den Haupt-Sales-Container ('container-new') nicht finden.")
            return []
        skin_elements = sales_container.find_all('a', style=lambda value: value and 'font-weight:700' in value)
        sale_skin_list = [skin.get_text(strip=True) for skin in skin_elements]
        if sale_skin_list:
            print(f"Erfolgreich {len(sale_skin_list)} Items im Angebot gefunden.")
        else:
            print("Warnung: Sales-Container gefunden, aber keine Skin-Namen darin.")
        return sale_skin_list
    except requests.exceptions.RequestException as e:
        print(f"Fehler: Konnte die Sales-Webseite nicht erreichen. {e}")
        return []

if __name__ == "__main__":
    print("--- LoL Skin Sale Alarm ---")
    
    print("\nSchritt 1.1: Rufe alle existierenden Skins ab...")
    latest_version = get_latest_ddragon_version()
    if latest_version:
        all_skins = get_all_skins(latest_version)
        if all_skins:
            print(f"-> {len(all_skins)} Skins in der Datenbank.")
        else:
            print("-> Konnte keine Skins abrufen.")
            
    print("\nSchritt 1.2: Rufe aktuelle Sales ab...")
    sale_skins = get_weekly_sales()
    if sale_skins:
        print("\n--- Aktuell im Angebot ---")
        for skin in sale_skins:
            print(f"- {skin}")
    else:
        print("-> Konnte keine aktuellen Sales finden.")