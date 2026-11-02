"""Prepare a reviewable import request from TXT/MD/chat or task CSV/JSON."""
import argparse,csv,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('--title',required=True);p.add_argument('--users',required=True);p.add_argument('--kind',choices=['document','chat','tasks'],default='document');p.add_argument('--workspace',default='demo');p.add_argument('--output',required=True);a=p.parse_args()
f=Path(a.input);body=f.read_text(encoding='utf-8-sig')
if a.kind=='tasks' and f.suffix.lower() in ('.csv','.json'):
    rows=json.loads(body) if f.suffix.lower()=='.json' else list(csv.DictReader(body.splitlines()))
    if not isinstance(rows,list):raise SystemExit('Task JSON harus array.')
    fields=['title','status','pic','deadline','blocker','dependency'];lines=[]
    for r in rows:
        if not r.get('title'):raise SystemExit('Setiap task memerlukan title.')
        values=[str(r.get(k) or '').replace('|','/').replace('\n',' ') for k in fields]
        lines.append('TASK|'+'|'.join(values))
    body='\n'.join(lines)
req={'workspace':a.workspace,'action':'import','payload':{'title':a.title,'body':body,'kind':a.kind,'users':a.users.split(',')}}
Path(a.output).write_text(json.dumps(req,ensure_ascii=False,indent=2),encoding='utf-8')
print('Draf request tersimpan. Jalankan bridge plan, lalu tinjau melalui approve.py.')
