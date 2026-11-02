"""Operator only: provision the single persona token used by the runtime workspace.

Writes one token (not the whole key file) to the operator state folder, which is
outside the WorkBuddy runtime workspace. The runtime agent cannot choose a persona.
"""
import argparse, json, os
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--persona', help='andi | budi | manager')
p.add_argument('--state', default=str(Path.home() / '.relayfy-local'))
p.add_argument('--show', action='store_true', help='tampilkan persona aktif tanpa mengubah apa pun')
a = p.parse_args()

state = Path(a.state)
keys = json.loads((state / 'operator-keys.json').read_text(encoding='utf-8'))
active = state / 'active-token'

if a.show or not a.persona:
    current = '(belum ada)'
    if active.exists():
        t = active.read_text(encoding='utf-8').strip()
        current = next((k for k, v in keys.items() if v == t), 'tidak dikenal')
    print('Sesi runtime aktif:', current)
    print('Pilihan persona:', ', '.join(keys))
    raise SystemExit(0)

if a.persona not in keys:
    raise SystemExit('Persona tidak dikenal: ' + a.persona + ' (pilihan: ' + ', '.join(keys) + ')')

active.write_text(keys[a.persona], encoding='utf-8')
if os.name != 'nt':
    active.chmod(0o600)
print('Sesi runtime aktif:', a.persona, '— token tidak dicetak.')
print('Mulai task baru di WorkBuddy agar konteks percakapan lama tidak terbawa.')
