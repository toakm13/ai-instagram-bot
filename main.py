import random
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# -----------------------------------
# DATE
# -----------------------------------

now = datetime.now()
date_text = now.strftime("%Y-%m-%d")
day = now.strftime("%A")

# -----------------------------------
# CONTENT DATABASE
# -----------------------------------

market_structures = [
    "Nifty showing range-bound behavior near resistance.",
    "Option writers active at higher levels.",
    "Volatility expected to remain elevated near expiry.",
    "Market sentiment remains cautious despite positive cues.",
    "Put writers defending support aggressively."
]

smart_money_views = [
    "Institutions appear patient near key levels.",
    "Retail positioning looks overly directional.",
    "Smart money appears focused on volatility selling.",
    "Aggressive hedging visible near expiry zones."
]

psychology_lines = [
    "Discipline matters more than prediction.",
    "Risk management beats emotional trading.",
    "The market rewards patience.",
    "Structure matters more than excitement."
]

meme_templates = [
    "Buying breakout after 3 green candles.",
    "Holding losing options hoping for reversal.",
    "Expiry traders after sudden reversal.",
    "Retail buying top while institutions exit.",
    "FOMO traders entering late."
]

reel_hooks = [
    "Most traders got trapped today...",
    "This is why retail loses money near expiry...",
    "The market rewards structure, not emotions...",
    "What smart money did differently today..."
]

# -----------------------------------
# POSTS
# -----------------------------------

morning_post = f"""
📈 MORNING MARKET ANALYSIS

{random.choice(market_structures)}

{random.choice(smart_money_views)}

Key Insight:
{random.choice(psychology_lines)}

#Nifty #BankNifty #Trading
"""

meme_post = f"""
😂 MARKET MEME

{random.choice(meme_templates)}

Reality:
{random.choice(psychology_lines)}

#TradingMemes #StockMarket
"""

evening_wrap = f"""
📊 EVENING MARKET WRAP

{random.choice(market_structures)}

Observation:
{random.choice(smart_money_views)}

Learning:
{random.choice(psychology_lines)}

#MarketWrap #TradingPsychology
"""

weekend_analysis = f"""
🌍 WEEKEND MARKET OUTLOOK

{random.choice(market_structures)}

Institutional View:
{random.choice(smart_money_views)}

Reminder:
{random.choice(psychology_lines)}

#WeeklyAnalysis #Nifty
"""

reel_script = f"""
🎥 REEL SCRIPT

Hook:
{random.choice(reel_hooks)}

Body:
{random.choice(market_structures)}

Ending:
{random.choice(psychology_lines)}
"""

# -----------------------------------
# SAVE TEXT CONTENT
# -----------------------------------

all_content = f"""
==============================
MORNING POST
==============================

{morning_post}

==============================
MEME POST
==============================

{meme_post}

==============================
EVENING WRAP
==============================

{evening_wrap}

==============================
WEEKEND ANALYSIS
==============================

{weekend_analysis}

==============================
REEL SCRIPT
==============================

{reel_script}
"""

with open("generated_content.txt", "w", encoding="utf-8") as file:
    file.write(all_content)

# -----------------------------------
# CREATE IMAGE POST
# -----------------------------------

img = Image.new("RGB", (1080, 1080), color=(15, 15, 15))
draw = ImageDraw.Draw(img)

text = f"""
EVidyarthee

{random.choice(market_structures)}

{random.choice(smart_money_views)}

{random.choice(psychology_lines)}
"""

try:
    font = ImageFont.truetype("arial.ttf", 42)
except:
    font = ImageFont.load_default()

draw.multiline_text(
    (80, 200),
    text,
    fill=(255, 255, 255),
    font=font,
    spacing=20,
)

image_name = f"post_{date_text}.png"
img.save(image_name)

print("✅ Content generated successfully!")
print(all_content)
print(f"✅ Image saved: {image_name}")
