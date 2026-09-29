import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from repair_control import repair
class RepairTests(unittest.TestCase):
 def test_only_order(self):
  source='Invoice A is open\nInvoice B: cancelled'
  output={'invoices':{'A':{'x':1},'B':{'x':2}},'order':['A','typo']}
  fixed=repair(source,output,'v2')
  self.assertEqual(fixed['order'],['A','B']);self.assertEqual(fixed['invoices'],output['invoices']);self.assertEqual(output['order'],['A','typo'])
 def test_abstention(self):
  output={'invoices':{'A':{},'C':{}},'order':['A','typo']}
  self.assertEqual(repair('Invoice A is open\nInvoice B: cancelled',output,'v2'),output)
if __name__=='__main__':unittest.main()
