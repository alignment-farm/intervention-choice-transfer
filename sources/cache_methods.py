import datetime,hashlib,http.client,json,pathlib,time
out=pathlib.Path(__file__).parent
conn=http.client.HTTPSConnection('arxiv.org',timeout=30); records=[]
for key in ['2501.10868v1','2602.14743v1']:
 start=time.monotonic(); path='/html/'+key
 conn.request('GET',path,headers={'User-Agent':'intervention-choice-transfer/0.1 (serial versioned methods inspection)'})
 r=conn.getresponse();data=r.read();(out/(key+'.html')).write_bytes(data)
 records.append({'url':'https://arxiv.org'+path,'status':r.status,'sha256':hashlib.sha256(data).hexdigest(),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
 time.sleep(max(3-(time.monotonic()-start),float(r.getheader('Retry-After','0'))))
conn.close();(out/'method-cache.json').write_text(json.dumps(records,indent=2)+'\n');print(json.dumps(records))
