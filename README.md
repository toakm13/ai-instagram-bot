# AI Market Content Bot

Daily market-content automation for Instagram.

## Pipeline

1. GitHub Actions starts at 09:00 IST every day.
2. main.py downloads recent NIFTY 50 or BANK NIFTY 15-minute data.
3. It validates the data, builds a candlestick chart, creates a 1080x1080 JPEG, and writes caption.txt.
4. The generated files are committed to main.
5. The workflow publishes the exact committed image to Instagram through Meta Graph API v26.0.
6. Instagram media containers are polled until they are ready before media_publish.
7. Any Meta error fails the workflow; the bot no longer prints a false success message.

## Required GitHub Actions secrets

PAGE_ACCESS_TOKEN
A currently valid Page Access Token with the required Instagram publishing permissions.

IG_USER_ID
The Instagram Professional Account ID connected to the Page.

The previous token was observed in the September 9, 2026 workflow log as expired on May 9, 2026. A new token must be stored before publishing can succeed.

## Manual runs

The workflow supports two content types:

- image: normal daily feed post
- reel: generates reel.mp4 and publishes it as a Reel

## Meta requirements

The Instagram account must be a Professional account (Business or Creator). For the Facebook Login/Page-backed flow, the Page must be linked to that Instagram account.

## Development

Install dependencies and run:

    pip install -r requirements.txt
    pytest -q
    python main.py

For a Reel, install FFmpeg and run:

    python video.py
