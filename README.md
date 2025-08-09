# LoL Sale Alarm

Ein anpassbares Desktop-Tool, das die wöchentlichen Skin-Sales des bekannten Online-Spiels League of Legends überwacht und per Desktop-Benachrichtigung informiert, sobald ein Skin von der Wunschliste im Angebot ist.

## Projektübersicht

Als ehemaliger LoL-Spieler habe ich oft die wöchentlichen Skin-Sales verpasst, weil das manuelle Überprüfen der Angebote umständlich und leicht zu vergessen ist. Um dieses Problem zu lösen, habe ich den "LoL Sale Alarm" entwickelt.

Dieses Projekt ist eine Desktop-Anwendung, die diesen Prozess vollständig automatisiert. Sie ermöglicht es, eine persönliche Wunschliste von LoL-Skins zu verwalten, prüft im Hintergrund mit einem seperaten Python-Skript automatisch die wöchentlichen Angebote (einmalig/täglich/wöchentlich/monatlich) und gleicht sie mit der Wunschliste ab. Bei einer Übereinstimmung wird eine native Desktop-Benachrichtigung ausgelöst, sodass man nie wieder einen Sale verpasst und keinen Aufwand betreiben muss.

## Bestandteile des kleinen Projektes

*   **API-Interaktion:** Python (`requests`) zur Abfrage der offiziellen Riot-Daten
*   **Web Scraping:** `BeautifulSoup4` zum Extrahieren von Daten von Webseiten
*   **GUI-Entwicklung:** `Tkinter` zur Erstellung der GUI
*   **Automatisierung** von Skripten mit der Windows-Aufgabenplanung

## Features

- **Grafische Konfiguration:** Es wird eine GUI zur Verwaltung der Wunschliste verwendet.
- **Vollständige Skin-Datenbank:** Nutzt die offizielle Riot DDragon API, um immer alle verfügbaren Skins anzuzeigen.
- **Interaktive Auswahl:** Skins können in der GUI einfach durchsucht, gefiltert und per Klick ausgewählt oder abgewählt werden.
    - **Alternativ:** Skinnamen selber in eine .txt schreiben.                                          
- **Persistente Wunschliste:** Deine Auswahl wird lokal in einer Textdatei gespeichert.
- **Automatischer Abgleich:** Ein separates Checker-Skript übernimmt die wöchentliche Überprüfung.
- **Desktop-Benachrichtigungen:** Man wird sofort informiert, wenn ein gewünschter Skin im Angebot ist.

## 📁 Projektstruktur
```
LoLSaleAlarm/
├── .venv/
├── main.py
├── gui.py
├── data_fetcher.py
├── checker.py
├── wished_skins.txt
└── README.md
```

##  Funktionsweise

1.  **Konfiguration:** Der Nutzer startet `main.py`, um die GUI zu öffnen. In der GUI werden alle existierenden Skins über die DDragon API geladen und angezeigt.
2.  **Wunschliste:** Der Nutzer wählt seine gewünschten Skins aus und klickt auf "Speichern & Schließen". Die Auswahl wird in `wished_skins.txt` geschrieben.
3.  **Automatischer Check:** Ein geplanter Task (z.B. wöchentlich) führt das `checker.py`-Skript aus.
3.b **Manueller Check:** Nutzer startet `checker.py` manuell (PShell: python checker.py)
4.  **Datenabruf:** Das Skript ruft die aktuellen Sales von einer Community-Webseite ab und liest die `wished_skins.txt` ein.
5.  **Abgleich:** Die beiden Listen werden verglichen.
6.  **Benachrichtigung:** Bei einer Übereinstimmung wird eine Desktop-Benachrichtigung über `plyer` ausgelöst.

## Einrichtung des Projektes

1.  **Projekt klonen**
2.  **Projekt in einer IDE (z.B. VSCode) öffnen**

3.  **Virtuelle Umgebung erstellen und aktivieren :**
    ```bash
    # Erstellen
    python -m venv .venv

    # Aktivieren (Windows PowerShell)
    .\.venv\Scripts\Activate.ps1
    ```

4.  **Abhängigkeiten installieren:**
    ```bash
    pip install requests
    pip install beautifulsoup4
    pip install plyer
    ```
    *(requests: API-Anfragen, beautifulsoup4: Parsen des HTML-Codes, plyer: Desktop-Benachrichtigungen)*

5.  **Gui starten, um die Wunschliste zu konfigurieren:**
    ```bash
    python main.py
    ```

6.  **Automatisierung einrichten**, durch Folgen der Anweisungen im Abschnitt `Automatisierung`.

7. **Optional: Manuelles Überprüfen von Skin-Matches (mit Benachrichtigung)**
    ```bash
    python checker.py
    ```


## ⚙️Automatisierung

Um das Skript automatisch in regelmäßigen Abständen (z.B. wöchentlich) auszuführen, wird eine geplante Aufgabe eingerichtet.

**Für Windows (Aufgabenplanung):**
1.  "Windows-Aufgabenplanung" öffnen.
2.  Option "Aufgabe erstellen..." auswählen.
3.  **Trigger:** Einen neuen Trigger erstellen, der z.B. "wöchentlich" ausgeführt wird.
4.  **Aktionen:** Eine neue Aktion vom Typ "Programm starten" erstellen und wie folgt konfigurieren:
    *   **Programm/Skript:** Der **vollständige Pfad** zur `python.exe` innerhalb der virtuellen Umgebung (z.B. `C:\Projekte\LoLSaleAlarm\.venv\Scripts\python.exe`).
    *   **Argumente hinzufügen:** Der **vollständige Pfad** zum `checker.py`-Skript (z.B. `C:\Projekte\LoLSaleAlarm\checker.py`).
    *   **Starten in:** Der **vollständige Pfad** zum Projektordner (z.B. `C:\Projekte\LoLSaleAlarm`). **Dieser Schritt ist entscheidend für die korrekte Ausführung.**

## Mögliche Ideen für Erweiterungen
- **Grafische Auswahl:** Ersetzen der Textliste durch eine visuelle Ansicht mit Champion-Splasharts. Beim Klicken auf diese folgen Skin-Splasharts des Champions die zur Auswahl stehen.
- **Zusätzliche Benachrichtigungen:** Implementierung weiterer Benachrichtigungsmethoden wie E-Mail oder Discord-Webhooks.
- **Standalone-Anwendung:** Verpacken des Projekts als eigenständige `.exe`-Datei mittels PyInstaller für eine einfachere Verteilung.
- **Caching:** Lokales Speichern der Skin-Datenbank, um die Ladezeit der GUI zu verkürzen und die Anzahl der API-Anfragen zu reduzieren.

## Autor
- Thanh Pham
