import io
import json
import os
import shutil
import subprocess
import tempfile
from datetime import date, datetime, timedelta
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)

BASE_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.join(BASE_DIR, "data.json")
DEFAULT_TEMPLATE = os.path.join(BASE_DIR, "Vorlage.docx")

app = Flask(__name__)
app.secret_key = "dev-secret-change-me"  # für flash-messages

def load_data() -> dict:
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data: dict) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def monday_of_week(d: date) -> date:
    return d - timedelta(days=d.weekday())

def week_dates(d: date):
    mon = monday_of_week(d)
    return [mon + timedelta(days=i) for i in range(7)]

def year_from_date(d: date) -> str:
    return str(d.year)

def build_context(data: dict, days: list[date], name: str, year: str) -> dict:
    def normalize_text(text: str) -> str:
        return (text or "").replace("\r\n", "\n")

    return {
        "NAME": name,
        "JAHR": year,
        "DAT_STA": days[0].isoformat(),
        "DAT_END": days[4].isoformat(),
        "MO_TAETIGKEITEN": normalize_text(data.get(days[0].isoformat(), "")),
        "DI_TAETIGKEITEN": normalize_text(data.get(days[1].isoformat(), "")),
        "MI_TAETIGKEITEN": normalize_text(data.get(days[2].isoformat(), "")),
        "DO_TAETIGKEITEN": normalize_text(data.get(days[3].isoformat(), "")),
        "FR_TAETIGKEITEN": normalize_text(data.get(days[4].isoformat(), "")),
        "DAT_HEUTE": date.today().isoformat(),
    }

def render_docx(template_path: str, context: dict, output_path: str) -> None:
    from docxtpl import DocxTemplate

    doc = DocxTemplate(template_path)
    doc.render(context)
    doc.save(output_path)

def convert_to_pdf(docx_path: str, out_dir: str) -> str | None:
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        return None
    try:
        subprocess.run(
            [
                soffice,
                "--headless",
                "--convert-to",
                "pdf",
                "--outdir",
                out_dir,
                docx_path,
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    pdf_path = os.path.join(out_dir, os.path.splitext(os.path.basename(docx_path))[0] + ".pdf")
    return pdf_path if os.path.exists(pdf_path) else None

@app.get("/")
def index():
    # Woche bestimmen (optional per Query: ?date=YYYY-MM-DD)
    q = request.args.get("date", "").strip()
    if q:
        try:
            d = datetime.strptime(q, "%Y-%m-%d").date()
        except ValueError:
            flash("Ungültiges Datum. Bitte YYYY-MM-DD verwenden.")
            return redirect(url_for("index"))
    else:
        d = date.today()

    days = week_dates(d)[:5]  # Mo–Fr
    data = load_data()

    week = []
    for day in days:
        iso = day.isoformat()
        week.append({
            "date_iso": iso,
            "weekday": day.strftime("%A"),
            "text": data.get(iso, "")
        })

    monday = days[0]
    prev_monday = monday - timedelta(days=7)
    next_monday = monday + timedelta(days=7)

    return render_template(
        "index.html",
        week=week,
        monday=monday.isoformat(),
        prev_monday=prev_monday.isoformat(),
        next_monday=next_monday.isoformat(),
    )

@app.get("/export")
def export_form():
    q = request.args.get("date", "").strip()
    if q:
        try:
            d = datetime.strptime(q, "%Y-%m-%d").date()
        except ValueError:
            flash("Ungültiges Datum. Bitte YYYY-MM-DD verwenden.")
            return redirect(url_for("index"))
    else:
        d = date.today()

    days = week_dates(d)[:5]
    data = load_data()
    year = year_from_date(days[0])
    week = []
    for day in days:
        iso = day.isoformat()
        week.append({
            "date_iso": iso,
            "weekday": day.strftime("%A"),
            "text": data.get(iso, "")
        })

    return render_template(
        "export.html",
        week=week,
        monday=days[0].isoformat(),
        friday=days[4].isoformat(),
        year=year,
    )

@app.post("/export")
def export_submit():
    name = request.form.get("name", "").strip()
    monday = request.form.get("monday", "").strip()

    if not name:
        flash("Bitte deinen Namen eingeben.")
        return redirect(url_for("export_form", date=monday or None))

    try:
        d = datetime.strptime(monday, "%Y-%m-%d").date()
    except ValueError:
        flash("Ungültiges Datum. Bitte YYYY-MM-DD verwenden.")
        return redirect(url_for("export_form"))

    data = load_data()
    year = year_from_date(d)
    days = week_dates(d)[:5]
    try:
        context = build_context(data, days, name, year)
    except ModuleNotFoundError:
        flash("Das Paket 'docxtpl' fehlt. Bitte installieren, um den Export zu nutzen.")
        return redirect(url_for("export_form", date=monday))

    with tempfile.TemporaryDirectory() as tmpdir:
        template_path = DEFAULT_TEMPLATE
        if not os.path.exists(template_path):
            flash("Keine Vorlage gefunden. Bitte Vorlage.docx im Projektverzeichnis ablegen.")
            return redirect(url_for("export_form", date=monday))

        output_docx = os.path.join(tmpdir, "ausbildungsnachweis.docx")
        try:
            render_docx(template_path, context, output_docx)
        except ModuleNotFoundError:
            flash("Das Paket 'docxtpl' fehlt. Bitte installieren, um den Export zu nutzen.")
            return redirect(url_for("export_form", date=monday))

        pdf_path = convert_to_pdf(output_docx, tmpdir)
        if pdf_path:
            with open(pdf_path, "rb") as pdf_file:
                return send_file(
                    io.BytesIO(pdf_file.read()),
                    mimetype="application/pdf",
                    as_attachment=False,
                    download_name="ausbildungsnachweis.pdf",
                )

        flash("PDF-Konvertierung fehlgeschlagen. DOCX wird stattdessen bereitgestellt.")
        with open(output_docx, "rb") as docx_file:
            return send_file(
                io.BytesIO(docx_file.read()),
                mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                as_attachment=True,
                download_name="ausbildungsnachweis.docx",
            )

@app.get("/add")
def add_form():
    # vorausfüllen über ?date=YYYY-MM-DD oder default heute
    q = request.args.get("date", "").strip()
    d = date.today().isoformat()
    if q:
        d = q
    data = load_data()
    return render_template("add.html", date_iso=d, text=data.get(d, ""))

@app.post("/add")
def add_submit():
    day = request.form.get("date", "").strip()
    text = request.form.get("text", "").strip()
    delete_entry = request.form.get("delete_entry") == "on"

    # Validierung
    try:
        datetime.strptime(day, "%Y-%m-%d")
    except ValueError:
        flash("Ungültiges Datum. Bitte YYYY-MM-DD verwenden.")
        return redirect(url_for("add_form"))

    data = load_data()
    if delete_entry:
        if day in data:
            del data[day]
            save_data(data)
            flash(f"Eintrag für {day} gelöscht ✅")
        else:
            flash("Kein Eintrag zum Löschen gefunden.")
        return redirect(url_for("index", date=day))

    if not text:
        flash("Bitte einen Text eingeben oder 'Eintrag löschen' wählen.")
        return redirect(url_for("add_form", date=day))

    data[day] = text
    save_data(data)

    flash(f"Gespeichert für {day} ✅")
    return redirect(url_for("index", date=day))

if __name__ == "__main__":
    app.run(debug=True)
