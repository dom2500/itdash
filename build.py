#!/usr/bin/env python3
import csv, html, io

TEMPLATE_FILE = 'index_template.html'
OUTPUT_FILE = 'index.html'
CSV_FILE = 'devices.csv'

def safe(v):
    """None -> '', trimmen & HTML-escapen."""
    return html.escape((v or '').strip())

# Template lesen
with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
    tpl = f.read()

# CSV lesen (Trenner automatisch erkennen, leere Zeilen ignorieren)
with open(CSV_FILE, 'r', encoding='utf-8', newline='') as f:
    raw = f.read()

lines = [ln for ln in raw.splitlines() if ln.strip() != '']
sample = '\n'.join(lines[:3]) or 'name,ip,host,protocol,port,note'
try:
    dialect = csv.Sniffer().sniff(sample)
except Exception:
    dialect = csv.excel  # Komma

rdr = csv.DictReader(io.StringIO('\n'.join(lines)), dialect=dialect)

rows = []
for r in rdr:
    # komplett leere Zeilen überspringen
    if not any((r.get(k) or '').strip() for k in ('name','ip','host','protocol','port','note')):
        continue

    name = safe(r.get('name'))
    ip   = safe(r.get('ip'))
    host = safe(r.get('host'))
    proto = (r.get('protocol') or '').strip().lower()
    if proto not in ('http', 'https'):
        proto = 'http'
    port = (r.get('port') or '').strip()
    note = safe(r.get('note'))

    portpart = ':' + port if port else ''
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
    rows.append(row)

html_out = tpl.replace('<!-- ROWS_WILL_BE_INSERTED_HERE -->', '\n'.join(rows))

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write(html_out)

print(f"{OUTPUT_FILE} erzeugt aus {CSV_FILE}. Zeilen: {len(rows)}")
