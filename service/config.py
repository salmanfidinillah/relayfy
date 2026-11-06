"""Small dependency-free runtime configuration. Never exposes secrets to clients."""
import os
from pathlib import Path

def load_env(path=None):
    path = Path(path or Path(__file__).resolve().parents[1] / '.env')
    if path.exists():
        for line in path.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                os.environ.setdefault(k.strip(), v.strip().strip('\"\''))

class Config:
    def __init__(self):
        load_env()
        self.production = os.getenv('RELAYFY_ENV') == 'production'
        self.origin = os.getenv('PUBLIC_ORIGIN', 'http://127.0.0.1:8765').rstrip('/')
        self.db_path = os.getenv('RELAYFY_DB_PATH', str(Path.home() / '.relayfy-web' / 'relayfy.sqlite'))
        self.api_key = os.getenv('OPENAI_API_KEY', '')
        self.model = os.getenv('OPENAI_MODEL', '')
        self.base_url = os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1').rstrip('/')
        self.model_timeout = float(os.getenv('MODEL_TIMEOUT_SECONDS', '35'))
        self.demo_mode = os.getenv('RELAYFY_DEMO', 'false').lower() == 'true'
        self.ai_backend = os.getenv('RELAYFY_AI_BACKEND', 'api')
        if self.ai_backend not in ('api','workbuddy'):raise RuntimeError('RELAYFY_AI_BACKEND harus api atau workbuddy.')
        if self.production and self.demo_mode:raise RuntimeError('Profil demo dilarang pada konfigurasi produksi.')
        self.registration = os.getenv('ALLOW_REGISTRATION', 'true').lower() == 'true'
        if self.production:
            if not self.origin.startswith('https://'): raise RuntimeError('PUBLIC_ORIGIN harus HTTPS pada produksi.')
            if not os.getenv('RELAYFY_DB_PATH') or os.getenv('PERSISTENT_STORAGE_CONFIRMED') != 'true':
                raise RuntimeError('Produksi memerlukan RELAYFY_DB_PATH dan PERSISTENT_STORAGE_CONFIRMED=true pada volume permanen.')
