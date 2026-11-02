"""Run by human operator outside WorkBuddy. Requires explicit typed confirmation."""
import argparse,json
from pathlib import Path
from service.core import Store,Fault
p=argparse.ArgumentParser();p.add_argument('plan');p.add_argument('--state',default=str(Path.home()/'.relayfy-local'));a=p.parse_args()
db=Store(Path(a.state)/'relayfy.sqlite')
plan=db.db.execute('SELECT * FROM plans WHERE id=?',(a.plan,)).fetchone()
if not plan:raise SystemExit('Plan tidak ditemukan.')
print(json.dumps(dict(plan),ensure_ascii=False,indent=2))
if input('Setujui detail di atas? Ketik SETUJU: ').strip()!='SETUJU':raise SystemExit('Tidak dieksekusi.')
try:print(json.dumps(db.approve(a.plan),ensure_ascii=False,indent=2))
except Fault as e:raise SystemExit(str(e))
finally:db.db.close()
