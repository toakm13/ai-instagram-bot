import requests
import os

IG_USER_ID = os.getenv("IG_USER_ID")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")

VIDEO_URL = "https://github.com/toakm13/ai-instagram-bot/raw/main/reel.mp4"

caption = """
📈 AI Market Update

#stockmarket #trading #investing #nifty #banknifty
"""

create_url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media"

create_payload = {
    "media_type": "REELS",
    "video_url": VIDEO_URL,
    "caption": caption,
    "access_token": PAGE_ACCESS_TOKEN
}

r = requests.post(create_url, data=create_payload)
result = r.json()

print(result)

creation_id = result.get("id")

publish_url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media_publish"

publish_payload = {
    "creation_id": creation_id,
    "access_token": PAGE_ACCESS_TOKEN
}

r2 = requests.post(publish_url, data=publish_payload)

print(r2.json())
