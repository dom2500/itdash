#!/usr/bin/env python3
import csv, html, os

TEMPLATE_FILE = 'index_template.html'
OUTPUT_FILE = 'index.html'
CSV_FILE = 'devices.csv'

with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
    tpl = f.read()

rows_html = []
with open(CSV_FILE, newline='', encoding='utf-8') as f:
    rdr = csv.DictReader(f)
    for r in rdr:
        name = html.escape(r.get('name',''))
        ip = html.escape(r.get('ip',''))
        host = html.escape(r.get('host',''))
        proto = (r.get('protocol') or 'http').lower()
        port = (r.get('port') or '').strip()
        note = html.escape(r.get('note',''))
        portpart = (':' + port) if port else ''
        # prefer host if present, else ip
        target = host if host else ip
        url = f"{proto}://{target}{portpart}" if target else '#'
        row = f"<tr><td>{name}</td><td><a href='{url}' target='_blank' rel='noopener'>{ip}</a></td><td>{host}</td><td><a href='{url}' target='_blank'>{proto.upper()}{portpart}</a></td><td class='note'>{note}</td></tr>"
        rows_html.append(row)

html_out = tpl.replace('<!-- ROWS_WILL_BE_INSERTED_HERE -->', '\n'.join(rows_html))

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write(html_out)

print(f"{OUTPUT_FILE} erzeugt aus {CSV_FILE}.")
