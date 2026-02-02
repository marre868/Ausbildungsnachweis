import json
import os
from datetime import date, datetime, timedelta

DATA_FILE = "data.json"

def load_data() -> dict:
    if not os.path.exists(DATA_FILE):
        save_data({})
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            save_data({})
            return {}
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            print("Warnung: data.json ist ungültig. Starte mit leeren Daten.")
            save_data({})
            return {}

def save_data(data: dict) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def parse_date(s: str) -> str:
    """
    Accepts: YYYY-MM-DD or 'today'/'heute'
    Returns: ISO date string YYYY-MM-DD
    """
    s = s.strip().lower()
    if s in ("today", "heute"):
        return date.today().isoformat()
    # valid format check
    datetime.strptime(s, "%Y-%m-%d")
    return s

def monday_of_week(d: date) -> date:
    return d - timedelta(days=d.weekday())  # weekday: Mon=0

def week_dates(d: date):
    mon = monday_of_week(d)
    return [mon + timedelta(days=i) for i in range(7)]

def add_entry(data: dict):
    raw = input("Datum (YYYY-MM-DD oder 'heute'): ").strip()
    day = parse_date(raw)

    existing = data.get(day, "").strip()
    if existing:
        print("Vorhandener Eintrag:")
        print("-" * 60)
        print(existing)
        print("-" * 60)

    print("Schreibe deinen Tagesbericht. Leere Zeile = fertig.")
    lines = []
    while True:
        line = input("> ")
        if line.strip() == "":
            break
        lines.append(line)

    text = "\n".join(lines).strip()
    if not text:
        print("Kein Text eingegeben – abgebrochen.")
        return

    if existing:
        data[day] = f"{existing}\n{text}"
    else:
        data[day] = text
    save_data(data)
    print(f"Gespeichert für {day} ✅")

def show_day(data: dict):
    day = parse_date(input("Datum (YYYY-MM-DD oder 'heute'): ").strip())
    print("\n" + "=" * 60)
    print(f"Tagesnachweis: {day}")
    print("-" * 60)
    print(data.get(day, "(kein Eintrag)"))
    print("=" * 60 + "\n")

def export_week(data: dict):
    raw = input("Irgendein Datum in der Woche (YYYY-MM-DD oder 'heute'): ").strip()
    d = datetime.strptime(parse_date(raw), "%Y-%m-%d").date()
    days = week_dates(d)

    out_lines = []
    out_lines.append("WOCHENÜBERSICHT (zum Übertragen ins Berichtsheft)")
    out_lines.append(f"Woche ab Montag: {days[0].isoformat()}")
    out_lines.append("=" * 60)

    for day in days[:5]:  # Mo–Fr
        iso = day.isoformat()
        out_lines.append(f"\n{day.strftime('%A')} ({iso})")
        out_lines.append("-" * 60)
        out_lines.append(data.get(iso, "(kein Eintrag)"))

    output = "\n".join(out_lines)
    print("\n" + output + "\n")

    save = input("Als Textdatei speichern? (j/n): ").strip().lower()
    if save == "j":
        filename = f"wochenbericht_{days[0].isoformat()}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Gespeichert als {filename} ✅")

def menu():
    data = load_data()
    while True:
        print("=== Ausbildungsnachweis CLI ===")
        print("1) Tagesbericht hinzufügen/ändern")
        print("2) Tagesbericht anzeigen")
        print("3) Woche ausgeben (Mo–Fr)")
        print("4) Beenden")
        choice = input("Auswahl: ").strip()

        if choice == "1":
            add_entry(data)
            data = load_data()
        elif choice == "2":
            show_day(data)
        elif choice == "3":
            export_week(data)
        elif choice == "4":
            print("Bis dann 👋")
            break
        else:
            print("Ungültig. Bitte 1–4 wählen.\n")

if __name__ == "__main__":
    menu()
