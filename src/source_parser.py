"""Source-only baseline for the disclosed authored input grammar, with abstention."""
import argparse, datetime as dt, json, re, time
from pathlib import Path
from experiment import ROOT, adapt, cases, dump, sha, validate

STRING = r'"(?:[^"\\]|\\.)*"'
DATE = r'(?:[A-Za-z]+ \d{2}, \d{4}|unknown)'
MONEY = r'(?P<amount>\d+(?:\.\d+)?) (?P<currency>USD|EUR|GBP|JPY|KWD)'
PLAIN = re.compile(r'Invoice (?P<id>\S+) is from (?P<vendor>'+STRING+r')\. Its total is '+MONEY+r'\. Deadline: (?P<due>'+DATE+r')\. It is (?P<status>open|cancelled)\. Its memo is (?P<memo>'+STRING+r')\.')
CORRECTION = re.compile(r'Invoice (?P<id>\S+): vendor is (?P<vendor>'+STRING+r'); total \d+(?:\.\d+)? (?:USD|EUR|GBP|JPY|KWD); deadline (?P<due>'+DATE+r'); status open; memo (?P<memo>'+STRING+r')\. Correction for (?P=id): total is '+MONEY+r', and final status is (?P<status>open|cancelled)\. All other fields remain unchanged\.')

def extract(source):
    rows=[]
    for line in source.splitlines():
        match=PLAIN.fullmatch(line) or CORRECTION.fullmatch(line)
        if not match:raise ValueError('outside supported grammar')
        row=match.groupdict();row['vendor']=json.loads(row['vendor']);row['memo']=json.loads(row['memo'])
        row['due']=None if row['due']=='unknown' else dt.datetime.strptime(row['due'],'%B %d, %Y').date().isoformat()
        rows.append(row)
    result={'invoices':rows}
    if not validate(result,'canonical'):raise ValueError('invalid parsed invoice')
    return result

def run(output, fresh):
    out=ROOT/output
    if out.exists():raise SystemExit('Refusing overwrite')
    out.mkdir(parents=True)
    data=cases(440,6) if fresh else sum([json.loads((ROOT/'evidence'/p/'cases.json').read_text()) for p in ['development','acquisition','confirmation']],[])
    dump(out/'cases.json',data)
    dump(out/'manifest.json',{'fresh':fresh,'seed':440 if fresh else None,'parser_sha256':sha(Path(__file__)),'harness_sha256':sha(ROOT/'src/experiment.py'),'protocol_sha256':sha(ROOT/'protocols/followup.md'),'participant_model_calls':0,'gold_access':'Scoring only. extract() argument is source string.'})
    results=[]
    # Expected payload from separately implemented oracle in audit.py.
    from audit import independent_expected
    for case in data:
        for interface in ['v1','v2']:
            start=time.perf_counter()
            actual=adapt(extract(case['source']),interface)
            duration=time.perf_counter()-start
            results.append({'case_id':case['case_id'],'interface':interface,'output':actual,'success':actual==independent_expected(case,interface),'seconds':duration})
    dump(out/'outcomes.json',results)
    dump(out/'summary.json',{'n':len(results),'success':sum(r['success'] for r in results),'source_cases':len(data),'model_calls':0,'prompt_tokens':0,'completion_tokens':0,'parser_and_adapter_seconds':sum(r['seconds'] for r in results)})
    print((out/'summary.json').read_text())
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--fresh',action='store_true');args=p.parse_args();run(args.output,args.fresh)
