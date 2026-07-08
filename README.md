# Ausbildungsnachweis

Eine einfache Anwendung zum Erfassen, Bearbeiten und Exportieren von Ausbildungsnachweisen bzw. Wochenberichten.

Das Projekt richtet sich ausdrücklich auch an Personen ohne Programmiererfahrung. Es kann entweder direkt mit Python gestartet oder als fertige Windows-EXE verteilt werden. Beim Start der Web-Anwendung öffnet sich die Bedienoberfläche automatisch im Standardbrowser.

---

## Inhaltsverzeichnis

- [Überblick](#überblick)
- [Features](#features)
- [Architekturidee](#architekturidee)
- [Designentscheidungen](#designentscheidungen)
- [Projektstruktur](#projektstruktur)
- [Installation und Voraussetzungen](#installation-und-voraussetzungen)
- [Konfiguration](#konfiguration)
- [Verwendung der Web-GUI](#verwendung-der-web-gui)
- [Verwendung der Windows-EXE](#verwendung-der-windows-exe)
- [CLI-Verwendung](#cli-verwendung)
- [DOCX- und PDF-Export](#docx--und-pdf-export)
- [Datenhaltung und wichtige Hinweise](#datenhaltung-und-wichtige-hinweise)
- [Technische Details](#technische-details)
- [Fehlerbehebung](#fehlerbehebung)
- [Für Entwicklerinnen und Entwickler](#für-entwicklerinnen-und-entwickler)
- [Lizenz](#lizenz)

---

## Überblick

**Ausbildungsnachweis** ist ein lokales Tool zum Führen eines einfachen Berichtshefts. Tagesberichte werden pro Datum gespeichert und können anschließend als Wochenübersicht angezeigt oder in eine Word-Vorlage übertragen werden.

Typischer Ablauf:

1. Anwendung starten.
2. Browser öffnet automatisch die lokale Weboberfläche.
3. Tagesberichte für Montag bis Freitag eintragen oder bearbeiten.
4. Woche prüfen.
5. Ausbildungsnachweis als PDF oder DOCX exportieren.

Die Anwendung läuft lokal auf dem eigenen Rechner. Es wird kein externer Server benötigt und die gespeicherten Inhalte bleiben in einer lokalen `data.json`-Datei.

---

## Features

- **Weboberfläche mit Flask**
  - Übersicht der aktuellen Arbeitswoche von Montag bis Freitag.
  - Vor- und Zurückblättern zwischen Wochen.
  - Einträge pro Datum erstellen, ändern und löschen.
  - Bestehende Einträge werden beim Bearbeiten automatisch wieder in das Formular geladen.

- **Automatischer Browserstart**
  - Beim Start von `python app.py` oder der EXE öffnet sich die Weboberfläche automatisch.
  - Falls das automatische Öffnen nicht klappt, kann die Seite manuell über `http://127.0.0.1:5000` geöffnet werden.

- **Lokale Speicherung**
  - Alle Einträge werden in `data.json` gespeichert.
  - Im normalen Python-Betrieb liegt `data.json` im Projektordner.
  - Im EXE-Betrieb liegt `data.json` neben der `.exe`, damit Daten dauerhaft erhalten bleiben.

- **Exportfunktion**
  - Export der gewählten Woche über eine Word-Vorlage `Vorlage.docx`.
  - Platzhalter in der Vorlage werden automatisch mit Name, Zeitraum und Tätigkeiten ersetzt.
  - Wenn LibreOffice verfügbar ist, wird zusätzlich bzw. bevorzugt eine PDF erzeugt.
  - Wenn keine PDF-Konvertierung möglich ist, wird eine DOCX-Datei ausgegeben.

- **Optionale CLI**
  - Zusätzlich zur Weboberfläche gibt es eine einfache Terminal-Anwendung in `main.py`.

- **Windows-EXE-Unterstützung**
  - Mit PyInstaller kann eine einzelne `Ausbildungsnachweis.exe` gebaut werden.
  - Ein Laie kann anschließend die EXE starten, ohne Python-Befehle eingeben zu müssen.

---

## Architekturidee

Die Anwendung ist bewusst klein und nachvollziehbar aufgebaut:

- `app.py` enthält die Flask-Webanwendung.
- `main.py` enthält eine einfache Kommandozeilenvariante.
- `templates/` enthält die HTML-Seiten der Weboberfläche.
- `static/` enthält CSS und statische Webdateien.
- `data.json` dient als einfache lokale Datenbank.
- `Vorlage.docx` ist optional und dient als Exportvorlage.

Die wichtigste Idee ist: **so wenig Installation und Bedienaufwand wie möglich**.

Für technisch unerfahrene Nutzende ist besonders die EXE-Variante gedacht. Die Weboberfläche läuft zwar technisch als lokaler Flask-Server, fühlt sich für den Nutzer aber wie ein normales lokales Programm an: EXE doppelklicken, Browser geht auf, Daten eintragen.

---

## Designentscheidungen

### Warum Flask?

Flask ist ein leichtgewichtiges Python-Webframework. Für dieses Projekt ist es passend, weil:

- die Anwendung lokal und klein bleibt,
- HTML-Formulare einfach umgesetzt werden können,
- keine große Frontend-Architektur notwendig ist,
- die Bedienung im Browser für Laien verständlicher ist als eine reine Terminal-App.

### Warum JSON statt Datenbank?

Für den aktuellen Zweck reicht eine `data.json` aus:

- keine zusätzliche Datenbankinstallation,
- leicht zu sichern und zu kopieren,
- für einfache Tagesberichte gut lesbar,
- geringe Einstiegshürde.

Für sehr viele Nutzer, parallele Bearbeitung oder komplexe Auswertungen wäre später eine Datenbank wie SQLite sinnvoll. Für die lokale Einzelplatznutzung ist JSON jedoch einfacher.

### Warum PyInstaller?

PyInstaller bündelt Python-Anwendung und Abhängigkeiten in eine ausführbare Datei. Dadurch muss die spätere nutzende Person nicht selbst Python, Flask oder docxtpl installieren. Das ist ideal, wenn die Anwendung an Personen weitergegeben wird, die nur eine Datei starten möchten.

### Warum öffnet sich ein Browser?

Die Anwendung nutzt den Browser als Oberfläche. Das bedeutet nicht, dass Daten ins Internet hochgeladen werden. Der Browser zeigt nur die lokal laufende Flask-Anwendung unter `127.0.0.1` an. Diese Adresse verweist auf den eigenen Computer.

---

## Projektstruktur

```text
Ausbildungsnachweis/
├── app.py                    # Flask-Webanwendung
├── main.py                   # Optionale CLI-Version
├── README.md                 # Projektdokumentation
├── LICENSE                   # Lizenzdatei
├── requirements.txt          # Laufzeitabhängigkeiten
├── requirements-build.txt    # Zusätzliche Build-Abhängigkeiten für PyInstaller
├── build_exe.bat             # Windows-Skript zum Erstellen der EXE
├── Ausbildungsnachweis.spec  # PyInstaller-Konfiguration
├── templates/                # HTML-Templates für Flask
│   ├── add.html
│   ├── base.html
│   ├── export.html
│   └── index.html
└── static/                   # Statische Dateien
    └── styles.css
```

Dateien, die zur Laufzeit entstehen oder optional daneben liegen können:

```text
data.json        # gespeicherte Tagesberichte
```

Bei der EXE-Variante liegt diese Datei typischerweise im gleichen Ordner wie `Ausbildungsnachweis.exe`.

---

## Installation und Voraussetzungen

Es gibt zwei Nutzungsarten:

1. **Empfohlen für Laien:** fertige Windows-EXE verwenden.
2. **Für Entwicklung oder Anpassungen:** Projekt mit Python starten.

### Variante A: Fertige EXE nutzen

Voraussetzungen für die nutzende Person:

- Windows-Rechner
- die Datei `Ausbildungsnachweis.exe`
- optional: LibreOffice, wenn direkt PDF-Dateien erzeugt werden sollen

Es muss normalerweise kein Python installiert werden, wenn die EXE bereits fertig gebaut wurde.

### Variante B: Mit Python starten

Voraussetzungen:

- Python 3.x
- pip
- Projektordner

Abhängigkeiten installieren:

```bash
python -m pip install -r requirements.txt
```

Weboberfläche starten:

```bash
python app.py
```

Danach öffnet sich automatisch der Browser.

---

## Konfiguration

Die Anwendung funktioniert ohne zusätzliche Konfiguration. Optional können einige Dinge angepasst werden.

### Host und Port

Standardmäßig startet die Weboberfläche auf:

```text
http://127.0.0.1:5000
```

Über Umgebungsvariablen kann das geändert werden:

```bash
FLASK_RUN_HOST=127.0.0.1 FLASK_RUN_PORT=5000 python app.py
```

Unter Windows PowerShell zum Beispiel:

```powershell
$env:FLASK_RUN_PORT = "5001"
python app.py
```

### Debug-Modus

Im normalen Python-Betrieb ist der Debug-Modus standardmäßig aktiv. In der EXE ist er automatisch deaktiviert.

Optional kann der Debug-Modus deaktiviert werden:

```bash
FLASK_DEBUG=0 python app.py
```

### Datenpfad

- Python-Betrieb: `data.json` im Projektordner.
- EXE-Betrieb: `data.json` neben `Ausbildungsnachweis.exe`.

Dieser Unterschied ist wichtig, weil eine PyInstaller-EXE interne Dateien temporär entpackt. Dauerhaft beschreibbare Nutzdaten müssen deshalb neben der EXE liegen.

### Vorlage für Export

Die Standardvorlage heißt:

```text
Vorlage.docx
```

Im Python-Betrieb wird sie im Projektordner erwartet.
---

## Verwendung der Web-GUI

### Start mit Python

Im Projektordner ausführen:

```bash
python app.py
```

Die Weboberfläche öffnet sich automatisch. Falls nicht, im Browser öffnen:

```text
http://127.0.0.1:5000
```

### Start über EXE

1. Ordner mit `Ausbildungsnachweis.exe` öffnen.
2. `Ausbildungsnachweis.exe` doppelklicken.
3. Kurz warten, bis sich der Browser öffnet.
4. Ausbildungsnachweis im Browser bearbeiten.

Wichtig: Das Konsolenfenster der EXE sollte offen bleiben, solange die Weboberfläche genutzt wird. Wird das Fenster geschlossen, wird auch der lokale Server beendet.

### Wochenübersicht

Auf der Startseite wird die ausgewählte Woche angezeigt. Die Anwendung zeigt Montag bis Freitag an.

Mögliche Aktionen:

- Eintrag für einen Tag öffnen.
- Zur vorherigen Woche wechseln.
- Zur nächsten Woche wechseln.
- Export für die angezeigte Woche starten.

### Eintrag hinzufügen oder bearbeiten

Ein Tagesbericht wird über ein Formular gepflegt:

1. Datum prüfen.
2. Tätigkeitstext eingeben oder vorhandenen Text ändern.
3. Speichern.

Wenn für das Datum bereits ein Eintrag existiert, wird er automatisch vorgeladen.

### Eintrag löschen

Im Bearbeitungsformular kann ein Eintrag gelöscht werden. Danach verschwindet er aus der Wochenübersicht und aus der `data.json`.

### Export starten

Über die Exportfunktion wird die aktuelle Woche vorbereitet. Dort können Angaben wie Name und Zeitraum geprüft werden. Anschließend wird die Vorlage gerendert und als PDF oder DOCX zurückgegeben.

---

## Verwendung der Windows-EXE

Die EXE ist für die einfache Weitergabe gedacht.

### EXE erstellen

Auf einem Windows-Rechner mit installiertem Python im Projektordner ausführen:

```bat
build_exe.bat
```

Das Skript installiert die benötigten Pakete und startet PyInstaller. Die fertige EXE liegt danach hier:

```text
dist\Ausbildungsnachweis.exe
```

### EXE verteilen

Für eine einfache Nutzung kann zum Beispiel dieser Ordner weitergegeben werden:

```text
Ausbildungsnachweis-Programm/
├── Ausbildungsnachweis.exe
├── data.json        # optional, falls vorhandene Daten mitgegeben werden sollen
```

Wenn noch keine `data.json` vorhanden ist, startet die Anwendung mit leeren Einträgen. Sobald Daten gespeichert werden, wird `data.json` neben der EXE angelegt.

### Vorhandene Daten in der EXE-Version nutzen

Wenn Einträge aus der Python-Version übernommen werden sollen:

1. Anwendung schließen.
2. `data.json` aus dem Projektordner kopieren.
3. Datei in den gleichen Ordner wie `Ausbildungsnachweis.exe` legen.
4. EXE erneut starten.

Die Daten sollten dann in der Weboberfläche erscheinen.

---

## CLI-Verwendung

Neben der Web-GUI gibt es eine einfache Terminalvariante:

```bash
python main.py
```

Die CLI bietet:

- Tagesbericht hinzufügen oder ändern,
- Tagesbericht anzeigen,
- Wochenübersicht im Terminal ausgeben,
- optional als Textdatei speichern.

Die CLI nutzt ebenfalls `data.json` im Projektordner. Für Laien ist die Weboberfläche oder EXE in der Regel komfortabler.

---

## DOCX- und PDF-Export

Für den DOCX-Export wird `docxtpl` verwendet. Die Datei `Vorlage.docx` muss passende Platzhalter enthalten.

### Unterstützte Platzhalter

```text
{{NAME}}
{{JAHR}}
{{DAT_STA}}
{{DAT_END}}
{{MO_TAETIGKEITEN}}
{{DI_TAETIGKEITEN}}
{{MI_TAETIGKEITEN}}
{{DO_TAETIGKEITEN}}
{{FR_TAETIGKEITEN}}
{{DAT_HEUTE}}
```

Bedeutung:

- `NAME`: eingegebener Name der auszubildenden Person
- `JAHR`: Jahr der ausgewählten Woche
- `DAT_STA`: Montag der Woche
- `DAT_END`: Freitag der Woche
- `MO_TAETIGKEITEN` bis `FR_TAETIGKEITEN`: gespeicherte Tätigkeiten
- `DAT_HEUTE`: aktuelles Datum beim Export

### PDF-Erzeugung

Für PDF wird LibreOffice im Headless-Modus verwendet. Wenn LibreOffice nicht gefunden wird oder die Konvertierung fehlschlägt, stellt die Anwendung stattdessen die DOCX-Datei bereit.

Das ist beabsichtigt, damit der Export nicht komplett scheitert, nur weil keine PDF-Konvertierung möglich ist.

---

## Datenhaltung und wichtige Hinweise

### Speicherformat

Die Datei `data.json` enthält die Berichte als Schlüssel-Wert-Struktur:

```json
{
  "2026-07-06": "Beispieltext für Montag",
  "2026-07-07": "Beispieltext für Dienstag"
}
```

Der Schlüssel ist immer ein Datum im Format `YYYY-MM-DD`.

### Datensicherung

Die wichtigsten Nutzdaten stecken in `data.json`. Für Backups reicht es meistens, diese Datei regelmäßig zu kopieren.

Empfohlen:

- vor Updates eine Kopie von `data.json` erstellen,
- bei EXE-Nutzung den gesamten Programmordner sichern,
- vor dem Löschen oder Verschieben der EXE prüfen, ob daneben eine `data.json` liegt.

### Mehrere Installationsorte

Wenn mehrere Kopien der EXE in unterschiedlichen Ordnern liegen, hat jede Kopie ihre eigene `data.json`. Das kann gewünscht sein, kann aber auch zu Verwirrung führen.

Beispiel:

```text
C:\Programme\Ausbildungsnachweis\data.json
C:\Users\Name\Desktop\Ausbildungsnachweis\data.json
```

Diese Dateien sind unabhängig voneinander.

---

## Technische Details

### Laufzeitabhängigkeiten

Siehe `requirements.txt`:

```text
Flask
docxtpl
```

### Build-Abhängigkeiten

Siehe `requirements-build.txt`:

```text
pyinstaller
```

### Flask-Routen

Die wichtigsten Routen sind:

- `GET /` – Wochenübersicht
- `GET /add` – Formular zum Hinzufügen oder Bearbeiten
- `POST /add` – Speichern oder Löschen eines Eintrags
- `GET /export` – Exportformular
- `POST /export` – DOCX/PDF erzeugen

### Ressourcen in der EXE

PyInstaller entpackt mitgelieferte Ressourcen intern in ein temporäres Verzeichnis. Deshalb unterscheidet die Anwendung zwischen:

- **Ressourcen**, die gelesen werden, zum Beispiel Templates und statische Dateien.
- **Schreibbaren Daten**, zum Beispiel `data.json`.

Schreibbare Daten werden im EXE-Betrieb neben der EXE abgelegt. Das verhindert, dass gespeicherte Einträge beim nächsten Start verschwinden.

### Browserstart

Die Anwendung nutzt Python `webbrowser`, um nach dem Serverstart automatisch die lokale URL zu öffnen. Im Debug-Betrieb wird berücksichtigt, dass Flask/Werkzeug den Prozess neu startet, damit der Browser nicht unnötig doppelt geöffnet wird.

---

## Fehlerbehebung

### Browser öffnet sich nicht automatisch

Manuell im Browser öffnen:

```text
http://127.0.0.1:5000
```

### In der EXE sind keine vorhandenen Daten sichtbar

Prüfen:

1. Liegt `data.json` im gleichen Ordner wie `Ausbildungsnachweis.exe`?
2. Wurde vielleicht eine andere EXE-Kopie in einem anderen Ordner gestartet?
3. Ist die Datei gültiges JSON?
4. Wurde die Anwendung nach dem Kopieren der Datei neu gestartet?

### Export findet die Vorlage nicht

Prüfen:

- Heißt die Datei exakt `Vorlage.docx`?
- Liegt sie im Projektordner?
- Enthält sie die benötigten Platzhalter?

### PDF wird nicht erstellt

Wahrscheinliche Ursache: LibreOffice ist nicht installiert oder wird nicht im Systempfad gefunden.

Lösung:

- LibreOffice installieren, oder
- die ausgegebene DOCX-Datei manuell in Word/LibreOffice als PDF speichern.

### Port 5000 ist bereits belegt

Einen anderen Port verwenden:

```bash
FLASK_RUN_PORT=5001 python app.py
```

Dann im Browser öffnen:

```text
http://127.0.0.1:5001
```

---

## Für Entwicklerinnen und Entwickler

### Abhängigkeiten installieren

```bash
python -m pip install -r requirements.txt
```

### Anwendung starten

```bash
python app.py
```

### Syntax prüfen

```bash
python -m compileall app.py main.py
```

### PyInstaller-Spec prüfen

```bash
python -m py_compile Ausbildungsnachweis.spec
```

### EXE bauen

Unter Windows:

```bat
build_exe.bat
```

Oder manuell:

```bash
python -m pip install -r requirements.txt -r requirements-build.txt
python -m PyInstaller Ausbildungsnachweis.spec
```

---

## Lizenz

Dieses Projekt enthält eine `LICENSE`-Datei. Bitte die dort genannten Lizenzbedingungen beachten.

---

## Kurzfassung für Laien

Wenn du eine fertige EXE bekommen hast:

1. `Ausbildungsnachweis.exe` doppelklicken.
2. Warten, bis der Browser aufgeht.
3. Einträge ausfüllen und speichern.
4. Für den Export optional `Vorlage.docx` neben die EXE legen.
5. Wichtig: `data.json` nicht löschen, denn darin stehen deine gespeicherten Berichte.
