# Ausbildungsnachweis (CLI + Flask)

Diese Anwendung ist ein einfaches Python-Tool zur Erstellung eines Ausbildungsnachweises
nach dem Vorbild der IHK-Berichtshefte. Sie enthält eine **CLI-Variante** (Terminal) und eine
**Flask-Weboberfläche** für die tägliche Pflege.

Ziel der Anwendung ist es, tägliche Tätigkeiten schnell und unkompliziert zu erfassen, bestehende Einträge
zu bearbeiten oder zu löschen und am Ende der Woche übersichtlich auszugeben, sodass die Inhalte problemlos
in ein offizielles Berichtsheft übertragen werden können.

---

## Funktionen (Überblick)

- Erfassen, **Bearbeiten** und **Löschen** von Tagesberichten (pro Datum)
- Anzeigen einzelner Tagesberichte (CLI)
- **Wochenausgabe (Montag–Freitag)** in übersichtlicher Textform
- Optionaler **Export als Textdatei (.txt)**
- Lokale Speicherung der Daten in einer JSON-Datei
- Weboberfläche mit vorbefülltem Formular für vorhandene Einträge
- Blättern zwischen Wochen in der Weboberfläche (vor/zurück)
- Export als DOCX/PDF über eine IHK-Vorlage (Platzhalter in der DOCX)

---

## Motivation

In der Maßnahme bzw. Ausbildung wird regelmäßig ein Ausbildungsnachweis geführt.
Diese Anwendung soll den Schreibaufwand reduzieren und dabei helfen, Inhalte strukturiert,
nachvollziehbar und konsistent festzuhalten.

Die Anwendung ist bewusst einfach gehalten und richtet sich an Einsteiger im Bereich Python
sowie an Auszubildende im IT-Bereich (z.B. Fachinformatiker/in für Systemintegration).

---

## Voraussetzungen

- Python 3.x
- Terminal / Kommandozeile (für CLI)
- Flask (für Weboberfläche)
- Optional: docxtpl (für DOCX-Generierung)
- Optional: LibreOffice (für PDF-Export aus DOCX)

---

## Start der Anwendung

### CLI (Terminal)

Im Projektordner ausführen:

```bash
python main.py
```

### Flask-Weboberfläche

1. Flask installieren:

```bash
pip install flask
```

2. Optional für DOCX/PDF-Export installieren:

```bash
pip install docxtpl
```

3. Server starten:

```bash
python app.py
```

4. Im Browser öffnen:

```
http://localhost:5000
```

---

## Datenhaltung

Alle Einträge werden lokal in `data.json` gespeichert und von CLI sowie Weboberfläche gemeinsam genutzt.

---

## Weboberfläche (UI)

- Zentrales Layout in `templates/base.html`
- Stylesheet in `static/styles.css` (inkl. Dark Mode über `prefers-color-scheme`)
- Export-Ansicht enthält Print-Styles (Navigation/Buttons werden beim Drucken ausgeblendet)

---

## DOCX/PDF-Export (IHK-Vorlage)

Die Weboberfläche bietet einen Export-Button. Im Export-Dialog kannst du deinen Namen,
das Ausbildungsjahr und die Woche prüfen, bevor die Datei erstellt wird. Die DOCX-Vorlage
heißt `Vorlage.docx` und muss die folgenden Platzhalter enthalten:

- `{{NAME}}`
- `{{JAHR}}`
- `{{DAT_STA}}`
- `{{DAT_END}}`
- `{{MO_TAETIGKEITEN}}`
- `{{DI_TAETIGKEITEN}}`
- `{{MI_TAETIGKEITEN}}`
- `{{DO_TAETIGKEITEN}}`
- `{{FR_TAETIGKEITEN}}`
- `{{DAT_HEUTE}}`

Für den PDF-Export wird LibreOffice im Headless-Modus verwendet. Falls LibreOffice nicht
vorhanden ist, liefert die Anwendung stattdessen die DOCX-Datei zurück.