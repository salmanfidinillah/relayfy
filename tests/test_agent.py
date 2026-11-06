"""WorkBuddy transport tests. Replies are explicit test fixtures, NOT model inference."""
import io,json,sys,time,unittest,subprocess,tempfile,threading
from pathlib import Path
from wsgiref.simple_server import make_server
import test_web
from service.webapp import App
from service.runtime import RuntimeStore
from service.core import Fault,UNKNOWN
from service.model import Model
from web_start import Quiet
ROOT=Path(__file__).resolve().parents[1]

class AgentTests(unittest.TestCase):
    req=test_web.WebTests.req;get=test_web.WebTests.get;post=test_web.WebTests.post;plan=test_web.WebTests.plan;mutate=test_web.WebTests.mutate;brief=test_web.WebTests.brief;reviewed=test_web.WebTests.reviewed
    def setUp(self):
        test_web.WebTests.setUp(self);self.config.ai_backend='workbuddy';self.runtime=RuntimeStore(self.path)
    def tearDown(self):self.runtime.db.close();test_web.WebTests.tearDown(self)
    def pair(self,who='receiver',purpose='ask'):
        c,r,_=self.post('agent_pair',who,purpose=purpose);self.assertEqual(c,200,r);return r
    def worker(self,op,token,p=None,origin=None,remote='127.0.0.1'):
        data=json.dumps(p or {}).encode();env={'PATH_INFO':'/api/worker/'+op,'REQUEST_METHOD':'POST','QUERY_STRING':'','wsgi.input':io.BytesIO(data),'CONTENT_TYPE':'application/json','CONTENT_LENGTH':str(len(data)),'REMOTE_ADDR':remote,'HTTP_AUTHORIZATION':'Bearer '+token}
        if origin:env['HTTP_ORIGIN']=origin
        out={}
        def start(s,h):out['status']=int(s.split()[0])
        raw=b''.join(self.app(env,start));return out['status'],json.loads(raw)
    def enqueue(self,who='receiver',op='ask',q='Mengapa peluncuran tertunda?'):
        c,j,_=self.post(op,who,question=q);self.assertEqual(c,200,j);return j
    def claim(self,who='receiver',purpose='ask',op='ask'):
        config=self.pair(who,purpose);queued=self.enqueue(who,op);c,job=self.worker('next',config['token']);self.assertEqual(c,200,job);return config,queued,job
    def fixture(self,job):
        e=job['data']['evidence'][0]
        return {'unknown':False,'claims':[{'text':e['text'],'citation':e['citation'],'quote':e['text']}],'clarification':''}
    def finish(self,config,job,answer=None):return self.worker('finish',config['token'],{'job':job['job'],'lease':job['lease'],'answer':answer or self.fixture(job)})
    def test_pair_is_scoped_and_key_hashed(self):
        config=self.pair();r=self.runtime.db.execute('SELECT * FROM worker_keys').fetchone();self.assertNotEqual(r['token'],config['token']);self.assertEqual(r['user'],self.r);self.assertEqual(r['purpose'],'ask')
        self.assertNotIn(config['token'],json.dumps(self.get('audit','receiver')[1]))
    def test_unknown_has_no_job_and_no_restricted_existence(self):
        a=self.enqueue(q='Kenari');b=self.enqueue(q='Unicorn')
        self.assertEqual(a['message'],b['message']);self.assertEqual(a['message'],UNKNOWN)
        self.assertFalse(a.get('queued'));self.assertEqual(self.get('jobs','receiver')[1],[])
    def test_real_job_flow_and_revision_history(self):
        config,queued,job=self.claim();self.assertEqual(job['identity']['id'],self.r);self.assertNotIn('RAHASIA',json.dumps(job));self.assertEqual(job['revision'],self.s.ws(self.r,self.w)['revision'])
        self.assertEqual(self.finish(config,job)[0],200)
        c,r,_=self.get('job','receiver',id=queued['job']);self.assertEqual(c,200);self.assertEqual(r['status'],'Done');self.assertEqual(r['result']['origin'],'workbuddy_bridge')
        self.assertEqual(len(self.get('history','receiver')[1]),1)
        self.assertIn('agent_completed',json.dumps(self.get('audit','receiver')[1]))
    def test_worker_for_other_account_cannot_claim_or_complete(self):
        own,queued,job=self.claim();other=self.pair('giver')
        self.assertIsNone(self.worker('next',other['token'])[1]['job'])
        self.assertEqual(self.finish(other,job)[0],404)
        self.assertEqual(self.get('job','giver',id=queued['job'])[0],404)
    def test_worker_denies_browser_and_nonloopback(self):
        token=self.pair()['token']
        self.assertEqual(self.worker('next',token,origin='http://localhost')[0],403)
        self.assertEqual(self.worker('next',token,remote='192.0.2.10')[0],403)
        self.assertEqual(self.worker('next','forged')[0],401)
        self.assertEqual(self.worker('approve',token)[0],404)
    def test_forged_citation_and_quote_rejected_no_history(self):
        config,queued,job=self.claim();a=self.fixture(job);a['claims'][0]['citation']='restricted:1'
        self.assertEqual(self.finish(config,job,a)[0],422);self.assertEqual(self.get('history','receiver')[1],[])
        a=self.fixture(job);a['claims'][0]['quote']='Invented'
        self.assertEqual(self.finish(config,job,a)[0],422)
    def test_replay_and_wrong_lease_rejected(self):
        config,queued,job=self.claim();bad=job|{'lease':'wrong'}
        self.assertEqual(self.finish(config,bad)[0],409);self.assertEqual(self.finish(config,job)[0],200);self.assertEqual(self.finish(config,job)[0],409)
    def test_revocation_invalidates_pair_job_history_and_payload(self):
        config,queued,job=self.claim();self.mutate('acl',{'source':self.shared,'users':[self.g]})
        self.assertEqual(self.worker('next',config['token'])[0],409);self.assertEqual(self.finish(config,job)[0],409)
        self.assertEqual(self.get('job','receiver',id=queued['job'])[0],409)
        self.assertEqual(self.get('jobs','receiver')[1],[]);self.assertEqual(self.get('history','receiver')[1],[])
        new=self.pair();self.assertIsNone(self.worker('next',new['token'])[1]['job'])
        self.assertEqual(self.enqueue(q='peluncuran')['message'],UNKNOWN)
    def test_pair_rotation_invalidates_old_key_and_lease(self):
        config,queued,job=self.claim();new=self.pair()
        self.assertEqual(self.finish(config,job)[0],401)
        c,newjob=self.worker('next',new['token']);self.assertEqual(c,200);self.assertEqual(newjob['job'],job['job']);self.assertNotEqual(newjob['lease'],job['lease'])
        self.assertEqual(self.finish(new,job)[0],409);self.assertEqual(self.finish(new,newjob)[0],200)
    def test_brief_job_private_until_human_review(self):
        config,queued,job=self.claim('giver','brief','generate');self.assertEqual(job['mode'],'brief');self.assertNotIn('RAHASIA',json.dumps(job))
        self.assertEqual(self.finish(config,job)[0],200);c,j,_=self.get('job',id=queued['job']);bid=j['result']['brief']
        self.assertEqual(self.get('brief','receiver',id=bid)[0],404);self.assertEqual(self.get('workspace')[1]['briefs'][0]['kind'],'workbuddy')
        self.mutate('review',{'brief':bid});self.mutate('accept',{'brief':bid},'receiver');self.assertEqual(self.get('workspace','receiver')[1]['workspace']['status'],'Accepted')
    def test_context_purpose_separates_private_ask_and_recipient_brief(self):
        config=self.pair('giver','ask');self.enqueue('giver','generate')
        self.assertIsNone(self.worker('next',config['token'])[1]['job'])
        self.assertEqual(self.post('agent_pair','receiver',purpose='brief')[0],403)
    def test_failed_worker_no_fake_success(self):
        config,queued,job=self.claim();c,r=self.worker('finish',config['token'],{'job':job['job'],'lease':job['lease'],'failed':True});self.assertEqual(c,200);self.assertEqual(r['status'],'Failed')
        self.assertEqual(self.get('job','receiver',id=queued['job'])[1]['status'],'Failed');self.assertEqual(self.get('history','receiver')[1],[])
    def test_cancel_processing_invalidates_result(self):
        config,queued,job=self.claim();self.assertEqual(self.post('cancel_job','receiver',id=queued['job'])[0],200)
        self.assertEqual(self.finish(config,job)[0],409);self.assertEqual(self.get('history','receiver')[1],[])
    def test_pending_limit_and_other_account_cancel(self):
        one=self.enqueue();self.enqueue();self.enqueue()
        self.assertEqual(self.post('ask','receiver',question='peluncuran')[0],429)
        self.assertEqual(self.post('cancel_job','giver',id=one['job'])[0],404)
    def test_extractive_fallback_is_labeled_without_ai(self):
        r=self.post('ask','receiver',question='peluncuran',answer_mode='evidence')[1]
        self.assertEqual(r['origin'],'retrieval');self.assertFalse(r['provider_called']);self.assertTrue(r['evidence']);self.assertEqual(r['claims'],[])
    def test_job_expired_lease_can_be_reclaimed(self):
        config,queued,job=self.claim();self.runtime.db.execute('UPDATE agent_jobs SET lease_until=0 WHERE id=?',(job['job'],));self.runtime.db.commit()
        self.assertEqual(self.finish(config,job)[0],409);c,retry=self.worker('next',config['token']);self.assertEqual(c,200);self.assertNotEqual(retry['lease'],job['lease'])
    def test_finish_transaction_rolls_back_when_audit_fails(self):
        config,queued,job=self.claim();key=self.runtime.worker(config['token']);original=self.runtime.log
        def fail(*a):raise RuntimeError('synthetic audit failure')
        self.runtime.log=fail
        with self.assertRaises(RuntimeError):self.runtime.finish_job(key,{'job':job['job'],'lease':job['lease'],'answer':self.fixture(job)})
        self.runtime.log=original
        self.assertEqual(self.get('history','receiver')[1],[]);self.assertEqual(self.get('job','receiver',id=queued['job'])[1]['status'],'Processing')
    def test_context_preparation_revision_cannot_be_reused(self):
        context=self.runtime.prepare(self.r,self.w,'ask',{'question':'peluncuran'});self.mutate('import',{'title':'new','body':'new','users':[self.g,self.r]})
        with self.assertRaises(Fault):self.runtime.enqueue(self.r,self.w,context)
    def test_actual_http_cli_and_mcp_tools_with_fixture_reply(self):
        server=make_server('127.0.0.1',0,self.app,handler_class=Quiet);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            config=self.pair();config['url']='http://127.0.0.1:'+str(server.server_port);queued=self.enqueue()
            cfg=Path(self.tmp.name)/'connection.json';cfg.write_text(json.dumps(config))
            cli=[sys.executable,str(ROOT/'relayfy-agent/client.py')]
            r=subprocess.run(cli+['next','--config',str(cfg)],capture_output=True,text=True,timeout=10);self.assertEqual(r.returncode,0,r.stderr);job=json.loads(r.stdout)
            reply=Path(self.tmp.name)/'reply.json';reply.write_text(json.dumps({'job':job['job'],'lease':job['lease'],'answer':self.fixture(job)}))
            r=subprocess.run(cli+['finish','--config',str(cfg),'--file',str(reply)],capture_output=True,text=True,timeout=10);self.assertEqual(r.returncode,0,r.stderr)
            messages=[{'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-03-26'}},{'jsonrpc':'2.0','method':'notifications/initialized'},{'jsonrpc':'2.0','id':2,'method':'tools/list'},{'jsonrpc':'2.0','id':3,'method':'tools/call','params':{'name':'relayfy_status','arguments':{}}}]
            r=subprocess.run([sys.executable,str(ROOT/'relayfy-agent/server.py'),'--config',str(cfg)],input='\n'.join(json.dumps(m) for m in messages)+'\n',capture_output=True,text=True,timeout=10);self.assertEqual(r.returncode,0,r.stderr)
            rows=[json.loads(line) for line in r.stdout.splitlines()];self.assertEqual(len(rows),3);self.assertEqual(rows[0]['result']['protocolVersion'],'2025-03-26');self.assertEqual(len(rows[1]['result']['tools']),4);self.assertFalse(rows[2]['result']['isError']);self.assertNotIn(config['token'],r.stdout)
            self.assertEqual(self.get('job','receiver',id=queued['job'])[1]['status'],'Done')
        finally:server.shutdown();server.server_close();thread.join()
    def test_demo_disabled_by_default_and_synthetic_profiles_seed_once(self):
        self.assertEqual(self.req('profiles')[0],404);self.assertEqual(self.req('demo-login',{'profile':'andi'})[0],404)
        self.config.demo_mode=True;self.runtime.seed_demo();self.runtime.seed_demo()
        c,profiles,_=self.req('profiles');self.assertEqual(c,200);self.assertEqual(len(profiles),4)
        c,r,h=self.req('demo-login',{'profile':'maya'});self.assertEqual(c,200);self.assertEqual(r['user']['id'],'demo-maya')
        self.assertNotIn('karsa-commercial',[s['id'] for s in self.runtime.visible('demo-maya','demo-karsa')]);self.assertIn('karsa-commercial',[s['id'] for s in self.runtime.visible('demo-dewi','demo-karsa')])
        self.assertEqual(self.req('demo-login',{'profile':'admin','role':'manager'})[0],404)
        self.config.production=True
        with self.assertRaises(RuntimeError):App(self.config)
        self.config.production=False
