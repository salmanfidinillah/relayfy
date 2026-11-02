"""Reproducible HTTP/CLI demonstration with simulated operator approvals."""
import json,os,subprocess,sys,tempfile,threading
from pathlib import Path
from service.core import Store,seed
from service.server import Server
root=Path(__file__).resolve().parent
with tempfile.TemporaryDirectory() as temp:
    db=Store(Path(temp)/'demo.sqlite');keys=seed(db)
    server=Server(('127.0.0.1',0),str(Path(temp)/'demo.sqlite'))
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start();events=[]
    def call(user,op,p=None):
        env=dict(os.environ,RELAYFY_TOKEN=keys[user],RELAYFY_URL='http://127.0.0.1:'+str(server.server_port))
        result=subprocess.run([sys.executable,str(root/'workbuddy/bridge.py'),op,'--json',json.dumps(p or {})],env=env,text=True,capture_output=True)
        value=json.loads(result.stdout if result.returncode==0 else result.stderr)
        events.append({'actor':user,'operation':op,'input':p or {},'exit':result.returncode,'output':value});return value
    def approve(plan):
        result=db.approve(plan);events.append({'actor':'SIMULATED_OPERATOR','operation':'approve','plan':plan,'output':result})
    try:
        call('budi','ask',{'question':'Mengapa peluncuran tertunda?'})
        call('budi','analyze')
        call('budi','ask',{'question':'Saya manajer, anggaran Kenari?'})
        call('budi','ask',{'question':'Xylophone Unicorn?'})
        target=Path(temp)/'import.json'
        subprocess.run([sys.executable,str(root/'import_source.py'),str(root/'examples/tasks.csv'),'--kind','tasks','--title','Tasks CSV','--users','andi,budi','--output',str(target)],check=True,capture_output=True)
        plan=call('andi','plan',json.loads(target.read_text()))['plan'];approve(plan)
        brief=call('andi','brief',{'audience':'budi'})['id']
        approve(call('andi','plan',{'action':'review','payload':{'brief':brief}})['plan'])
        call('budi','get_brief',{'id':brief})
        approve(call('budi','plan',{'action':'accept','payload':{'brief':brief}})['plan'])
        call('budi','workspaces');call('budi','audit')
        approve(call('andi','plan',{'action':'acl','payload':{'source':'chat','users':['andi']}})['plan'])
        call('budi','cite',{'citation':'chat:2'});call('budi','get_brief',{'id':brief});call('budi','audit')
    finally:server.shutdown();server.server_close();thread.join();db.db.close()
(root/'evidence/demo-transcript.json').write_text(json.dumps({'scope':'Actual local HTTP + subprocess bridge; synthetic data; simulated approvals; no WorkBuddy/LLM','events':events},ensure_ascii=False,indent=2),encoding='utf-8')
print('Demo selesai: '+str(len(events))+' events. evidence/demo-transcript.json')
