from __future__ import annotations
import hashlib,json,os,subprocess,time
from datetime import datetime,timedelta,timezone
from pathlib import Path
import requests
from PIL import Image,ImageDraw,ImageFont

TZ=timezone(timedelta(hours=5,minutes=30)); ROOT=Path(__file__).resolve().parent
STATE=ROOT/'data'/'evidyarthee_meme_state.json'; ASSETS=ROOT/'data'/'published_assets'/'memes'; TOPICS=ROOT/'meme_topics.json'

def env(n,d=''): return os.getenv(n,d).strip()
def killed(): return env('EVIDYARTHEE_EMERGENCY_KILL_SWITCH','false').lower() in {'1','true','yes','on'}
def load():
    try:return json.loads(STATE.read_text(encoding='utf-8')) if STATE.exists() else {'fingerprints':[],'runs':[]}
    except Exception:return {'fingerprints':[],'runs':[]}
def save(s): STATE.parent.mkdir(parents=True,exist_ok=True); STATE.write_text(json.dumps(s,ensure_ascii=False,indent=2),encoding='utf-8')
def font(n,b=False):
    p='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if b else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; return ImageFont.truetype(p,n)
def render(title,body,path):
    img=Image.new('RGB',(1080,1080),'#F6F9FC'); d=ImageDraw.Draw(img); navy='#0A2342'; blue='#123F70'; yellow='#F5C400'; white='#FFFFFF'; text='#10233F'
    d.rectangle((0,0,1080,150),fill=white); d.text((40,45),'Evidyarthee',font=font(48,1),fill=navy); d.text((820,55),'#FINANCEMEME',font=font(22,1),fill=blue)
    d.rounded_rectangle((35,175,1045,290),radius=22,fill=blue); d.text((65,205),title,font=font(42,1),fill=yellow)
    y=350
    for para in body.split('\n'):
        if not para:y+=22; continue
        line=''
        for word in para.split():
            test=(line+' '+word).strip()
            if d.textbbox((0,0),test,font=font(38))[2]>920:
                d.text((75,y),line,font=font(38,1),fill=text); y+=55; line=word
            else: line=test
        if line:d.text((75,y),line,font=font(38,1),fill=text); y+=55
    d.rounded_rectangle((40,865,1040,935),radius=18,fill='#FFF2C7'); d.text((65,887),'RELATABLE FINANCE • EDUCATIONAL • NO BUY/SELL ADVICE',font=font(22,1),fill=navy)
    d.rectangle((0,960,1080,1080),fill=navy); d.text((40,985),'Evidyarthee',font=font(34,1),fill=yellow); d.text((760,995),'Learn • Relate • Invest',font=font(22,1),fill=white)
    path.parent.mkdir(parents=True,exist_ok=True); img.save(path,'PNG',optimize=True)
def publish(caption,media,when):
    token,uid,bid=env('METRICOOL_USER_TOKEN'),env('METRICOOL_USER_ID'),env('METRICOOL_BLOG_ID','7004285')
    if not token or not uid:return {'ok':False,'error':'Missing Metricool credentials'}
    body={'publicationDate':{'dateTime':when.strftime('%Y-%m-%dT%H:%M:%S'),'timezone':'Asia/Calcutta'},'text':caption,'providers':[{'network':'instagram'},{'network':'facebook'}],'autoPublish':True,'draft':False,'media':[media],'instagramData':{'type':'POST','isAiGenerated':True},'facebookData':{'type':'POST'}}
    h={'X-Mc-Auth':token,'Content-Type':'application/json','User-Agent':'EvidyartheeMemeEngine/2.0'}
    for a in range(1,4):
        try:
            r=requests.post(f'https://app.metricool.com/api/v2/scheduler/posts?userId={uid}&blogId={bid}',headers=h,json=body,timeout=45)
            if r.ok:return {'ok':True,'data':r.json(),'attempt':a}
            err=f'HTTP {r.status_code}: {r.text[:400]}'
        except Exception as e:err=str(e)
        if a<3:time.sleep(2**(a-1))
    return {'ok':False,'error':err}
def commit(path):
    subprocess.run(['git','config','user.name','evidyarthee-bot'],check=True); subprocess.run(['git','config','user.email','41898282+github-actions[bot]@users.noreply.github.com'],check=True); subprocess.run(['git','add',str(path)],check=True); subprocess.run(['git','commit','-m','chore: publish Evidyarthee meme'],check=False); subprocess.run(['git','push','origin','HEAD:main'],check=True); return f"https://raw.githubusercontent.com/{env('GITHUB_REPOSITORY')}/main/{path.as_posix()}"
def choose(state):
    data=json.loads(TOPICS.read_text(encoding='utf-8')); items=[]
    for cat,rows in data['categories'].items():
        for title,body in rows:items.append((cat,title,body))
    start=len(state.get('runs',[]))%len(items)
    for i in range(len(items)):
        cat,title,body=items[(start+i)%len(items)]; fp=hashlib.sha256((title+'|'+body).encode()).hexdigest()
        if fp not in state.get('fingerprints',[]):return cat,title,body,fp
    return None
def run():
    if killed():return {'status':'blocked','reason':'Emergency kill switch active'}
    s=load(); choice=choose(s)
    if not choice:return {'status':'no_new_meme'}
    cat,title,body,fp=choice; asset=ASSETS/f'{fp[:24]}.png'; render(title,body,asset)
    if asset.stat().st_size>8*1024*1024:return {'status':'blocked','reason':'Asset too large'}
    media=commit(asset)
    now=datetime.now(TZ)
    when=now.replace(hour=19,minute=30,second=0,microsecond=0)
    if when <= now: when=now+timedelta(minutes=2)
    caption=f'😂 {title}\n\n{body}\n\nयह relatable finance content है — buy/sell recommendation नहीं.\n\n#Evidyarthee #FinanceMemes #IndianInvestors #PersonalFinance #FinancialEducation #StockMarket'
    result=publish(caption,media,when); s.setdefault('fingerprints',[]).append(fp); s.setdefault('runs',[]).append({'at':datetime.now(TZ).isoformat(),'category':cat,'title':title,'status':'queued' if result.get('ok') else 'failed','metricool':result}); save(s)
    return {'status':'queued' if result.get('ok') else 'failed','category':cat,'title':title,'metricool':result,'publish_at':when.isoformat()}
if __name__=='__main__': print(json.dumps(run(),ensure_ascii=False,indent=2))
