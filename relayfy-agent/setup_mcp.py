"""Generate local MCP path configuration only; never edits WorkBuddy global settings."""
import json,sys
from pathlib import Path
root=Path(__file__).resolve().parent
server={'relayfy':{'command':sys.executable,'args':[str(root/'server.py')],'timeout':45000}}
(root/'mcp.local.json').write_text(json.dumps({'mcpServers':server},indent=2),encoding='utf-8')
(root/'mcp.servers.local.json').write_text(json.dumps(server,indent=2),encoding='utf-8')
print('Konfigurasi lokal dibuat. Tambahkan server relayfy melalui custom MCP WorkBuddy sesuai format kolom aplikasi. Jangan menimpa server lain.')
