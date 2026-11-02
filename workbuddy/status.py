"""Read-only environment check for the runtime workspace. Never prints the token."""
import json, os, subprocess, sys
from pathlib import Path

print('python:', sys.version.split()[0])
print('service:', os.environ.get('RELAYFY_URL', 'http://127.0.0.1:8765'))

source, token = None, os.environ.get('RELAYFY_TOKEN')
if token:
    source = 'RELAYFY_TOKEN'
else:
    f = Path(os.environ.get('RELAYFY_STATE', Path.home() / '.relayfy-local')) / 'active-token'
    if f.exists():
        token, source = f.read_text(encoding='utf-8').strip(), 'file sesi operator'

if not token:
    print('token: TIDAK ADA — minta operator menjalankan: python session.py --persona <nama>')
    sys.exit(1)
print('token: tersedia via', source, '(nilai tidak ditampilkan)')

r = subprocess.run([sys.executable, str(Path(__file__).with_name('bridge.py')), 'workspaces'],
                   capture_output=True, text=True)
if r.returncode != 0:
    print('bridge: GAGAL —', (r.stderr or r.stdout).strip()[:300])
    sys.exit(1)
data = json.loads(r.stdout)
print('bridge: OK,', len(data), 'workspace')
for w in data:
    print('  -', w['id'], '|', w['name'], '| revision', w['revision'], '|', w['status'])
