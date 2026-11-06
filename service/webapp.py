"""Same-origin WSGI web application. Legacy bearer-token API is deliberately not mounted."""
import json, mimetypes, secrets, time
from pathlib import Path
from http.cookies import SimpleCookie
from urllib.parse import urlsplit, parse_qs
from .config import Config
from .core import Fault, UNKNOWN, dump
from .model import Model
from .webstore import digest
from .runtime import RuntimeStore as WebStore

ROOT=Path(__file__).resolve().parents[1]
class App:
    def __init__(self,config=None,model=None):
        self.config=config or Config(); self.model=model or Model(self.config)
        if self.config.production and getattr(self.config,'demo_mode',False):raise RuntimeError('Demo lokal tidak boleh dipakai sebagai autentikasi produksi.')
        Path(self.config.db_path).parent.mkdir(parents=True,exist_ok=True,mode=0o700)
        db=WebStore(self.config.db_path)
        db.db.execute('PRAGMA journal_mode=WAL')
        if getattr(self.config,'demo_mode',False):db.seed_demo()
        db.db.close()
    def __call__(self,environ,start_response):
        headers=[];store=None
        try:
            path=environ.get('PATH_INFO','/');method=environ.get('REQUEST_METHOD','GET')
            if path=='/healthz':return self.respond(start_response,200,{'status':'ok'})
            if not path.startswith('/api/'):
                if method!='GET':raise Fault('Endpoint tidak tersedia.',404)
                return self.static(path,start_response)
            if method not in ('GET','POST'):raise Fault('Metode tidak diizinkan.',405)
            store=WebStore(self.config.db_path)
            if path.startswith('/api/worker/'):
                return self.worker_request(environ,start_response,store,path,method)
            body={}
            if method=='POST':
                origin=environ.get('HTTP_ORIGIN','')
                if origin!=self.config.origin:raise Fault('Asal permintaan tidak diizinkan.',403)
                if environ.get('CONTENT_TYPE','').split(';')[0]!='application/json':raise Fault('Gunakan JSON.',415)
                n=int(environ.get('CONTENT_LENGTH') or 0)
                if not 0<n<=250000:raise Fault('Request terlalu besar atau kosong.',413)
                body=json.loads(environ['wsgi.input'].read(n))
                if not isinstance(body,dict):raise Fault('JSON object wajib.')
            query={k:v[0] for k,v in parse_qs(environ.get('QUERY_STRING','')).items()}
            p=body if method=='POST' else query
            op=path.removeprefix('/api/')
            cookies=SimpleCookie();cookies.load(environ.get('HTTP_COOKIE',''))
            token=cookies['relayfy_session'].value if 'relayfy_session' in cookies else ''
            if op=='meta' and method=='GET':return self.respond(start_response,200,{'demo':getattr(self.config,'demo_mode',False),'backend':getattr(self.config,'ai_backend','api'),'model_ready':self.model.ready,'registration':self.config.registration})
            if op=='profiles' and method=='GET':
                if not getattr(self.config,'demo_mode',False):raise Fault('Profil demo tidak tersedia.',404)
                return self.respond(start_response,200,store.demo_profiles())
            if op=='demo-login' and method=='POST':
                if not getattr(self.config,'demo_mode',False):raise Fault('Profil demo tidak tersedia.',404)
                token=store.demo_login(p.get('profile'));headers.append(('Set-Cookie',self.cookie(token)));sess=store.session(token)
                return self.respond(start_response,200,{'user':store.profile(sess['user']),'csrf':sess['csrf']},headers)
            if op in ('login','register') and method=='POST':
                store.limit('auth:'+environ.get('REMOTE_ADDR','unknown'))
                if not isinstance(p.get('password'),str) or len(p.get('password',''))>200:raise Fault('Password tidak valid.')
                if op=='register':
                    if not self.config.registration:raise Fault('Pendaftaran dinonaktifkan. Hubungi pemilik aplikasi.',403)
                    uid=store.register(p);token=store.new_session(uid)
                else:token=store.login(p)
                headers.append(('Set-Cookie',self.cookie(token)))
                sess=store.session(token);result={'user':store.profile(sess['user']),'csrf':sess['csrf']}
            else:
                sess=store.session(token);u=sess['user']
                if method=='POST' and not secrets.compare_digest(environ.get('HTTP_X_CSRF_TOKEN',''),sess['csrf']):raise Fault('Sesi form kedaluwarsa. Muat ulang halaman.',403)
                if op=='session' and method=='GET':result={'user':store.profile(u),'csrf':sess['csrf'],'model_ready':self.model.ready,'model_name':self.config.model if self.model.ready else '', 'backend':getattr(self.config,'ai_backend','api'),'demo':getattr(self.config,'demo_mode',False)}
                elif op=='logout' and method=='POST':
                    store.db.execute('DELETE FROM sessions WHERE token=?',(digest(token),));store.db.commit()
                    headers.append(('Set-Cookie',self.cookie('',True)));result={'ok':True}
                elif op=='workspaces' and method=='GET':result=store.dispatch(u,'workspaces',{})
                elif op=='create' and method=='POST':result=store.create_workspace(u,p)
                else:
                    w=p.get('workspace','');ws=store.ws(u,w)
                    if op=='workspace' and method=='GET':result=store.snapshot(u,w)
                    elif op=='cite' and method=='GET':result=store.dispatch(u,'cite',p)
                    elif op=='source' and method=='GET':
                        visible={s['id']:s for s in store.visible(u,w)}
                        if p.get('id') not in visible:raise Fault(UNKNOWN,404)
                        s=visible[p['id']];result={k:s[k] for k in ('id','title','kind','body','effective','version')}
                    elif op=='agent_status' and method=='GET':result=store.agent_status(u,w)
                    elif op=='agent_pair' and method=='POST':
                        if getattr(self.config,'ai_backend','api')!='workbuddy':raise Fault('Pilih backend WorkBuddy untuk melakukan pairing.',409)
                        result=store.pair(u,w,self.config.origin,p.get('purpose','ask'))
                    elif op=='jobs' and method=='GET':result=store.jobs(u,w)
                    elif op=='job' and method=='GET':result=store.job(u,w,p.get('id'))
                    elif op=='cancel_job' and method=='POST':result=store.cancel_job(u,w,p.get('id'))
                    elif op=='history' and method=='GET':result=store.history(u,w)
                    elif op=='audit' and method=='GET':result=store.dispatch(u,'audit',p)
                    elif op=='brief' and method=='GET':result=store.brief(u,w,p.get('id'))
                    elif op=='plan' and method=='POST':
                        if p.get('action') not in ('import','acl','review','accept','clarify'):raise Fault('Aksi tidak tersedia.')
                        result=store.dispatch(u,'plan',p)
                        result['next']='Tinjau detail dan konfirmasi melalui dialog aplikasi.'
                        store.log(u,w,'approval_requested',{'plan':result['plan'],'action':result['action'],'preview':result['preview']})
                    elif op=='confirm' and method=='POST':
                        if p.get('confirmed') is not True:raise Fault('Konfirmasi manusia diperlukan.')
                        # Bind both the requested workspace and plan actor; never trust actor in body.
                        plan=store.db.execute('SELECT workspace FROM plans WHERE id=? AND actor=?',(p.get('plan'),u)).fetchone()
                        if not plan or plan['workspace']!=w:raise Fault(UNKNOWN,404)
                        result=store.confirm(u,p['plan'])
                    elif op in ('ask','generate') and method=='POST':
                        store.limit('ai:'+u,30,600)
                        if getattr(self.config,'ai_backend','api')=='workbuddy' or (op=='ask' and p.get('answer_mode')=='evidence'):
                            context=store.prepare(u,w,op,p)
                            result=store.evidence_reply(u,w,context) if op=='ask' and p.get('answer_mode')=='evidence' else store.enqueue(u,w,context)
                        else:result=self.ai(store,u,w,ws,op,p)
                    elif op=='extractive' and method=='POST':
                        if ws['giver']!=u:raise Fault('Hanya pemberi dapat menyusun handover.',403)
                        data=store.analysis(ws['receiver'],w)
                        if not store.sources_allowed(u,w,data):raise Fault(UNKNOWN,404)
                        if not data['evidence']:raise Fault('Tambahkan sumber yang dapat diakses penerima terlebih dahulu.')
                        result=store.save_brief(u,w,ws['receiver'],ws['revision'],data,'extractive')
                    else:raise Fault('Endpoint tidak tersedia.',404)
            return self.respond(start_response,200,result,headers)
        except Fault as e:return self.respond(start_response,e.status,{'error':str(e)},headers)
        except (ValueError,TypeError,KeyError):return self.respond(start_response,400,{'error':'Request tidak valid.'})
        except Exception:
            # No exception contents: provider bodies, passwords and source text must not enter access logs.
            return self.respond(start_response,500,{'error':'Operasi gagal. Coba muat ulang atau hubungi operator.'})
        finally:
            if store:store.db.close()
    def worker_request(self,environ,start,store,path,method):
        if getattr(self.config,'ai_backend','api')!='workbuddy':raise Fault('Endpoint tidak tersedia.',404)
        if method!='POST':raise Fault('Metode tidak diizinkan.',405)
        if environ.get('HTTP_ORIGIN') or environ.get('REMOTE_ADDR') not in ('127.0.0.1','::1'):raise Fault('Tool agent hanya menerima koneksi lokal tanpa browser origin.',403)
        token=environ.get('HTTP_AUTHORIZATION','').removeprefix('Bearer ')
        key=store.worker(token)
        if environ.get('CONTENT_TYPE','').split(';')[0]!='application/json':raise Fault('Gunakan JSON.',415)
        size=int(environ.get('CONTENT_LENGTH') or 0)
        if not 0<size<=100000:raise Fault('Ukuran payload tidak valid.',413)
        payload=json.loads(environ['wsgi.input'].read(size))
        if not isinstance(payload,dict):raise Fault('JSON object wajib.')
        op=path.rsplit('/',1)[-1]
        if op=='next':result=store.next_job(key)
        elif op=='finish':result=store.finish_job(key,payload)
        elif op=='status':result=store.agent_status(key['user'],key['workspace'])
        else:raise Fault('Endpoint tidak tersedia.',404)
        return self.respond(start,200,result)
    def ai(self,store,u,w,ws,op,p):
        if op=='ask':
            question=p.get('question','').strip()
            if not question or len(question)>2000:raise Fault('Pertanyaan wajib, maksimal 2000 karakter.')
            retrieval=store.dispatch(u,'ask',{'workspace':w,'question':question})
            evidence=retrieval['evidence']
            # Short follow-ups can use re-authorized prior citations, never another user's turns.
            history=store.history(u,w)[-4:]
            if len(question.split())<=6 and history:
                previous=history[-1]['result'].get('evidence',[])
                citations={e['citation'] for e in evidence}
                evidence+= [e for e in previous if e['citation'] not in citations][:4]
            if sum(len(e['text']) for e in evidence)>45000:raise Fault('Bukti terlalu panjang untuk satu pertanyaan. Pisahkan bahan ke workspace lebih kecil.',413)
            conflicts=store.analysis(u,w)['conflicts']
            selected={e['citation'] for e in evidence}
            conflicts=[c for c in conflicts if any(e['citation'] in selected for e in c['sources'])]
            for conflict in conflicts:
                for e in conflict['sources']:
                    if e['citation'] not in selected:evidence.append({k:v for k,v in e.items() if k!='value'});selected.add(e['citation'])
            try:
                answer=self.model.generate(question,evidence,[{'question':h['question'],'claims':h['result'].get('claims',[])} for h in history])
            except Fault as e:
                store.log(u,w,'model_failed',{'operation':'ask','status':e.status});raise
            result={**answer,'evidence':evidence,'conflicts':conflicts,'access_revision':ws['revision']}
            store.save_answer(u,w,ws['revision'],question,result);return result
        if ws['giver']!=u:raise Fault('Hanya pemberi dapat menyusun handover.',403)
        data=store.analysis(ws['receiver'],w)
        if not store.sources_allowed(u,w,data):raise Fault(UNKNOWN,404)
        if not data['evidence']:raise Fault('Tambahkan sumber yang dapat diakses penerima terlebih dahulu.')
        # Explicit limit avoids silently summarizing an incomplete corpus.
        if sum(len(e['text']) for e in data['evidence'])>45000:raise Fault('Bahan terlalu panjang untuk satu ringkasan. Pisahkan workspace atau ringkas bahan sumber terlebih dahulu.',413)
        try:answer=self.model.generate('Buat ringkasan handover bersumber. Tunjukkan ketidakpastian.',data['evidence'],mode='brief')
        except Fault as e:
            store.log(u,w,'model_failed',{'operation':'brief','status':e.status});raise
        data['ai']=answer
        return store.save_brief(u,w,ws['receiver'],ws['revision'],data,'ai')
    def cookie(self,value,clear=False):
        return 'relayfy_session='+value+'; Path=/; HttpOnly; SameSite=Strict; Max-Age='+('0' if clear else '43200')+('; Secure' if self.config.production else '')
    def respond(self,start,status,data,extra=None):
        raw=json.dumps(data,ensure_ascii=False).encode()
        phrases={200:'OK',400:'Bad Request',401:'Unauthorized',403:'Forbidden',404:'Not Found',405:'Method Not Allowed',409:'Conflict',413:'Payload Too Large',415:'Unsupported Media Type',422:'Unprocessable Entity',429:'Too Many Requests',500:'Internal Server Error',502:'Bad Gateway',503:'Service Unavailable'}
        start(str(status)+' '+phrases.get(status,'Error'),self.headers()+[('Content-Type','application/json; charset=utf-8'),('Content-Length',str(len(raw)))]+(extra or []))
        return [raw]
    def headers(self):
        return [('Cache-Control','no-store'),('X-Content-Type-Options','nosniff'),('Referrer-Policy','same-origin'),('X-Frame-Options','DENY'),
                ('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'"),
                ('Permissions-Policy','camera=(), microphone=(), geolocation=()')]
    def static(self,path,start):
        files={'/':'index.html','/app.js':'app.js','/style.css':'style.css','/logo.svg':'logo.svg','/assets/team-portraits.png':'assets/team-portraits.png'}
        if path not in files:raise Fault('Halaman tidak tersedia.',404)
        file=ROOT/'web'/files[path]
        # Production serves the verified build, if present. All files are fixed allowlist paths.
        built=ROOT/'dist'/files[path]
        if self.config.production and built.exists():file=built
        raw=file.read_bytes();ctype=mimetypes.guess_type(str(file))[0] or 'application/octet-stream'
        start('200 OK',self.headers()+[('Content-Type',ctype+'; charset=utf-8'),('Content-Length',str(len(raw)))])
        return [raw]
