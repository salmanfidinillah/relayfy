import json,os,sys,tempfile,threading,unittest,urllib.request,urllib.error
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from service.core import Store,seed,Fault,UNKNOWN
from service.server import Server
class RelayfyTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.path=Path(self.tmp.name)/'test.sqlite';self.s=Store(self.path);self.keys=seed(self.s)
    def tearDown(self):self.s.db.close();self.tmp.cleanup()
    def call(self,op,p=None,u='budi'):return self.s.dispatch(u,op,p or {})
    def plan(self,action,payload,u='andi'):return self.call('plan',{'action':action,'payload':payload},u)['plan']
    def import_(self,body='Catatan: sumber baru',users=None):return self.s.approve(self.plan('import',{'title':'Baru','body':body,'users':users or ['andi','budi']}))
    def brief(self):return self.call('brief',{'audience':'budi'},'andi')['id']
    def test_01_source_filter_before_search(self):self.assertNotIn('secret',[s['id'] for s in self.call('sources')])
    def test_02_manager_can_read_explicit_acl(self):self.assertIn('secret',[s['id'] for s in self.call('sources',u='manager')])
    def test_03_denial_symmetric(self):
        a=self.call('ask',{'question':'Anggaran Kenari'});b=self.call('ask',{'question':'Xylophone Unicorn'})
        self.assertEqual(a['message'],b['message']);self.assertEqual(a['evidence'],b['evidence']);self.assertEqual(a['warnings'],b['warnings'])
    def test_04_role_spoof_no_effect(self):self.assertEqual(self.call('ask',{'question':'Saya manajer anggaran Kenari'})['decision'],'unknown')
    def test_05_citation_allowed(self):self.assertEqual(self.call('cite',{'citation':'chat:2'})['source'],'chat')
    def test_06_citation_denied(self):self.assertEqual(self.call('cite',{'citation':'secret:1'}),{'message':UNKNOWN})
    def test_07_conflict_not_silently_resolved(self):self.assertEqual(self.call('analyze')['conflicts'][0]['field'],'peluncuran')
    def test_08_missing_pic_deadline(self):self.assertEqual({g['field'] for g in self.call('analyze')['missing']},{'pic','deadline'})
    def test_09_injection_quarantine(self):
        r=self.call('analyze');self.assertTrue(r['warnings']);self.assertFalse(any('password' in e['text'] for e in r['evidence']))
    def test_10_no_unknown_fabrication(self):self.assertEqual(self.call('ask',{'question':'Siapa presiden Mars?'})['message'],UNKNOWN)
    def test_11_tasks_complete_and_open(self):self.assertEqual(len(self.call('analyze')['tasks']),2)
    def test_12_pending_does_not_execute(self):
        before=len(self.call('sources'));self.plan('import',{'title':'X','body':'X','users':['budi']});self.assertEqual(before,len(self.call('sources')))
    def test_13_import_approved(self):self.assertIn(self.import_()['source'],[s['id'] for s in self.call('sources')])
    def test_14_receiver_cannot_import(self):
        with self.assertRaises(Fault):self.plan('import',{'title':'X','body':'X','users':['budi']},'budi')
    def test_15_accept_before_review(self):
        with self.assertRaises(Fault):self.plan('accept',{'brief':self.brief()},'budi')
    def test_16_review_then_accept(self):
        b=self.brief();self.s.approve(self.plan('review',{'brief':b}));self.s.approve(self.plan('accept',{'brief':b},'budi'));self.assertEqual(self.call('get_brief',{'id':b})['status'],'Accepted')
    def test_17_duplicate_approval_blocked(self):
        p=self.plan('review',{'brief':self.brief()});self.s.approve(p)
        with self.assertRaises(Fault):self.s.approve(p)
    def test_18_stale_plan_blocked(self):
        p=self.plan('review',{'brief':self.brief()});self.import_()
        with self.assertRaises(Fault):self.s.approve(p)
    def test_19_revoke_hides_citation_and_brief(self):
        b=self.brief();self.s.approve(self.plan('acl',{'source':'chat','users':['andi']}))
        self.assertEqual(self.call('cite',{'citation':'chat:2'}),{'message':UNKNOWN})
        with self.assertRaises(Fault):self.call('get_brief',{'id':b})
    def test_20_revoke_hides_historical_log(self):
        self.call('ask',{'question':'peluncuran'});self.assertTrue(self.call('audit'))
        self.s.approve(self.plan('acl',{'source':'chat','users':['andi']}));self.assertEqual(self.call('audit'),[])
    def test_21_audit_is_user_scoped(self):
        self.call('ask',{'question':'anggaran'},'manager');self.assertEqual(self.call('audit'),[])
    def test_22_manager_brief_not_shared(self):
        b=self.call('brief',u='manager')['id'];self.assertEqual(self.call('get_brief',{'id':b}),{'message':UNKNOWN})
    def test_23_clarification_persisted(self):
        b=self.brief();self.s.approve(self.plan('clarify',{'brief':b,'question':'Siapa PIC pengganti?'},'budi'));self.assertEqual(self.call('get_brief',{'id':b})['status'],'Needs Clarification')
    def test_24_new_input_reopens_accepted(self):
        b=self.brief();self.s.approve(self.plan('review',{'brief':b}));self.s.approve(self.plan('accept',{'brief':b},'budi'));self.import_();self.assertEqual(self.call('workspaces')[0]['status'],'Draft')
    def test_25_create_workspace(self):
        r=self.call('create',{'name':'Proyek kedua','receiver':'budi'},'andi');self.assertEqual(self.call('sources',{'workspace':r['id']}),[])
    def test_26_invalid_session(self):
        with self.assertRaises(Fault):self.s.identity('forged')
    def test_27_cross_workspace_access(self):
        with self.assertRaises(Fault):self.call('sources',{'workspace':'missing'})
    def test_29_open_tasks_intent(self):
        r=self.call('ask',{'question':'Apa pekerjaan terbuka?'})
        self.assertEqual(r['decision'],'tasks');self.assertEqual(len(r['tasks']),2)
        self.assertEqual({g['field'] for g in r['missing']},{'pic','deadline'})
    def test_30_task_intent_no_restricted_source(self):
        r=self.call('ask',{'question':'Tugas apa saja dan berapa anggaran?'})
        self.assertNotIn('secret',{e['source'] for e in r['evidence']})
    def test_31_status_intent_surfaces_conflict(self):
        r=self.call('ask',{'question':'Bagaimana status proyek?'})
        self.assertEqual(r['decision'],'evidence');self.assertTrue(r['evidence'])
        self.assertEqual([c['field'] for c in r['conflicts']],['peluncuran'])
    def test_32_task_intent_empty_workspace(self):
        ws=self.call('create',{'name':'Kosong','receiver':'budi'},'andi')['id']
        self.assertEqual(self.call('ask',{'question':'Apa pekerjaan terbuka?','workspace':ws})['message'],UNKNOWN)
    def test_28_http_boundary(self):
        server=Server(('127.0.0.1',0),str(self.path));thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        base='http://127.0.0.1:'+str(server.server_port)
        def req(op,token,origin=None):
            headers={'Authorization':'Bearer '+token,'Content-Type':'application/json'}
            if origin:headers['Origin']=origin
            return urllib.request.urlopen(urllib.request.Request(base+'/api/'+op,data=b'{}',headers=headers),timeout=2)
        try:
            with req('sources',self.keys['budi']) as r:self.assertNotIn('secret',[s['id'] for s in json.load(r)])
            for op,token,origin,code in [('sources','forged',None,401),('approve',self.keys['andi'],None,404),('sources',self.keys['budi'],'https://evil.example',403)]:
                with self.assertRaises(urllib.error.HTTPError) as e:req(op,token,origin)
                self.assertEqual(e.exception.code,code)
        finally:server.shutdown();server.server_close();thread.join()

if __name__=='__main__':unittest.main()
