import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from source_parser import extract
class ParserTests(unittest.TestCase):
 def test_correction(self):
  source='Invoice A-7: vendor is "Müller & \\\"Sons\\\""; total 19.231 KWD; deadline unknown; status open; memo "fragile; retain". Correction for A-7: total is 18.005 KWD, and final status is cancelled. All other fields remain unchanged.'
  self.assertEqual(extract(source),{'invoices':[dict(id='A-7',vendor='Müller & "Sons"',amount='18.005',currency='KWD',due=None,status='cancelled',memo='fragile; retain')]})
 def test_plain(self):
  source='Invoice B is from "O’Neill". Its total is 57 JPY. Deadline: February 29, 2028. It is open. Its memo is "café".'
  self.assertEqual(extract(source)['invoices'][0]['due'],'2028-02-29')
  self.assertEqual(extract(source)['invoices'][0]['amount'],'57')
 def test_abstain(self):
  for source in ['Pay Alice twelve dollars tomorrow.','','Invoice A is from "V". Its total is 1.12 JPY. Deadline: unknown. It is open. Its memo is "m".']:
   with self.assertRaises(ValueError):extract(source)
if __name__=='__main__':unittest.main()
