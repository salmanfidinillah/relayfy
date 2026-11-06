"""WorkBuddy client: only scoped HTTP jobs. Never reads the application database."""
import argparse,json,sys,time,urllib.request,urllib.error
from pathlib import Path
from urllib.parse import urlsplit
class Client:
    def __init__(self,path=None):
        path=Path(path) if path else Path(__file__).resolve().parent/'relayfy-connection.json'
        if not path.is_file():raise ValueError('File koneksi belum ada. Unduh dari web > Hubungkan WorkBuddy dan simpan sebagai relayfy-connection.json di folder agent ini.')
        self.config=json.loads(path.read_text(encoding='utf-8-sig'))
        url=self.config.get('url','');parsed=urlsplit(url)
        if parsed.scheme!='http' or parsed.hostname!='127.0.0.1' or not parsed.port or parsed.path not in ('','/') or parsed.query or parsed.fragment or parsed.username:
            raise ValueError('Client hanya menerima layanan lokal http://127.0.0.1:PORT. Buat koneksi dari web lokal pada laptop yang sama.')
        if not isinstance(self.config.get('token'),str):raise ValueError('File koneksi tidak valid.')
        self.url=url.rstrip('/')
    def call(self,op,payload=None):
        req=urllib.request.Request(self.url+'/api/worker/'+op,data=json.dumps(payload or {}).encode(),headers={'Content-Type':'application/json','Authorization':'Bearer '+self.config['token']})
        try:
            with urllib.request.urlopen(req,timeout=12) as r:return json.load(r)
        except urllib.error.HTTPError as e:
            try:message=json.loads(e.read()).get('error','Tool gagal.')
            except ValueError:message='Tool gagal.'
            raise ValueError(message)
        except (urllib.error.URLError,TimeoutError):raise ValueError('Server Relayfy belum berjalan atau tidak dapat dijangkau di laptop ini.')
    def next(self,wait=0):
        end=time.monotonic()+min(30,max(0,int(wait)))
        while True:
            result=self.call('next')
            if result.get('job') or time.monotonic()>=end:return result
            time.sleep(min(2,max(0,end-time.monotonic())))
def main():
    # MCP/WorkBuddy pipes use UTF-8, including on Windows consoles with another locale.
    sys.stdout.reconfigure(encoding='utf-8',newline='\n')
    p=argparse.ArgumentParser();p.add_argument('operation',choices=['next','finish','fail','status']);p.add_argument('--config');p.add_argument('--file');p.add_argument('--wait',type=int,default=0);args=p.parse_args()
    try:
        client=Client(args.config)
        if args.operation=='next':result=client.next(args.wait)
        elif args.operation=='status':result=client.call('status')
        else:
            if not args.file:raise ValueError('Gunakan --file reply.json yang berisi job, lease dan answer, atau failed=true.')
            payload=json.loads(Path(args.file).read_text(encoding='utf-8-sig'))
            if args.operation=='fail':payload['failed']=True
            result=client.call('finish',payload)
        print(json.dumps(result,ensure_ascii=False,indent=2))
    except (ValueError,KeyError,OSError,json.JSONDecodeError) as e:
        print(json.dumps({'error':str(e)},ensure_ascii=False),file=sys.stderr);return 1
    return 0
if __name__=='__main__':sys.exit(main())
