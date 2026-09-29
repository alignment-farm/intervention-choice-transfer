"""Authored invoice/API transfer experiment. Standard-library-only, explicit gold isolation."""
import argparse, calendar, datetime as dt, decimal, hashlib, json, os, platform, random, re, subprocess, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
URL = 'https://mac-studio-7hr7.taile71f88.ts.net/engines/v1/chat/completions'
MODEL = 'docker.io/ai/qwen3:8B-Q4_K_M'
SCALES = {'USD':2,'EUR':2,'GBP':2,'JPY':0,'KWD':3}
GROUPS = ['plain','correction','precision']
SEMANTICS = '''Extract every invoice in first-mention order. Keep cancelled invoices. Apply explicit corrections; preserve all other fields. Copy IDs, vendors and memos exactly, including punctuation and Unicode. Never infer an unknown deadline: use null. Normalize dates to the requested form. Amounts are total invoice amounts, not amounts due after cancellation; retain their amounts. USD/EUR/GBP use 2 decimal places, JPY 0, KWD 3. No extra fields. Return only JSON. /no_think'''
CONTRACTS = {
'canonical': '''Return {"invoices":[{"id":string,"vendor":string,"amount":decimal-string-in-major-currency-units,"currency":currency-code,"due":YYYY-MM-DD-or-null,"status":"open"-or-"cancelled","memo":string}]}. The amount is a JSON string without currency symbol or grouping separators. Example: {"invoices":[{"id":"EX-1","vendor":"Example","amount":"12.30","currency":"USD","due":"2027-02-03","status":"open","memo":"sample"}]}.''',
'v1': '''Return {"invoices":[{"id":string,"vendor":string,"amount_minor":integer,"currency":currency-code,"due":YYYY-MM-DD-or-null,"status":"open"-or-"cancelled","memo":string}]}. Convert amounts to integer minor currency units exactly. Example: {"invoices":[{"id":"EX-1","vendor":"Example","amount_minor":1230,"currency":"USD","due":"2027-02-03","status":"open","memo":"sample"}]}.''',
'v2': '''Return {"invoices":{invoice-id:{"supplier":string,"money":{"units":integer-minor-currency-units,"currency":currency-code},"deadline":{"year":integer,"month":integer,"day":integer}-or-null,"cancelled":boolean,"memo":string}},"order":[invoice-ids-in-first-mention-order]}. The id is the object key, not a field inside its value. Convert amounts to integer minor units exactly. Example: {"invoices":{"EX-1":{"supplier":"Example","money":{"units":1230,"currency":"USD"},"deadline":{"year":2027,"month":2,"day":3},"cancelled":false,"memo":"sample"}},"order":["EX-1"]}.'''
}

