"""Use SQLite online backup API; do not copy an open WAL database directly."""
import argparse,sqlite3
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('database');p.add_argument('destination');a=p.parse_args()
if not Path(a.database).is_file():raise SystemExit('Database sumber tidak ditemukan.')
if Path(a.destination).exists():raise SystemExit('Tujuan sudah ada. Pilih nama backup baru.')
Path(a.destination).parent.mkdir(parents=True,exist_ok=True)
with sqlite3.connect(a.database) as source,sqlite3.connect(a.destination) as destination:
    source.backup(destination)
    if destination.execute('PRAGMA integrity_check').fetchone()[0]!='ok':raise SystemExit('Backup gagal integrity_check.')
print('Backup selesai; simpan di tempat privat di luar host layanan.')
