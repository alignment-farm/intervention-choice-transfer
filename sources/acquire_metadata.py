"""One connection, no parallel requests, honor Retry-After; cache every response."""
import datetime, hashlib, http.client, json, pathlib, time
out=pathlib.Path(__file__).parent
path='/api/query?id_list=2501.10868,2303.17651,2602.14743'
conn=http.client.HTTPSConnection('export.arxiv.org',timeout=30)
t=time.monotonic()
try:
 conn.request('GET',path,headers={'User-Agent':'intervention-choice-transfer/0.1 (bounded local scientific study; serial metadata retrieval)'})
 response=conn.getresponse();data=response.read();(out/'arxiv-query.xml').write_bytes(data)
 meta={'url':'https://export.arxiv.org'+path,'status':response.status,'headers':dict(response.getheaders()),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sha256':hashlib.sha256(data).hexdigest()}
 (out/'arxiv-query.json').write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps(meta))
finally:
 conn.close(); time.sleep(max(0,3-(time.monotonic()-t)))