def dump(path, value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def cases(seed, per_group):
    rng=random.Random(seed); out=[]
    for group in GROUPS:
        for i in range(per_group):
            rows=[]; prose=[]
            for j in range(2):
                currency=rng.choice(['JPY','KWD']) if group=='precision' else rng.choice(['USD','EUR','GBP'])
                scale=SCALES[currency]; minor=rng.randrange(1,990000)
                amount=format(decimal.Decimal(minor).scaleb(-scale), f'.{scale}f')
                ident=f'INV-{seed}-{i}-{j}-{rng.randrange(10000,99999)}'
                vendor=rng.choice(['Acme & Sons','Müller Studio','North "Star"','O’Neill Labs','A/B Supply'])
                memo=rng.choice(['retain original order','batch "B" / blue','café supplies','no rush; fragile','line A & B'])
                date=dt.date(2027,rng.randrange(1,13),rng.randrange(1,29)) if rng.random()>.3 else None
                status='cancelled' if rng.random()<.35 else 'open'
                row=dict(id=ident,vendor=vendor,amount=amount,currency=currency,due=date.isoformat() if date else None,status=status,memo=memo)
                rows.append(row)
                due=date.strftime('%B %d, %Y') if date else 'unknown'
                if group=='correction':
                    old=format(decimal.Decimal(minor+731).scaleb(-scale),f'.{scale}f')
                    prose.append(f'Invoice {ident}: vendor is {json.dumps(vendor,ensure_ascii=False)}; total {old} {currency}; deadline {due}; status open; memo {json.dumps(memo,ensure_ascii=False)}. Correction for {ident}: total is {amount} {currency}, and final status is {status}. All other fields remain unchanged.')
                else:
                    prose.append(f'Invoice {ident} is from {json.dumps(vendor,ensure_ascii=False)}. Its total is {amount} {currency}. Deadline: {due}. It is {status}. Its memo is {json.dumps(memo,ensure_ascii=False)}.')
            out.append(dict(case_id=f'{seed}-{group}-{i}',source='\n'.join(prose),gold={'invoices':rows},group=group))
    rng.shuffle(out); return out

def visible_group(source):
    if 'Correction for ' in source:return 'correction'
    if re.search(r'\b(?:JPY|KWD)\b',source):return 'precision'
    return 'plain'

def exact_keys(x, keys): return isinstance(x,dict) and set(x)==set(keys)
def iso(x):
    if x is None:return True
    if not isinstance(x,str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}',x):return False
    try:dt.date.fromisoformat(x); return True
    except ValueError:return False

def validate(x, interface):
    try:
        if interface in ('canonical','v1'):
            assert exact_keys(x,['invoices']) and isinstance(x['invoices'],list) and len(x['invoices'])>0
            ids=[]
            for row in x['invoices']:
                money='amount' if interface=='canonical' else 'amount_minor'
                assert exact_keys(row,['id','vendor',money,'currency','due','status','memo'])
                assert all(isinstance(row[k],str) for k in ['id','vendor','currency','status','memo'])
                assert row['currency'] in SCALES and row['status'] in ['open','cancelled'] and iso(row['due'])
                assert row['id'] and row['id'] not in ids; ids.append(row['id'])
                if interface=='v1': assert type(row[money]) is int and row[money]>=0
                else:
                    assert isinstance(row[money],str) and re.fullmatch(r'\d+(?:\.\d+)?',row[money])
                    scaled=decimal.Decimal(row[money]).scaleb(SCALES[row['currency']])
                    assert scaled==scaled.to_integral_value()
        else:
            assert exact_keys(x,['invoices','order']) and isinstance(x['invoices'],dict) and isinstance(x['order'],list)
            assert x['order'] and all(isinstance(s,str) for s in x['order'])
            assert len(set(x['order']))==len(x['order']) and set(x['order'])==set(x['invoices'])
            for row in x['invoices'].values():
                assert exact_keys(row,['supplier','money','deadline','cancelled','memo'])
                assert isinstance(row['supplier'],str) and isinstance(row['memo'],str) and type(row['cancelled']) is bool
                assert exact_keys(row['money'],['units','currency']) and type(row['money']['units']) is int and row['money']['units']>=0 and row['money']['currency'] in SCALES
                if row['deadline'] is not None:
                    assert exact_keys(row['deadline'],['year','month','day'])
                    assert all(type(v) is int for v in row['deadline'].values())
                    dt.date(**row['deadline'])
        return True
    except (AssertionError,KeyError,TypeError,ValueError,decimal.InvalidOperation):return False

def adapt(canonical, interface):
    if not validate(canonical,'canonical'): raise ValueError('invalid canonical extraction')
    rows=[]
    for r in canonical['invoices']:
        row=dict(r); row['amount_minor']=int(decimal.Decimal(row.pop('amount')).scaleb(SCALES[r['currency']]))
        rows.append(row)
    if interface=='v1':return {'invoices':rows}
    return {'invoices':{r['id']:{'supplier':r['vendor'],'money':{'units':r['amount_minor'],'currency':r['currency']},'deadline':dict(zip(['year','month','day'],map(int,r['due'].split('-')))) if r['due'] else None,'cancelled':r['status']=='cancelled','memo':r['memo']} for r in rows},'order':[r['id'] for r in rows]}

def parse(text):
    text=re.sub(r'<think>.*?</think>','',text,flags=re.S).strip()
    if text.startswith('```'): text=re.sub(r'^```(?:json)?\s*|\s*```$','',text)
    return json.loads(text)

def diff(expected, actual, prefix=''):
    if type(expected)!=type(actual):return [prefix+':type']
    if isinstance(expected,dict):
        result=[]
        for k in sorted(set(expected)|set(actual)):
            if k not in expected or k not in actual:result.append(prefix+'/'+str(k)+':key')
            else:result+=diff(expected[k],actual[k],prefix+'/'+str(k))
        return result
    if isinstance(expected,list):
        if len(expected)!=len(actual):return [prefix+':length']
        return sum([diff(a,b,prefix+'/'+str(i)) for i,(a,b) in enumerate(zip(expected,actual))],[])
    return [] if expected==actual else [prefix+':value']

def request(source, action, interface):
    # Deliberately takes source text only. Gold and group are never passed here.
    contract=CONTRACTS['canonical' if action=='C' else interface]
    payload={'model':MODEL,'messages':[{'role':'system','content':SEMANTICS},{'role':'user','content':contract+'\n\nSOURCE:\n'+source}],'temperature':0,'max_tokens':1000,'stream':False}
    started=time.perf_counter()
    req=urllib.request.Request(URL,data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(req,timeout=180) as response:
        body=json.load(response)
    return payload,body,time.perf_counter()-started

def run(args):
    out=ROOT/args.output; out.mkdir(parents=True,exist_ok=True)
    dataset=cases(args.seed,args.per_group)
    if (out/'manifest.json').exists(): raise SystemExit('Refusing to overwrite existing run')
    dump(out/'cases.json',dataset)
    dump(out/'manifest.json',dict(seed=args.seed,per_group=args.per_group,interfaces=args.interfaces,code_sha256=sha(Path(__file__)),protocol_sha256=sha(ROOT/'protocols/phase1.md'),git_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),python=platform.python_version(),started_utc=dt.datetime.now(dt.timezone.utc).isoformat(),model=MODEL,endpoint=URL,policy_sha256=sha(ROOT/'evidence/policy.json') if (ROOT/'evidence/policy.json').exists() else None))
    records=[]
    for case in dataset:
        for interface in args.interfaces:
            for action in ['D','C']:
                start=time.perf_counter()
                record=dict(case_id=case['case_id'],group=visible_group(case['source']),interface=interface,action=action)
                try:
                    payload,response,elapsed=request(case['source'],action,interface)
                    record.update(request=payload,response=response,request_seconds=elapsed)
                    content=response['choices'][0]['message'].get('content') or ''
                    try:
                        intermediate=parse(content); adapter_start=time.perf_counter()
                        actual=adapt(intermediate,interface) if action=='C' else intermediate
                        record['adapter_seconds']=time.perf_counter()-adapter_start
                        record.update(output=actual,valid=validate(actual,interface),differences=diff(adapt(case['gold'],interface),actual))
                        record['success']=record['valid'] and not record['differences']
                    except (ValueError,TypeError,KeyError) as error:record.update(valid=False,success=False,error=repr(error))
                except Exception as error:
                    record.update(transport_error=repr(error),elapsed_seconds=time.perf_counter()-start)
                    with (out/'outcomes.jsonl').open('a') as f:f.write(json.dumps(record,ensure_ascii=False)+'\n')
                    raise
                records.append(record)
                with (out/'outcomes.jsonl').open('a') as f:f.write(json.dumps(record,ensure_ascii=False)+'\n')
                print(json.dumps({k:record[k] for k in ['case_id','interface','action','valid','success','request_seconds']}),flush=True)
    dump(out/'summary.json',summarize(records))

def read_records(path):return [json.loads(x) for x in Path(path).read_text().splitlines()]
def summarize(records):
    out={}
    for interface in sorted({r['interface'] for r in records}):
        for action in ['D','C']:
            rows=[r for r in records if r['interface']==interface and r['action']==action]
            out[interface+'/'+action]=dict(n=len(rows),success=sum(r['success'] for r in rows),valid=sum(r['valid'] for r in rows),prompt_tokens=sum(r['response'].get('usage',{}).get('prompt_tokens',0) for r in rows),completion_tokens=sum(r['response'].get('usage',{}).get('completion_tokens',0) for r in rows),request_seconds=sum(r['request_seconds'] for r in rows))
    return out

def acquire(path):
    rows=read_records(path); assert all(r['interface']=='v1' for r in rows)
    counts={g:{a:{'success':sum(r['success'] for r in rows if r['group']==g and r['action']==a),'n':sum(r['group']==g and r['action']==a for r in rows)} for a in ['D','C']} for g in GROUPS}
    choice={g:max(['D','C'],key=lambda a:counts[g][a]['success']/counts[g][a]['n']) for g in GROUPS}
    global_choice=max(['D','C'],key=lambda a:sum(r['success'] for r in rows if r['action']==a))
    dump(ROOT/'evidence/policy.json',dict(counts=counts,choice=choice,global_choice=global_choice,eligible_outcomes_sha256=sha(Path(path)),tie_break='D',updated_utc=dt.datetime.now(dt.timezone.utc).isoformat()))

def evaluate(path):
    rows=read_records(path); policy=json.loads((ROOT/'evidence/policy.json').read_text()); grouped={}
    for r in rows:grouped.setdefault((r['case_id'],r['interface']),{})[r['action']]=r
    totals={}
    for name in ['fixed_D','fixed_C','inherited_category','inherited_global','current_source','schema_aware_reuse','validator_fallback','oracle']:
        selected=[]; additional=[]; decisions=[]
        for (case_id,interface),pair in grouped.items():
            group=pair['D']['group']
            action={'fixed_D':'D','fixed_C':'C','inherited_category':policy['choice'][group],'inherited_global':policy['global_choice'],'current_source':'D' if group=='plain' else 'C','schema_aware_reuse':'C' if interface=='v2' or group!='plain' else 'D','validator_fallback':'D' if pair['D']['valid'] else 'C','oracle':'D' if pair['D']['success'] else 'C'}[name]
            selected.append(pair[action]); decisions.append({'case_id':case_id,'interface':interface,'action':action,'success':pair[action]['success']})
            if name=='validator_fallback' and action=='C':additional.append(pair['D'])
        charged=selected+additional
        totals[name]=dict(n=len(selected),success=sum(r['success'] for r in selected),valid=sum(r['valid'] for r in selected),requests=len(charged),prompt_tokens=sum(r['response']['usage']['prompt_tokens'] for r in charged),completion_tokens=sum(r['response']['usage']['completion_tokens'] for r in charged),decisions=decisions,oracle_not_deployable=name=='oracle')
    dump(Path(path).parent/'policies.json',totals)
    print(json.dumps({k:{a:b for a,b in v.items() if a!='decisions'} for k,v in totals.items()},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest='command',required=True)
    r=sub.add_parser('run'); r.add_argument('--seed',type=int,required=True);r.add_argument('--per-group',type=int,required=True);r.add_argument('--interfaces',nargs='+',choices=['v1','v2'],required=True);r.add_argument('--output',required=True)
    for cmd in ['acquire','evaluate']:
        s=sub.add_parser(cmd);s.add_argument('path')
    args=p.parse_args()
    if args.command=='run':run(args)
    elif args.command=='acquire':acquire(args.path)
    else:evaluate(args.path)
