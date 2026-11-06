"""One-command LOCAL demo: synthetic personas + durable state + WorkBuddy job transport."""
import argparse,os
from pathlib import Path
from service.config import load_env,Config
from service.webapp import App
from web_start import Quiet,Threaded
from wsgiref.simple_server import make_server

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--state',default=str(Path.home()/'.relayfy-mvp'))
    p.add_argument('--port',type=int,default=int(os.getenv('PORT','8765')))
    p.add_argument('--host',default='127.0.0.1');p.add_argument('--strictPort',action='store_true')
    p.add_argument('--origin',help='Origin browser yang tepat, misal http://127.0.0.1:8765')
    p.add_argument('--backend',choices=['workbuddy','api'],default='workbuddy')
    a=p.parse_args();load_env()
    os.environ['RELAYFY_ENV']='development';os.environ['RELAYFY_DEMO']='true'
    os.environ['RELAYFY_AI_BACKEND']=a.backend
    state=Path(a.state).expanduser().resolve();state.mkdir(parents=True,exist_ok=True,mode=0o700)
    os.environ['RELAYFY_DB_PATH']=str(state/'relayfy.sqlite')
    os.environ['PUBLIC_ORIGIN']=a.origin or os.getenv('PUBLIC_ORIGIN') or 'http://127.0.0.1:'+str(a.port)
    app=App(Config())
    print('Relayfy MVP: '+app.config.origin,flush=True)
    print('Demo sintetis; data tetap tersimpan pada direktori state. Backend: '+a.backend,flush=True)
    print('Untuk WorkBuddy: pilih profil > Hubungkan WorkBuddy > ikuti petunjuk. Baca MULAI_DI_SINI.md.',flush=True)
    with make_server(a.host,a.port,app,server_class=Threaded,handler_class=Quiet) as server:server.serve_forever()
if __name__=='__main__':main()
