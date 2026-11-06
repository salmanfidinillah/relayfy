"""Start real production Gunicorn on loopback, synthetic data only; no deployment."""
import http.client,json,os,socket,subprocess,sys,tempfile,time,urllib.request,urllib.error
from pathlib import Path
root=Path(__file__).resolve().parents[1]
records=[]
def record(name,ok):
    records.append({'check':name,'passed':bool(ok)})
    if not ok:raise AssertionError(name)
with tempfile.TemporaryDirectory() as tmp:
    with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
    origin='https://relayfy.production.test';base='http://127.0.0.1:'+str(port)
    env=dict(os.environ,RELAYFY_ENV='production',PUBLIC_ORIGIN=origin,RELAYFY_DB_PATH=tmp+'/persistent-test.sqlite',PERSISTENT_STORAGE_CONFIRMED='true',OPENAI_API_KEY='',OPENAI_MODEL='')
    def start():
        proc=subprocess.Popen([sys.executable,'-m','gunicorn','--config','gunicorn.conf.py','--bind','127.0.0.1:'+str(port),'service.wsgi:application'],cwd=root,env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        for _ in range(60):
            try:
                with urllib.request.urlopen(base+'/healthz',timeout=1) as r:
                    if r.status==200:return proc
            except (OSError,urllib.error.URLError):time.sleep(.1)
        proc.terminate();raise RuntimeError('Production server startup failed')
    def req(path,p=None,cookie='',csrf=''):
        headers={'Origin':origin,'Content-Type':'application/json','Cookie':cookie,'X-CSRF-Token':csrf}
        data=json.dumps(p).encode() if p is not None else None
        request=urllib.request.Request(base+path,data=data,headers=headers)
        try:
            with urllib.request.urlopen(request,timeout=3) as r:return r.status,r.read(),dict(r.headers)
        except urllib.error.HTTPError as r:return r.code,r.read(),dict(r.headers)
    proc=start()
    try:
        c,raw,h=req('/');record('production static assets served',c==200 and b'Relayfy' in raw and b'.env' not in raw)
        record('security headers present',h.get('X-Frame-Options')=='DENY' and 'frame-ancestors' in h.get('Content-Security-Policy',''))
        record('anonymous API rejected',req('/api/workspaces')[0]==401)
        c,raw,h=req('/api/register',{'name':'Production QA','email':'production.qa@example.test','password':'Synthetic-QA-only-2026!'})
        record('register through production HTTP',c==200)
        session=json.loads(raw);cookie=h['Set-Cookie'].split(';')[0];csrf=session['csrf']
        record('production cookie Secure HttpOnly SameSite',all(x in h['Set-Cookie'] for x in ('Secure','HttpOnly','SameSite=Strict')))
        record('authenticated HTTP session',req('/api/session',cookie=cookie)[0]==200)
        proc.terminate();proc.wait(timeout=10);proc=start()
        record('database and session survive real process restart',req('/api/session',cookie=cookie)[0]==200)
        record('CSRF prevents mutation',req('/api/logout',{},cookie=cookie)[0]==403)
        record('valid logout',req('/api/logout',{},cookie=cookie,csrf=csrf)[0]==200)
        record('session revoked after logout',req('/api/session',cookie=cookie)[0]==401)
    finally:proc.terminate();proc.wait(timeout=10)
report={'run_at':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'scope':'Actual Gunicorn 26.2.0 production configuration on loopback; synthetic temporary database, NOT deployment or disk-mount verification','checks':records,'docker_build':'NOT RUN: Docker executable unavailable'}
(root/'evidence/production-smoke.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
