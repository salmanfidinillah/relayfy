"""Web-specific authorization, sessions and versioned handovers on the retained core schema."""
import hashlib, hmac, json, secrets, time
from .core import Store, Fault, UNKNOWN, dump, now

def digest(value): return hashlib.sha256(value.encode()).hexdigest()
def password_hash(password, salt=None):
    salt=salt or secrets.token_hex(16)
    return salt+':'+hashlib.scrypt(password.encode(),salt=salt.encode(),n=16384,r=8,p=1).hex()
def password_ok(password, encoded):
    try: return hmac.compare_digest(password_hash(password,encoded.split(':')[0]),encoded)
    except (ValueError,AttributeError): return False

class WebStore(Store):
    def __init__(self,path):
        super().__init__(path)
        self.db.execute('PRAGMA busy_timeout=10000')
        self.db.executescript('''
        CREATE TABLE IF NOT EXISTS accounts(user TEXT PRIMARY KEY, email TEXT UNIQUE NOT NULL, name TEXT NOT NULL, password TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS sessions(token TEXT PRIMARY KEY, user TEXT NOT NULL, csrf TEXT NOT NULL, expires REAL NOT NULL);
        CREATE TABLE IF NOT EXISTS conversations(id INTEGER PRIMARY KEY, user TEXT, workspace TEXT, revision INTEGER, question TEXT, result TEXT, created TEXT);
        CREATE TABLE IF NOT EXISTS brief_meta(brief TEXT PRIMARY KEY, creator TEXT, kind TEXT, created TEXT);
        CREATE TABLE IF NOT EXISTS current_briefs(workspace TEXT,audience TEXT,brief TEXT,PRIMARY KEY(workspace,audience));
        CREATE TABLE IF NOT EXISTS clarifications(plan TEXT PRIMARY KEY,workspace TEXT,brief TEXT,user TEXT,revision INTEGER,question TEXT,created TEXT);
        CREATE TABLE IF NOT EXISTS rate_limits(key TEXT PRIMARY KEY,start REAL,count INTEGER);
        CREATE INDEX IF NOT EXISTS idx_acl_user ON acl(user, source);
        CREATE INDEX IF NOT EXISTS idx_conversations ON conversations(user,workspace,revision);
        ''')
    def register(self,p):
        email=p.get('email','').strip().lower(); name=p.get('name','').strip();pw=p.get('password','')
        if '@' not in email or len(email)>254 or not name or len(name)>100 or len(pw)<12 or len(pw)>200:
            raise Fault('Nama, email valid, dan password 12–200 karakter wajib.')
        if self.db.execute('SELECT 1 FROM accounts WHERE email=?',(email,)).fetchone():raise Fault('Pendaftaran tidak dapat diproses. Gunakan akun yang sudah dimiliki.',409)
        uid=secrets.token_hex(12)
        self.db.execute('INSERT INTO users VALUES(?,NULL)',(uid,))
        self.db.execute('INSERT INTO accounts VALUES(?,?,?,?)',(uid,email,name,password_hash(pw)))
        self.db.commit();return uid
    def login(self,p):
        email=p.get('email','').strip().lower(); password=p.get('password','')
        row=self.db.execute('SELECT * FROM accounts WHERE email=?',(email,)).fetchone()
        # Equal work for absent accounts; never return account existence.
        encoded=row['password'] if row else '00000000000000000000000000000000:'+('0'*128)
        valid=password_ok(password,encoded)
        if not row or not valid:raise Fault('Email atau password salah.',401)
        return self.new_session(row['user'])
    def new_session(self,u):
        token=secrets.token_urlsafe(32);csrf=secrets.token_urlsafe(32)
        self.db.execute('DELETE FROM sessions WHERE expires<?',(time.time(),))
        self.db.execute('INSERT INTO sessions VALUES(?,?,?,?)',(digest(token),u,csrf,time.time()+43200))
        self.db.commit();return token
    def session(self,token):
        row=self.db.execute('SELECT user,csrf FROM sessions WHERE token=? AND expires>?',(digest(token),time.time())).fetchone()
        if not row:raise Fault('Silakan masuk kembali.',401)
        return dict(row)
    def profile(self,u):
        r=self.db.execute('SELECT user id,email,name FROM accounts WHERE user=?',(u,)).fetchone()
        return dict(r) if r else {'id':u,'name':u}
    def limit(self,key,maximum=20,window=600):
        t=time.time();row=self.db.execute('SELECT * FROM rate_limits WHERE key=?',(key,)).fetchone()
        start=row['start'] if row and t-row['start']<window else t
        count=row['count']+1 if row and start==row['start'] else 1
        self.db.execute('INSERT OR REPLACE INTO rate_limits VALUES(?,?,?)',(key,start,count));self.db.commit()
        if count>maximum:raise Fault('Terlalu banyak permintaan. Coba lagi beberapa menit lagi.',429)
    def create_workspace(self,u,p):
        row=self.db.execute('SELECT user FROM accounts WHERE email=?',(p.get('receiver_email','').strip().lower(),)).fetchone()
        if not row:raise Fault('Penerima belum tersedia. Minta penerima mendaftar terlebih dahulu.')
        if row['user']==u:raise Fault('Pilih akun penerima yang berbeda.')
        name=p.get('name','').strip()
        if not name or len(name)>120:raise Fault('Nama workspace wajib, maksimal 120 karakter.')
        result=super().dispatch(u,'create',{'name':name,'receiver':row['user']})
        self.log(u,result['id'],'create',{'name':name,'receiver':row['user']})
        return result
    def sources_allowed(self,u,w,data):
        return {e['source'] for e in data.get('evidence',[])} <= {s['id'] for s in self.visible(u,w)}
    def brief(self,u,w,bid):
        ws=self.ws(u,w)
        row=self.db.execute('SELECT b.*,m.creator,m.kind,m.created FROM briefs b JOIN brief_meta m ON m.brief=b.id WHERE b.id=? AND b.workspace=?',(bid,w)).fetchone()
        if not row:raise Fault(UNKNOWN,404)
        if u!=row['creator'] and (u!=row['audience'] or row['status']=='Draft'):raise Fault(UNKNOWN,404)
        if row['revision']!=ws['revision']:raise Fault('Versi tidak berlaku. Buat ringkasan terbaru.',409)
        data=json.loads(row['body'])
        if not self.sources_allowed(u,w,data):raise Fault(UNKNOWN,404)
        return {k:row[k] for k in ('id','revision','audience','status','kind','created')}|data
    def list_briefs(self,u,w):
        ws=self.ws(u,w);out=[]
        for r in self.db.execute('SELECT b.id FROM current_briefs c JOIN briefs b ON b.id=c.brief WHERE c.workspace=? AND b.revision=?',(w,ws['revision'])):
            try:out.append(self.brief(u,w,r['id']))
            except Fault:pass
        return out
    def history(self,u,w):
        ws=self.ws(u,w);out=[]
        for row in self.db.execute('SELECT * FROM conversations WHERE user=? AND workspace=? AND revision=? ORDER BY id DESC LIMIT 12',(u,w,ws['revision'])):
            result=json.loads(row['result'])
            if self.sources_allowed(u,w,result):out.append({'id':row['id'],'question':row['question'],'result':result,'created':row['created']})
        return list(reversed(out))
    def save_answer(self,u,w,revision,q,result):
        self.db.execute('BEGIN IMMEDIATE')
        try:
            if self.ws(u,w)['revision']!=revision or not self.sources_allowed(u,w,result):raise Fault('Akses atau sumber berubah saat model bekerja. Ulangi permintaan.',409)
            self.db.execute('INSERT INTO conversations(user,workspace,revision,question,result,created) VALUES(?,?,?,?,?,?)',(u,w,revision,q,dump(result),now()))
            self.log(u,w,'ai_answer',{'question':q,'result':result})
        except Exception:self.db.rollback();raise
    def save_brief(self,u,w,audience,revision,data,kind):
        self.db.execute('BEGIN IMMEDIATE')
        try:
            ws=self.ws(u,w)
            if ws['revision']!=revision:raise Fault('Akses atau sumber berubah. Buat ulang ringkasan.',409)
            if ws['giver']!=u:raise Fault('Hanya pemberi dapat menyusun handover.',403)
            if not self.sources_allowed(u,w,data) or not self.sources_allowed(audience,w,data):raise Fault(UNKNOWN,404)
            bid=secrets.token_hex(12)
            self.db.execute('INSERT INTO briefs VALUES(?,?,?,?,?,?)',(bid,w,revision,audience,dump(data),'Draft'))
            self.db.execute('INSERT INTO brief_meta VALUES(?,?,?,?)',(bid,u,kind,now()))
            self.db.execute('INSERT OR REPLACE INTO current_briefs VALUES(?,?,?)',(w,audience,bid))
            self.db.execute("UPDATE workspaces SET status='Draft' WHERE id=?",(w,))
            self.log(u,w,'brief_draft',{'brief':bid,'audience':audience,'kind':kind})
            return self.brief(u,w,bid)
        except Exception:self.db.rollback();raise
    def validate(self,u,w,action,p):
        ws=self.ws(u,w)
        if action=='import':
            if not isinstance(p.get('users'),list) or not all(isinstance(x,str) for x in p['users']):raise Fault('Audiens sumber tidak valid.')
            if u not in p['users']:raise Fault('Pemberi harus tetap memiliki akses sumber.')
            if len(p.get('title',''))>200 or len(p.get('effective',''))>40:raise Fault('Metadata terlalu panjang.')
        if action=='acl':
            if ws['role']!='manager':raise Fault('Tindakan tidak diizinkan.',403)
            if p.get('source') not in {s['id'] for s in self.visible(u,w)}:raise Fault(UNKNOWN,404)
            if not isinstance(p.get('users'),list) or u not in p['users']:raise Fault('Pemberi harus tetap memiliki akses sumber.')
        if action in ('review','accept','clarify'):
            b=self.brief(u,w,p.get('brief'))
            current=self.db.execute('SELECT brief FROM current_briefs WHERE workspace=? AND audience=?',(w,b['audience'])).fetchone()
            if not current or current['brief']!=b['id']:raise Fault('Ada draf lebih baru. Tinjau versi terbaru.',409)
            if action=='review' and (u!=ws['giver'] or b['status'] not in ('Draft','Needs Clarification')):raise Fault('Review tidak diizinkan pada status ini.',409)
            if action in ('accept','clarify') and (u!=ws['receiver'] or b['audience']!=u):raise Fault('Tindakan tidak diizinkan.',403)
            if action=='clarify' and b['status'] not in ('Ready for Acceptance','Needs Clarification'):raise Fault('Versi ini belum dibagikan untuk review.',409)
            if len(p.get('question',''))>2000:raise Fault('Pertanyaan terlalu panjang.')
        super().validate(u,w,action,p)
    def confirm(self,u,pid):
        self.db.execute('BEGIN IMMEDIATE')
        self.defer_commit=True
        try:
            p=self.db.execute('SELECT * FROM plans WHERE id=?',(pid,)).fetchone()
            if not p or p['actor']!=u:raise Fault(UNKNOWN,404)
            result=self._approve(pid)
            # Replace legacy channel only for this exact web confirmation.
            r=self.db.execute('SELECT id,body FROM audit WHERE user=? AND workspace=? ORDER BY id DESC LIMIT 1',(u,p['workspace'])).fetchone()
            body=json.loads(r['body']);body['approval_channel']='authenticated web confirmation'
            if p['action']=='clarify':
                payload=json.loads(p['payload'])
                self.db.execute('INSERT INTO clarifications VALUES(?,?,?,?,?,?,?)',(pid,p['workspace'],payload['brief'],u,p['revision'],payload['question'],now()))
            self.db.execute('UPDATE audit SET body=? WHERE id=?',(dump(body),r['id']));self.db.commit()
            return result
        except Exception:self.db.rollback();raise
        finally:self.defer_commit=False
    def snapshot(self,u,w):
        ws=self.ws(u,w)
        members=[self.profile(r['user'])|{'role':r['role']} for r in self.db.execute('SELECT user,role FROM members WHERE workspace=?',(w,))]
        sources=super().dispatch(u,'sources',{'workspace':w})
        if ws['role']=='manager':
            for s in sources:s['users']=[r['user'] for r in self.db.execute('SELECT user FROM acl WHERE source=?',(s['id'],))]
        analysis=self.analysis(u,w)
        # No raw corpus in workspace response; cite/source endpoints retrieve authorized data on demand.
        analysis['evidence']=[]
        clarifications=[dict(r) for r in self.db.execute('SELECT question,user,brief,created FROM clarifications WHERE workspace=? AND revision=? ORDER BY created',(w,ws['revision']))] if u in (ws['giver'],ws['receiver']) else []
        return {'clarifications':clarifications,'workspace':ws,'members':members,'sources':sources,'analysis':analysis,'briefs':self.list_briefs(u,w)}
