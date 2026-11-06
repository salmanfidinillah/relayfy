import argparse, os
from wsgiref.simple_server import make_server, WSGIRequestHandler, WSGIServer
from socketserver import ThreadingMixIn
from service.config import Config
from service.webapp import App
class Quiet(WSGIRequestHandler):
    def log_message(self,*a):pass
class Threaded(ThreadingMixIn,WSGIServer):daemon_threads=True
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--strictPort',action='store_true');p.add_argument('--host',default='127.0.0.1');p.add_argument('--port',type=int,default=int(os.getenv('PORT','8765')));a=p.parse_args()
    config=Config()
    print('Relayfy web: http://'+a.host+':'+str(a.port),flush=True)
    print('Development server. Production: gunicorn service.wsgi:application',flush=True)
    with make_server(a.host,a.port,App(config),server_class=Threaded,handler_class=Quiet) as server:server.serve_forever()
