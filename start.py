"""Operator only: initialize private state and launch loopback service."""
import argparse,json,os
from pathlib import Path
from service.core import Store,seed
from service.server import Server
p=argparse.ArgumentParser();p.add_argument('--state',default=str(Path.home()/'.relayfy-local'));p.add_argument('--port',type=int,default=8765);a=p.parse_args()
root=Path(a.state).resolve();root.mkdir(parents=True,exist_ok=True)
if os.name!='nt':root.chmod(0o700)
path=root/'relayfy.sqlite';db=Store(path)
if not db.db.execute('SELECT 1 FROM users').fetchone():
    keys=seed(db);k=root/'operator-keys.json';k.write_text(json.dumps(keys,indent=2),encoding='utf-8')
    if os.name!='nt':k.chmod(0o600);path.chmod(0o600)
db.db.close()
print('Relayfy service: http://127.0.0.1:'+str(a.port),flush=True)
print('Operator state: '+str(root),flush=True)
print('Data sintetis; token tidak dicetak. Baca README untuk setup WorkBuddy.',flush=True)
Server(('127.0.0.1',a.port),str(path)).serve_forever()
