import json
import os
import time
from pathlib import Path

import requests

API_VERSION = os.getenv("META_GRAPH_API_VERSION", "v26.0")
GRAPH_BASE = f"https://graph.facebook.com/{API_VERSION}"

IG_USER_ID = os.getenv("IG_USER_ID")
ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
MEDIA_SHA = os.getenv("MEDIA_SHA")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")
CONTENT_TYPE = os.getenv("CONTENT_TYPE", "image").lower()

CAPTION_FILE = Path(os.getenv("CAPTION_FILE", "caption.txt"))

TIMEOUT = 30
MAX_POLL_SECONDS = 300
POLL_INTERVAL_SECONDS = 10


class MetaAPIError(RuntimeError):
    pass


def require_config():
    missing = []
    for name, value in {
        "IG_USER_ID": IG_USER_ID,
        "PAGE_ACCESS_TOKEN": ACCESS_TOKEN,
        "MEDIA_SHA": MEDIA_SHA,
        "GITHUB_REPOSITORY": GITHUB_REPOSITORY,
    }.items():
        if not value:
            missing.append(name)

    if missing:
        raise RuntimeError(f"Missing required configuration: {', '.join(missing)}")

    if CONTENT_TYPE not in {"image", "reel"}:
        raise RuntimeError("CONTENT_TYPE must be 'image' or 'reel'")

    if not CAPTION_FILE.exists():
        raise RuntimeError(f"Caption file not found: {CAPTION_FILE}")


def api_request(method: str, path: str, **kwargs):
    url = f"{GRAPH_BASE}/{path.lstrip('/')}"
    params = kwargs.pop("params", {})
    params["access_token"] = ACCESS_TOKEN

    response = requests.request(
        method,
        url,
        params=params,
        timeout=TIMEOUT,
        **kwargs,
    )

    try:
        payload = response.json()
    except ValueError:
        payload = {"raw": response.text}

    if not response.ok or "error" in payload:
        error = payload.get("error", payload)
        raise MetaAPIError(
            f"Meta API request failed ({response.status_code}): "
            f"{json.dumps(error, ensure_ascii=False)}"
        )

    return payload


def public_media_url(filename: str) -> str:
    return f"https://raw.githubusercontent.com/{GITHUB_REPOSITORY}/{MEDIA_SHA}/{filename}"


def load_caption() -> str:
    caption = CAPTION_FILE.read_text(encoding="utf-8").strip()
    if not caption:
        raise RuntimeError("caption.txt is empty")

    if len(caption) > 2200:
        raise RuntimeError(f"Caption is {len(caption)} characters; maximum is 2,200")

    if caption.count("#") > 30:
        raise RuntimeError("Caption contains more than 30 hashtags")

    return caption


def wait_for_container(container_id: str):
    deadline = time.monotonic() + MAX_POLL_SECONDS

    while time.monotonic() < deadline:
        payload = api_request(
            "GET",
            f"/{container_id}",
            params={"fields": "status_code,status"},
        )
        status = payload.get("status_code")
        print(f"Instagram container {container_id}: {status}")

        if status in {"FINISHED", "PUBLISHED"}:
            return

        if status in {"ERROR", "EXPIRED"}:
            raise MetaAPIError(
                f"Instagram media container {container_id} entered terminal state: "
                f"{json.dumps(payload, ensure_ascii=False)}"
            )

        time.sleep(POLL_INTERVAL_SECONDS)

    raise TimeoutError(
        f"Instagram media container {container_id} was not ready after "
        f"{MAX_POLL_SECONDS} seconds"
    )


def create_container(caption: str) -> str:
    if CONTENT_TYPE == "image":
        media_url = public_media_url("post.png")
        print(f"Creating Instagram image container from {media_url}")
        payload = api_request(
            "POST",
            f"/{IG_USER_ID}/media",
            data={"image_url": media_url, "caption": caption},
        )
    else:
        media_url = public_media_url("reel.mp4")
        print(f"Creating Instagram Reel container from {media_url}")
        payload = api_request(
            "POST",
            f"/{IG_USER_ID}/media",
            data={
                "media_type": "REELS",
                "video_url": media_url,
                "caption": caption,
                "share_to_feed": "true",
            },
        )

    creation_id = payload.get("id")
    if not creation_id:
        raise MetaAPIError(f"Meta did not return a creation id: {payload}")

    return creation_id


def publish_container(creation_id: str) -> str:
    payload = api_request(
        "POST",
        f"/{IG_USER_ID}/media_publish",
        data={"creation_id": creation_id},
    )
    media_id = payload.get("id")
    if not media_id:
        raise MetaAPIError(f"Meta did not return a published media id: {payload}")
    return media_id


def main():
    require_config()
    caption = load_caption()

    print(f"Publishing daily Instagram {CONTENT_TYPE} post")
    creation_id = create_container(caption)
    print(f"Created container: {creation_id}")

    wait_for_container(creation_id)

    media_id = publish_container(creation_id)
    print(f"INSTAGRAM_PUBLISHED_MEDIA_ID={media_id}")
    print("Instagram publish completed successfully.")


if __name__ == "__main__":
    main()
