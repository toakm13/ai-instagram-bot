from __future__ import annotations
import hashlib, json, os, re, subprocess, time, xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import quote, urlparse
from email.utils import parsedate_to_datetime

import requests
import yfinance as yf
from PIL import Image, ImageDraw, ImageFont

TZ = timezone(timedelta(hours=5, minutes=30))
ROOT = Path(__file__).resolve().parent
STATE = ROOT / "data" / "evidyarthee_state.json"
ASSET_DIR = ROOT / "data" / "published_assets"
QUERIES = ["Fed FOMC Federal Reserve interest rates","RBI repo rate monetary policy","SEBI circular market regulation","NSE BSE market rule trading","India major financial market news"]
PRIMARY = ("federalreserve.gov","rbi.org.in","sebi.gov.in","nseindia.com","bseindia.com","gov.in")
TERMS = {"interest rate":.35,"rate decision":.35,"repo rate":.4,"federal reserve":.3,"fomc":.35,"sebi":.3,"rbi":.3,"circular":.25,"regulation":.25,"inflation":.2,"gdp":.2,"tariff":.25,"sanction":.3,"merger":.25,"acquisition":.25,"default":.3}
EDUCATION = [("What is an Index?","An index is a basket that represents a selected group of securities. Nifty 50 and Sensex are examples used to track parts of the Indian equity market."),("What is Market Capitalisation?","Market capitalisation is broadly calculated as share price multiplied by shares outstanding. It is one way to describe the market value of a listed company."),("What is Volatility?","Volatility describes how much an asset's price moves over time. Higher volatility means larger price fluctuations, not a guaranteed direction."),("What is a Bond?","A bond is a debt instrument. An investor lends money to an issuer, which generally promises interest payments and repayment subject to the bond's terms and credit risk."),("What is an ETF?","An ETF is a fund whose units trade on an exchange. Many ETFs aim to track an index or another defined basket of assets.")]
def env(n,d=""): return os.getenv(n,d).strip()
def killed(): return env("EVIDYARTHEE_EMERGENCY_KILL_SWITCH","false").lower() in {"1","true","yes","on"}
def load_state():
    if STATE.exists():
        try:return json.loads(STATE.read_text(encoding="utf-8"))
        except Exception:pass
    return {"fingerprints":[],"runs":[]}
def save_state(s):
    STATE.parent.mkdir(parents=True,exist_ok=True); STATE.write_text(json.dumps(s,ensure_ascii=False,indent=2),encoding="utf-8")
def rss(q):
    u="https://news.google.com/rss/search?q="+quote(q)+"&hl=en-IN&gl=IN&ceid=IN:en"; r=requests.get(u,timeout=20,headers={"User-Agent":"Evidyarthee/1.0"}); r.raise_for_status(); root=ET.fromstring(r.content); out=[]
    for item in root.findall("./channel/item"):
        def t(tag):
            x=item.find(tag); return (x.text or "").strip() if x is not None else ""
        out.append({"title":t("title"),"url":t("link"),"published":t("pubDate"),"source":t("source")})
    return out
def fresh(pub,hours=36):
    try:
        d=parsedate_to_datetime(pub); d=d if d.tzinfo else d.replace(tzinfo=timezone.utc); age=datetime.now(timezone.utc)-d.astimezone(timezone.utc); return timedelta(minutes=-5)<=age<=timedelta(hours=hours)
    except Exception:return False
def primary(url):
    h=urlparse(url).netloc.lower().split(":")[0]; return any(h==p or h.endswith("."+p) for p in PRIMARY)
def news_candidate():
    found=[]; seen=set()
    for q in QUERIES:
        try:rows=rss(q)
        except Exception:continue
        for x in rows:
            if not x["url"] or not fresh(x["published"]):continue
            text=(x["title"]+" "+x["source"]).lower(); score=sum(v for k,v in TERMS.items() if k in text)+(0.2 if primary(x["url"]) else 0)
            if score<.35:continue
            key=hashlib.sha256((re.sub(r"\W+"," ",x["title"].lower())+"|"+urlparse(x["url"]).netloc.lower()).encode()).hexdigest()[:24]
            if key not in seen:seen.add(key); found.append((score,key,x))
    found.sort(key=lambda z:z[0],reverse=True); state=load_state()
    for s,k,x in found:
        if k not in state.get("fingerprints",[]):return k,x
    return None,None
def font(size,bold=False):
    p="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"; return ImageFont.truetype(p,size) if Path(p).exists() else ImageFont.load_default()
def render(title,body,source,path):
    img=Image.new("RGB",(1080,1080),"#F6F9FC"); d=ImageDraw.Draw(img); navy="#0A2342"; blue="#123F70"; yellow="#F5C400"; white="#FFFFFF"; text="#10233F"
    d.rectangle((0,0,1080,150),fill=white); d.text((40,45),"Evidyarthee",font=font(48,True),fill=navy); d.rounded_rectangle((35,170,1045,245),radius=18,fill=blue); d.text((65,190),"FINANCIAL EDUCATION",font=font(34,True),fill=white)
    y=285
    for i,line in enumerate(re.findall(r'.{1,27}(?:\s|$)',title.upper())[:3]):d.text((45,y),line.strip(),font=font(54 if i==0 else 48,True),fill=navy if i%2==0 else yellow); y+=64
    top=max(500,y+25); d.rounded_rectangle((40,top,1040,810),radius=28,fill=white,outline="#D9E3EF",width=3); d.text((70,top+30),"KEY UPDATE",font=font(30,True),fill=blue); by=top+85
    for line in re.findall(r'.{1,60}(?:\s|$)',body)[:11]:d.text((70,by),line.strip(),font=font(27),fill=text); by+=42
    d.rounded_rectangle((40,835,1040,930),radius=20,fill="#FFF2C7"); d.text((65,855),"EDUCATIONAL • NO BUY/SELL RECOMMENDATION",font=font(25,True),fill=navy); d.rectangle((0,950,1080,1080),fill=navy); d.text((40,970),f"Source: {source}",font=font(20,True),fill=white); d.text((760,985),"Evidyarthee",font=font(32,True),fill=yellow)
    path.parent.mkdir(parents=True,exist_ok=True); img.save(path,"PNG",optimize=True)
