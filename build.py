#!/usr/bin/env python3
import csv, html, os, io

TEMPLATE_FILE = 'index_template.html'
OUTPUT_FILE = 'index.html'
CSV_FILE = 'devices.csv'

def safe(v: str) -> str:
    """None -> '', trimmen, HTML-escapen."""
    if v is None:
        return ''
    return html.escape(str(v).strip())

# Template laden
with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
    tpl = f.read()

# CSV einlesen (Trenner automatisch erkennen, Komma oder Semikolon)
with open(CSV_FILE, 'r', encoding='utf-8', newline='') as f:
    raw = f.read()
    # Dialekt erkennen (fällt zurück auf Komma)
    try:
        dialect = csv.Sniffer().sniff(raw.splitlines()[0])
    except Exception:
        dialect = csv.get_dialect('excel')  # Komma
    rdr = csv.DictReader(io.StringIO(raw), dialect=dialect)

    rows_html = []
    for r in rdr:
        # komplett leere Zeilen überspringen
        if not any((r.get(k) or '').strip() for k in ('name','ip','host','protocol','port','note')):
            continue

        name = safe(r.get('name'))
        ip   = safe(r.get('ip'))
        host = safe(r.get('host'))
        proto_raw = (r.get('protocol') or '').strip().lower()
        proto = proto_raw if proto_raw in ('http','https') else 'http'
        port = (r.get('port') or '').strip()
        note = safe(r.get('note'))

        portpart = (':' + port) if port else ''
        target = host or ip
        url = f"{proto}://{target}{portpart}" if target else '#'

        row = (
            f"<tr>"
            f"<td>{name}</td>"
            f"<td><a href='{url}' target='_blank' rel='noopener'>{ip}</a></td>"
            f"<td>{host}</td>"
            f"<td><a href='{url}' target='_blank'>{proto.upper()}{portpart}</a></td>"
            f"<td class='note'>{note}</td>"
            f"</tr>"
        )
        rows_html.append(row)

html_out = tpl.replace('<!-- ROWS_WILL_BE_INSERTED_HERE -->', '\n'.join(rows_html))

with open(OUTPUT_FI_
