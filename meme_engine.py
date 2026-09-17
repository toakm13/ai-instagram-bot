from __future__ import annotations

import hashlib
import json
import os
import subprocess
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests
from PIL import Image, ImageDraw, ImageFont

TZ = timezone(timedelta(hours=5, minutes=30))
ROOT = Path(__file__).resolve().parent
STATE = ROOT / "data" / "evidyarthee_meme_state.json"
ASSET_DIR = ROOT / "data" / "published_assets" / "memes"

# Original, text-first finance situations. No copyrighted meme templates are downloaded.
TEMPLATES = [
    ("SALARY DAY", "Salary credited 💰\nRent: gone\nEMI: gone\nBills: gone\n\nMe: This month I will definitely invest more."),
    ("WHEN THE MARKET MOVES", "Market moves 0.3%\n\nOption premium:\nI have decided to experience\nevery emotion today."),
    ("BULL MARKET LOGIC", "Friend: Bro, this stock is going up.\n\nMe: What's the business?\n\nFriend: It's going up."),
    ("LONG-TERM INVESTOR", "Portfolio: -2%\nMe: It's a long-term investment 😌\n\nPortfolio: +2%\nMe: Should I book profit? 🤔"),
    ("FOMO CHECK", "Friend: Everyone is buying this.\n\nMe: What's the reason?\n\nFriend: Everyone is buying it."),
]


def env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


def killed() -> bool:
    return env("EVIDYARTHEE_EMERGENCY_KILL_SWITCH", "false").lower() in {"1", "true", "yes", "on"}


def load_state() -> dict:
    if STATE.exists():
        try:
            return json.loads(STATE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"fingerprints": [], "runs": []}


def save_state(state: dict) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def font(size: int, bold: bool = False):
    path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(path, size) if Path(path).exists() else ImageFont.load_default()


def render(title: str, body: str, path: Path) -> None:
    img = Image.new("RGB", (1080, 1080), "#F6F9FC")
    draw = ImageDraw.Draw(img)
    navy, blue, yellow, white, text = "#0A2342", "#123F70", "#F5C400", "#FFFFFF", "#10233F"

    draw.rectangle((0, 0, 1080, 150), fill=white)
    draw.text((40, 45), "Evidyarthee", font=font(48, True), fill=navy)
    draw.text((820, 55), "#FINANCEMEME", font=font(22, True), fill=blue)

    draw.rounded_rectangle((35, 175, 1045, 290), radius=22, fill=blue)
    draw.text((65, 205), title, font=font(42, True), fill=yellow)

    y = 350
    for paragraph in body.split("\n"):
        if not paragraph:
            y += 22
            continue
        words = paragraph.split()
        line = ""
        for word in words:
            test = f"{line} {word}".strip()
            if draw.textbbox((0, 0), test, font=font(38))[2] > 920:
                draw.text((75, y), line, font=font(38, True), fill=text)
                y += 55
                line = word
            else:
                line = test
        if line:
            draw.text((75, y), line, font=font(38, True), fill=text)
            y += 55

    draw.rounded_rectangle((40, 865, 1040, 935), radius=18, fill="#FFF2C7")
    draw.text((65, 887), "RELATABLE FINANCE • EDUCATIONAL • NO BUY/SELL ADVICE", font=font(22, True), fill=navy)
    draw.rectangle((0, 960, 1080, 1080), fill=navy)
    draw.text((40, 985), "Evidyarthee", font=font(34, True), fill=yellow)
    draw.text((760, 995), "Learn • Relate • Invest", font=font(22, True), fill=white)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, "PNG", optimize=True)


def publish(caption: str, media_url: str, when: datetime) -> dict:
    token, uid, bid = env("METRICOOL_USER_TOKEN"), env("METRICOOL_USER_ID"), env("METRICOOL_BLOG_ID", "7004285")
    if not token or not uid:
        return {"ok": False, "error": "Missing Metricool credentials"}
    body = {
        "publicationDate": {"dateTime": when.strftime("%Y-%m-%dT%H:%M:%S"), "timezone": "Asia/Calcutta"},
        "text": caption,
        "providers": [{"network": "instagram"}, {"network": "facebook"}],
        "autoPublish": True,
        "draft": False,
        "media": [media_url],
        "instagramData": {"type": "POST", "isAiGenerated": True},
        "facebookData": {"type": "POST"},
    }
    headers = {"X-Mc-Auth": token, "Content-Type": "application/json", "User-Agent": "EvidyartheeMemeEngine/1.0"}
    for attempt in range(1, 4):
        try:
            response = requests.post(f"https://app.metricool.com/api/v2/scheduler/posts?userId={uid}&blogId={bid}", headers=headers, json=body, timeout=45)
            if response.ok:
                return {"ok": True, "data": response.json(), "attempt": attempt}
            error = f"HTTP {response.status_code}: {response.text[:400]}"
        except Exception as exc:
            error = str(exc)
        if attempt < 3:
            time.sleep(2 ** (attempt - 1))
    return {"ok": False, "error": error}


def commit_asset(path: Path) -> str:
    subprocess.run(["git", "config", "user.name", "evidyarthee-bot"], check=True)
    subprocess.run(["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"], check=True)
    subprocess.run(["git", "add", str(path)], check=True)
    subprocess.run(["git", "commit", "-m", "chore: publish Evidyarthee meme"], check=False)
    subprocess.run(["git", "push", "origin", "HEAD:main"], check=True)
    return f"https://raw.githubusercontent.com/{env('GITHUB_REPOSITORY')}/main/{path.as_posix()}"


def run() -> dict:
    if killed():
        return {"status": "blocked", "reason": "Emergency kill switch active"}

    state = load_state()
    # Rotate deterministically so the same meme is never selected twice until the set is exhausted.
    start = len(state.get("runs", [])) % len(TEMPLATES)
    for offset in range(len(TEMPLATES)):
        title, body = TEMPLATES[(start + offset) % len(TEMPLATES)]
        fingerprint = hashlib.sha256((title + "|" + body).encode()).hexdigest()
        if fingerprint not in state.get("fingerprints", []):
            break
    else:
        return {"status": "no_new_meme"}

    asset = ASSET_DIR / f"{fingerprint[:24]}.png"
    render(title, body, asset)
    if asset.stat().st_size > 8 * 1024 * 1024:
        return {"status": "blocked", "reason": "Asset too large"}

    media = commit_asset(asset)
    when = datetime.now(TZ) + timedelta(minutes=2)
    caption = f"😂 {title}\n\n{body}\n\nयह relatable finance content है — buy/sell recommendation नहीं।\n\n#Evidyarthee #FinanceMemes #IndianInvestors #PersonalFinance #FinancialEducation #StockMarket"
    result = publish(caption, media, when)
    state.setdefault("fingerprints", []).append(fingerprint)
    state.setdefault("runs", []).append({"at": datetime.now(TZ).isoformat(), "title": title, "status": "queued" if result.get("ok") else "failed", "metricool": result})
    save_state(state)
    return {"status": "queued" if result.get("ok") else "failed", "title": title, "metricool": result, "publish_at": when.isoformat()}


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
