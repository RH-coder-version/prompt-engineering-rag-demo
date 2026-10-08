"""Localhost-only API proxy. Never serves private records or credential files."""
import os,json,getpass,secrets,urllib.parse
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from engine import DeepSeek,Experiment,PROTOCOL,judge_messages,validate_response
ROOT=Path(__file__).resolve().parent
TOKEN=secrets.token_urlsafe(32)
API=None;EXPERIMENT=None
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(ROOT),**kwargs)
 def log_message(self,*args):pass
 def reply(self,data,status=200):
  body=json.dumps(data,ensure_ascii=False).encode();self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
 def allowed_host(self):return self.headers.get('Host') in ('127.0.0.1:8766','localhost:8766')
 def do_GET(self):
  if not self.allowed_host():return self.reply({'error':'Invalid host'},403)
  path=urllib.parse.urlparse(self.path).path
  if path=='/api/session':return self.reply({'token':TOKEN,'model':PROTOCOL['generation_model'],'judge':PROTOCOL['judge_model'],'key_configured':True})
  if path=='/api/status':return self.reply(EXPERIMENT.state)
  if path=='/api/results':
   if EXPERIMENT.result:return self.reply(EXPERIMENT.result)
   p=ROOT/'latest-results.json'
   if not p.exists():p=ROOT/'experiment-results.json'
   return self.reply(json.loads(p.read_text(encoding='utf8')) if p.exists() else {'error':'No results yet'})
  name=path.lstrip('/') or 'live.html'
  if '/' in name or name.startswith('.') or Path(name).suffix not in ('.html','.css','.js','.json') or name not in {p.name for p in ROOT.iterdir() if p.is_file()} or name=='latest-results.json':return self.reply({'error':'Not found'},404)
  self.path='/'+name;super().do_GET()
 def do_POST(self):
  if not self.allowed_host() or self.headers.get('Origin') not in (None,'http://127.0.0.1:8766','http://localhost:8766') or self.headers.get('X-Demo-Token')!=TOKEN:return self.reply({'error':'Rejected origin or token'},403)
  try:
   n=int(self.headers.get('Content-Length','0'))
   if n>50000:return self.reply({'error':'Input too large'},413)
   data=json.loads(self.rfile.read(n) or b'{}')
   if self.path=='/api/experiment':return self.reply(EXPERIMENT.start())
   if self.path=='/api/generate':
    prompt=str(data.get('prompt','')).strip()
    if not prompt or len(prompt)>16000:return self.reply({'error':'Invalid prompt'},400)
    res=API.call([{'role':'user','content':prompt}],PROTOCOL['generation_model'],.7,900);return self.reply({'text':res['content'],'model':res['model'],'usage':res['usage'],'id':res['id'],'finish_reason':res['finish_reason']})
   return self.reply({'error':'Unknown action'},404)
  except Exception as e:return self.reply({'error':str(e) if type(e).__name__ in ('ApiError','ValueError') else type(e).__name__},400)
def main():
 global API,EXPERIMENT
 key=os.environ.get('DEEPSEEK_API_KEY') or getpass.getpass('DeepSeek API key (hidden): ')
 API=DeepSeek(key.strip());EXPERIMENT=Experiment(API)
 saved=ROOT/'latest-results.json'
 if not saved.exists():saved=ROOT/'experiment-results.json'
 if saved.exists():
  EXPERIMENT.result=json.loads(saved.read_text(encoding='utf8'))
  EXPERIMENT.state={'status':'complete','done':316,'total':316}
 print('Local demo ready: http://127.0.0.1:8766/live.html',flush=True)
 ThreadingHTTPServer(('127.0.0.1',8766),Handler).serve_forever()
if __name__=='__main__':main()
