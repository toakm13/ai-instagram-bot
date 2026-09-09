import pandas as pd
import pytest

import main
import post


def test_caption_has_market_data():
    frame = pd.DataFrame(
        {
            "Open": list(range(100, 112)),
            "High": [101] * 12,
            "Low": [99] * 12,
            "Close": list(range(100, 112)),
            "Volume": [1000] * 12,
        }
    )

    caption, overlay = main.build_caption("^NSEI", frame)

    assert "NIFTY 50" in caption
    assert "Last:" in caption
    assert "Move:" in caption
    assert "#NIFTY50" in caption
    assert "NIFTY 50" in overlay


def test_caption_validation(tmp_path, monkeypatch):
    path = tmp_path / "caption.txt"
    path.write_text("hello #test", encoding="utf-8")
    monkeypatch.setattr(post, "CAPTION_FILE", path)
    assert post.load_caption() == "hello #test"


def test_caption_rejects_oversize(tmp_path, monkeypatch):
    path = tmp_path / "caption.txt"
    path.write_text("x" * 2201, encoding="utf-8")
    monkeypatch.setattr(post, "CAPTION_FILE", path)

    with pytest.raises(RuntimeError, match="2,200"):
        post.load_caption()


def test_public_media_url(monkeypatch):
    monkeypatch.setattr(post, "GITHUB_REPOSITORY", "toakm13/ai-instagram-bot")
    monkeypatch.setattr(post, "MEDIA_SHA", "abc123")

    assert post.public_media_url("post.png").endswith("/abc123/post.png")


def test_meta_error_is_raised(monkeypatch):
    def fake_request(*args, **kwargs):
        raise post.MetaAPIError("invalid token")

    monkeypatch.setattr(post, "api_request", fake_request)
    monkeypatch.setattr(post, "IG_USER_ID", "123")
    monkeypatch.setattr(post, "ACCESS_TOKEN", "expired")
    monkeypatch.setattr(post, "MEDIA_SHA", "abc")
    monkeypatch.setattr(post, "GITHUB_REPOSITORY", "toakm13/ai-instagram-bot")
    monkeypatch.setattr(post, "CONTENT_TYPE", "image")

    with pytest.raises(post.MetaAPIError, match="invalid token"):
        post.create_container("test")
