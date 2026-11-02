import json, secrets, threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlsplit
from .core import Store, Fault

class Server(HTTPServer):
    def __init__(self,address,path):
        self.path=path
        self.lock=threading.Lock()
        super().__init__(address,Handler)
class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args): pass  # Never print tokens or query contents.
    def do_POST(self):
        store=None
        try:
            # Drain the body before any rejection: replying with unread request bytes
            # makes Windows reset the connection and the client sees RemoteDisconnected.
            length=int(self.headers.get('Content-Length','0'))
            if length<1:raise Fault('Ukuran request tidak valid.',413)
            if length>200000:
                remaining=min(length,5000000)
                while remaining>0:
                    chunk=self.rfile.read(min(65536,remaining))
                    if not chunk:break
                    remaining-=len(chunk)
                raise Fault('Ukuran request tidak valid.',413)
            raw=self.rfile.read(length)
            if self.headers.get('Origin'):raise Fault('Browser origin tidak diizinkan.',403)
            host=self.headers.get('Host','').split(':')[0]
            if host not in ('127.0.0.1','localhost'):raise Fault('Host ditolak.',403)
            request=json.loads(raw)
            if not isinstance(request,dict):raise Fault('JSON object diperlukan.')
            op=urlsplit(self.path).path.removeprefix('/api/')
            if not self.path.startswith('/api/') or op=='approve':raise Fault('Endpoint tidak tersedia.',404)
            with self.server.lock:
                store=Store(self.server.path)
                u=store.identity(self.headers.get('Authorization','').removeprefix('Bearer '))
                result=store.dispatch(u,op,request)
            self.send_json(200,result)
        except Fault as e:self.send_json(e.status,{'error':str(e)})
        except (ValueError,TypeError,KeyError):self.send_json(400,{'error':'Request tidak valid.'})
        except Exception:self.send_json(500,{'error':'Operasi gagal; periksa layanan lokal.'})
        finally:
            if store:store.db.close()
    def send_json(self,code,result):
        data=json.dumps(result,ensure_ascii=False).encode()
        self.send_response(code);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
