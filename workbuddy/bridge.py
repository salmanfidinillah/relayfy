"""Only HTTP client: no direct corpus, session switching or approval support."""
import argparse,json,os,sys,urllib.request,urllib.error
from pathlib import Path
OPS=['workspaces','create','sources','cite','ask','analyze','brief','get_brief','plan','audit']
p=argparse.ArgumentParser();p.add_argument('operation',choices=OPS);p.add_argument('--json',default='{}');p.add_argument('--file',help='UTF-8 JSON request file');a=p.parse_args()
try:
    payload=json.loads(Path(a.file).read_text(encoding='utf-8-sig') if a.file else a.json)
    token=os.environ.get('RELAYFY_TOKEN')
    if not token:raise ValueError('RELAYFY_TOKEN belum diatur oleh operator.')
    base=os.environ.get('RELAYFY_URL','http://127.0.0.1:8765')
    if not base.startswith('http://127.0.0.1:'):raise ValueError('Gunakan layanan loopback lokal.')
    req=urllib.request.Request(base+'/api/'+a.operation,data=json.dumps(payload).encode(),headers={'Authorization':'Bearer '+token,'Content-Type':'application/json'},method='POST')
    with urllib.request.urlopen(req,timeout=20) as r:result=json.load(r)
    print(json.dumps(result,ensure_ascii=False,indent=2))
except urllib.error.HTTPError as e:
    print(e.read().decode(),file=sys.stderr);sys.exit(1)
except Exception as e:
    print(json.dumps({'error':str(e)},ensure_ascii=False),file=sys.stderr);sys.exit(1)
