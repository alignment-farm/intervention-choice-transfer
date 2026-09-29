"""A source-only ordinary repair, frozen after development and before confirmation."""
import copy, json, re, sys, time
from pathlib import Path
from experiment import adapt, diff, dump, read_records, validate

def repair(source, output, interface):
    result=copy.deepcopy(output)
    if interface!='v2' or not isinstance(result,dict) or not isinstance(result.get('invoices'),dict): return result
    ids=re.findall(r'^Invoice ([^\s:]+)',source,re.M)
    if ids and len(ids)==len(set(ids)) and set(ids)==set(result['invoices']):result['order']=ids
    return result

def evaluate(path):
    path=Path(path);cases={x['case_id']:x for x in json.loads((path.parent/'cases.json').read_text())}
    records=read_records(path);patched=[]
    for record in records:
        r=copy.deepcopy(record);case=cases[r['case_id']]
        start=time.perf_counter();actual=repair(case['source'],r.get('output'),r['interface']);elapsed=time.perf_counter()-start
        r.update(output=actual,valid=validate(actual,r['interface']),differences=diff(adapt(case['gold'],r['interface']),actual),repair_seconds=elapsed)
        r['success']=r['valid'] and not r['differences'];patched.append(r)
    target=path.parent/'repaired-outcomes.jsonl'
    target.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in patched))
    from experiment import evaluate as policies
    policies(target)
    (path.parent/'policies.json').rename(path.parent/'repaired-policies.json')
    policies(path)
    dump(path.parent/'repair-summary.json',{'records':len(patched),'success':sum(r['success'] for r in patched),'cpu_seconds':sum(r['repair_seconds'] for r in patched),'note':'All policies receive same source-only repair; fallback checks post-repair validity.'})

if __name__=='__main__':evaluate(sys.argv[1])
