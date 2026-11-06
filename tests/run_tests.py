import datetime,json,sys,unittest
from pathlib import Path
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'tests'))
class Result(unittest.TextTestResult):
    def __init__(self,*a,**kw):super().__init__(*a,**kw);self.records=[]
    def addSuccess(self,test):super().addSuccess(test);self.records.append({'test':test.id(),'status':'PASS'})
    def addFailure(self,test,err):super().addFailure(test,err);self.records.append({'test':test.id(),'status':'FAIL','detail':self._exc_info_to_string(err,test)})
    def addError(self,test,err):super().addError(test,err);self.records.append({'test':test.id(),'status':'ERROR','detail':self._exc_info_to_string(err,test)})
suite=unittest.defaultTestLoader.discover(str(root/'tests'),pattern='test_*.py')
r=unittest.TextTestRunner(verbosity=2,resultclass=Result).run(suite)
report={'run_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Synthetic core, web auth/ACL/version, model HTTP adapter fixture, scoped WorkBuddy job queue, actual HTTP CLI and MCP stdio protocol. Model replies in tests are fixtures: NOT actual LLM inference, WorkBuddy application use, or official tests','tests':r.testsRun,'passed':r.testsRun-len(r.failures)-len(r.errors),'results':r.records}
(root/'evidence').mkdir(exist_ok=True)
(root/'evidence/test-results.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
text='# Hasil pengujian aktual\n\n'+report['scope']+'\n\nRun UTC: '+report['run_at']+'\n\n'+str(report['passed'])+'/'+str(report['tests'])+' lulus.\n\n| Kasus | Hasil |\n|---|---|\n'+'\n'.join('| '+x['test'].split('.')[-1]+' | '+x['status']+' |' for x in r.records)+'\n\nDataset/test resmi: belum tersedia. Percakapan dan screenshot WorkBuddy: belum diuji/direkam. Browser dan runtime produksi: lihat evidence/browser-mvp.md (MVP), evidence/browser-results.md (versi sebelumnya), dan evidence/production-smoke.json. Deteksi instruksi tersisip memakai pola terbatas dan bukan jaminan keamanan LLM. Tidak ada pengukuran waktu hemat.\n'
(root/'submission/03_test_results.md').write_text(text,encoding='utf-8')
sys.exit(0 if r.wasSuccessful() else 1)
