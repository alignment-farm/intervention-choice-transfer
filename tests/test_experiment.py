import copy, sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from experiment import adapt, cases, diff, validate, visible_group

class ContractTests(unittest.TestCase):
    def test_compiler_known_examples(self):
        x={'invoices':[dict(id='A',vendor='Müller',amount='0.007',currency='KWD',due='2028-02-29',status='cancelled',memo='"') ,dict(id='B',vendor='B',amount='19',currency='JPY',due=None,status='open',memo='x')]}
        v1=adapt(x,'v1');v2=adapt(x,'v2')
        self.assertEqual(v1['invoices'][0]['amount_minor'],7)
        self.assertEqual(v2,{'invoices':{'A':{'supplier':'Müller','money':{'units':7,'currency':'KWD'},'deadline':{'year':2028,'month':2,'day':29},'cancelled':True,'memo':'"'},'B':{'supplier':'B','money':{'units':19,'currency':'JPY'},'deadline':None,'cancelled':False,'memo':'x'}},'order':['A','B']})
    def test_semantic_validity_distinct(self):
        gold=adapt(cases(110,1)[0]['gold'],'v2');bad=copy.deepcopy(gold)
        bad['invoices'][bad['order'][0]]['money']['units']+=1
        self.assertTrue(validate(bad,'v2'));self.assertTrue(diff(gold,bad))
        bad['order'].append(bad['order'][0]);self.assertFalse(validate(bad,'v2'))
    def test_freshness_and_visible_groups(self):
        cohorts=[cases(seed,6) for seed in (110,220,330,440)]
        ids=[r['id'] for cohort in cohorts for c in cohort for r in c['gold']['invoices']]
        self.assertEqual(len(ids),len(set(ids)))
        for cohort in cohorts:
            for c in cohort:
                self.assertEqual(visible_group(c['source']),c['group'])
                for interface in ('v1','v2'):self.assertTrue(validate(adapt(c['gold'],interface),interface))
    def test_invalid_values(self):
        x=cases(110,1)[0]['gold'];x['invoices'][0]['amount']='NaN';self.assertFalse(validate(x,'canonical'))
        x=cases(110,1)[0]['gold'];x['invoices'][0]['due']='2027-02-30';self.assertFalse(validate(x,'canonical'))
if __name__=='__main__':unittest.main()
