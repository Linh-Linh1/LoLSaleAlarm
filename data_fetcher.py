import requests
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
    if not version: return []
    print(f"Lade alle Champion-Daten für Version {version}...")
    champions_url = f"http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/championFull.json"
    try:
        response = requests.get(champions_url)
        response.raise_for_status()
        all_champions_data = response.json()
        champions = all_champions_data.get('data', {})
        if not champions: return []
        skin_list = []
        for champion_key, champion_details in champions.items():
            skins_for_champion = champion_details.get('skins', [])
            for skin_info in skins_for_champion:
                if skin_info.get('num', -1) == 0: continue
                skin_name = skin_info.get('name', 'Unbekannter Skin')
                skin_list.append(skin_name)
        print(f"Erfolgreich {len(skin_list)} Skins extrahiert (ohne klassische Skins).")
        return sorted(skin_list)
    except (requests.exceptions.RequestException, KeyError, TypeError) as e:
        print(f"Fehler beim Abrufen oder Analysieren der Skin-Daten: {e}")
        return []

def get_weekly_sales():
    sales_url = "https://turbosmurfs.gg/lol-weekly-sale"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    try:
        response = requests.get(sales_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        sales_container = soup.find('div', class_='container-new')
        if not sales_container: return []
        skin_elements = sales_container.find_all('a', style=lambda value: value and 'font-weight:700' in value)
        sale_skin_list = [skin.get_text(strip=True) for skin in skin_elements]
        if sale_skin_list: print(f"\n{len(sale_skin_list)} Skins im Angebot     ", end='')
        else: print("Warnung: Sales-Container gefunden, aber keine Skin-Namen darin.")
        return sale_skin_list
    except requests.exceptions.RequestException as e:
        print(f"Fehler: Konnte die Sales-Webseite nicht erreichen. {e}")
        return []

def get_wished_skins():
    try:
        with open('wished_skins.txt', 'r', encoding='utf-8') as f:
            wished_list = [line.strip() for line in f if line.strip()]
            print(f"{len(wished_list)} Skins in Wunschliste")
            return wished_list
    except FileNotFoundError:
        print("Info: 'wished_skins.txt' nicht gefunden. Erstelle eine, um deine Wunsch-Skins einzutragen.")
        return []

def find_matches(sales_list, wished_list):
    print("Suche Matches...", end='')
    sales_set = set(sales_list)
    wished_set = set(wished_list)
    matches = sales_set & wished_set
    return list(matches)