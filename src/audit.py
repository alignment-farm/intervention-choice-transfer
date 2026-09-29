"""Offline claim audit: independently reconstruct fields and policy decisions."""
import datetime as dt, decimal, hashlib, json, sys
from pathlib import Path
from experiment import GROUPS, ROOT, adapt, diff, dump, read_records, summarize, validate

def independent_expected(case,interface):
    # Deliberately do not call adapt: guard against shared adapter/oracle errors.
    rows=[]
    for r in case['gold']['invoices']:
        scale={'JPY':1,'KWD':1000}.get(r['currency'],100)
        value=decimal.Decimal(r['amount'])*scale
        assert value==int(value)
        if interface=='v1':rows.append({'id':r['id'],'vendor':r['vendor'],'amount_minor':int(value),'currency':r['currency'],'due':r['due'],'status':r['status'],'memo':r['memo']})
        else:
            day=dt.date.fromisoformat(r['due']) if r['due'] else None
            rows.append((r['id'],{'supplier':r['vendor'],'money':{'units':int(value),'currency':r['currency']},'deadline':{'day':day.day,'month':day.month,'year':day.year} if day else None,'cancelled':r['status']=='cancelled','memo':r['memo']}))
    return {'invoices':rows} if interface=='v1' else {'invoices':dict(rows),'order':[x[0] for x in rows]}

def main():
    checks=[];all_records=[];seen_ids=set()
    for name,count in [('development',24),('acquisition',24),('confirmation',36)]:
        path=ROOT/'evidence'/name; cases=json.loads((path/'cases.json').read_text());rows=read_records(path/'outcomes.jsonl')
        assert len(rows)==count
        local_ids={r['id'] for c in cases for r in c['gold']['invoices']};assert not seen_ids&local_ids;seen_ids|=local_ids
        by_id={c['case_id']:c for c in cases};assert len({(r['case_id'],r['interface'],r['action']) for r in rows})==count
        for r in rows:
            expected=independent_expected(by_id[r['case_id']],r['interface']);assert expected==adapt(by_id[r['case_id']]['gold'],r['interface'])
            assert r['success']==(validate(r.get('output'),r['interface']) and r.get('output')==expected)
            # Request must contain source and no serialized expected object/feedback.
            assert len(r['request']['messages'])==2
            assert r['request']['messages'][1]['content'].endswith(by_id[r['case_id']]['source'])
            assert r['response']['choices'][0]['finish_reason']=='stop'
        assert summarize(rows)==json.loads((path/'summary.json').read_text())
        all_records+=rows;checks.append(name+': independent gold/scoring, complete run, source isolation, no truncation, unique cohort IDs')
    acquisition=read_records(ROOT/'evidence/acquisition/outcomes.jsonl');policy=json.loads((ROOT/'evidence/policy.json').read_text())
    assert policy['eligible_outcomes_sha256']==hashlib.sha256((ROOT/'evidence/acquisition/outcomes.jsonl').read_bytes()).hexdigest()
    for group in GROUPS:
        rates={a:sum(r['success'] for r in acquisition if r['group']==group and r['action']==a)/sum(r['group']==group and r['action']==a for r in acquisition) for a in ['D','C']}
        assert policy['choice'][group]==('C' if rates['C']>rates['D'] else 'D')
    manifest=json.loads((ROOT/'evidence/confirmation/manifest.json').read_text())
    assert manifest['policy_sha256']==hashlib.sha256((ROOT/'evidence/policy.json').read_bytes()).hexdigest()
    checks.append('policy acquired solely from old-interface records and byte-identical to pre-confirmation manifest')
    for filename in ['policies.json','repaired-policies.json']:
        results=json.loads((ROOT/'evidence/confirmation'/filename).read_text())
        for name,row in results.items():
            assert row['success']==sum(x['success'] for x in row['decisions'])
            assert row['n']==len(row['decisions'])==18
    parser_dir=ROOT/'evidence/parser-confirmation'
    parser_cases=json.loads((parser_dir/'cases.json').read_text())
    parser_rows=json.loads((parser_dir/'outcomes.json').read_text())
    assert len(parser_cases)==18 and len(parser_rows)==36
    assert not seen_ids & {r['id'] for c in parser_cases for r in c['gold']['invoices']}
    parser_by_id={c['case_id']:c for c in parser_cases}
    for r in parser_rows:
        assert r['success'] and r['output']==independent_expected(parser_by_id[r['case_id']],r['interface'])
    parser_manifest=json.loads((parser_dir/'manifest.json').read_text())
    assert parser_manifest['parser_sha256']==hashlib.sha256((ROOT/'src/source_parser.py').read_bytes()).hexdigest()
    assert parser_manifest['participant_model_calls']==0
    checks.append('fresh source-parser cohort: 36 exact tasks, disjoint IDs, independently reconstructed gold, frozen parser hash')
    dump(ROOT/'evidence/audit.json',{'passed':checks,'actual_calls':len(all_records),'actual_prompt_tokens':sum(r['response']['usage']['prompt_tokens'] for r in all_records),'actual_completion_tokens':sum(r['response']['usage']['completion_tokens'] for r in all_records),'actual_request_seconds':sum(r['request_seconds'] for r in all_records),'audit_scope':'Offline full primary cohort; not an independent investigator review.'})
    print(json.dumps(checks,indent=2))
if __name__=='__main__':main()