def market_snapshot():
    out=[]
    for ticker,name in [("^NSEI","NIFTY 50"),("^NSEBANK","NIFTY BANK")]:
        try:
            df=yf.download(ticker,period="5d",interval="1d",auto_adjust=False,progress=False)
            if len(df)>=2:
                close=float(df["Close"].iloc[-1]); prev=float(df["Close"].iloc[-2]); out.append((name,close,close-prev,(close-prev)/prev*100))
        except Exception:pass
    return out
def generate_core(lane):
    snap=market_snapshot()
    if lane=="educational":
        title,body=EDUCATION[len(load_state().get("runs",[]))%len(EDUCATION)]; return title,body,"Evidyarthee educational series"
    if lane=="pre-market":return "Pre-Market: What to Watch Today","Before the session begins, focus on verified market information rather than predictions. "+(" • ".join(f"{n}: {v:,.0f} ({p:+.2f}%)" for n,v,c,p in snap) if snap else "Live index data was unavailable, so no market number is being stated."),"Yahoo Finance market data" if snap else "Data unavailable"
    return "Post-Market: Session Snapshot",(" • ".join(f"{n}: {v:,.0f} ({p:+.2f}%)" for n,v,c,p in snap) if snap else "Market data was unavailable, so no market number is being stated."),"Yahoo Finance market data" if snap else "Data unavailable"
def publish(caption,media_url,when):
    token=env("METRICOOL_USER_TOKEN"); uid=env("METRICOOL_USER_ID"); bid=env("METRICOOL_BLOG_ID","7004285")
    if not token or not uid:return {"ok":False,"error":"Missing Metricool credentials"}
    body={"publicationDate":{"dateTime":when.strftime("%Y-%m-%dT%H:%M:%S"),"timezone":"Asia/Calcutta"},"text":caption,"providers":[{"network":"instagram"},{"network":"facebook"}],"autoPublish":True,"draft":False,"media":[media_url],"instagramData":{"type":"POST","isAiGenerated":True},"facebookData":{"type":"POST"}}; h={"X-Mc-Auth":token,"Content-Type":"application/json","User-Agent":"EvidyartheeLive/1.0"}
    for a in range(1,4):
        try:
            r=requests.post(f"https://app.metricool.com/api/v2/scheduler/posts?userId={quote(uid)}&blogId={quote(bid)}",headers=h,json=body,timeout=45)
            if r.ok:return {"ok":True,"data":r.json(),"attempt":a}
            err=f"HTTP {r.status_code}: {r.text[:400]}"
        except Exception as e:err=str(e)
        if a<3:time.sleep(2**(a-1))
    return {"ok":False,"error":err}
def commit_asset(path):
    subprocess.run(["git","config","user.name","evidyarthee-bot"],check=True); subprocess.run(["git","config","user.email","41898282+github-actions[bot]@users.noreply.github.com"],check=True); subprocess.run(["git","add",str(path)],check=True); subprocess.run(["git","commit","-m","chore: publish Evidyarthee asset"],check=False); subprocess.run(["git","push","origin","HEAD:main"],check=True); return f"https://raw.githubusercontent.com/{env('GITHUB_REPOSITORY')}/main/{path.as_posix()}"
def run(lane):
    if killed():return {"status":"blocked","reason":"Emergency kill switch active"}
    state=load_state()
    if lane=="news":
        key,item=news_candidate()
        if not item:return {"status":"no_material_news"}
        title=item["title"]; body="A fresh market-related development was detected from a current news source. The post is limited to the verified headline and source; unsupported details are intentionally omitted."; source=item["source"] or "Current news source"
    else:key=f"{lane}-{datetime.now(TZ).date()}"; title,body,source=generate_core(lane)
    fp=hashlib.sha256((title+"|"+body+"|"+source).encode()).hexdigest(); asset=ASSET_DIR/(fp[:24]+".png")
    if fp in state.get("fingerprints",[]) or asset.exists():return {"status":"duplicate","lane":lane}
    render(title,body,source,asset)
    if asset.stat().st_size>8*1024*1024:return {"status":"blocked","reason":"Asset too large"}
    media=commit_asset(asset); when=datetime.now(TZ)+timedelta(minutes=2); caption=f"📌 {title}\n\n{body}\n\nयह educational market content है, buy/sell recommendation नहीं।\n\nSource: {source}\n#Evidyarthee #FinancialEducation #MarketUpdate"; result=publish(caption,media,when)
    state.setdefault("fingerprints",[]).append(fp); state.setdefault("runs",[]).append({"at":datetime.now(TZ).isoformat(),"lane":lane,"status":"queued" if result.get("ok") else "failed","metricool":result}); save_state(state); return {"status":"queued" if result.get("ok") else "failed","lane":lane,"metricool":result,"publish_at":when.isoformat()}
if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser(); p.add_argument("lane",choices=["pre-market","educational","post-market","news"]); a=p.parse_args(); print(json.dumps(run(a.lane),ensure_ascii=False,indent=2)); raise SystemExit(0)
