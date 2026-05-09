import random
from datetime import datetime

# -----------------------------------
# DATE & DAY
# -----------------------------------

today = datetime.now()
day = today.strftime("%A")

# -----------------------------------
# MARKET ANALYSIS DATA
# -----------------------------------

market_structures = [
    "Market showing range-bound behavior near key resistance.",
    "Volatility expansion possible near expiry.",
    "Call writers active at higher levels.",
    "Put writers attempting to defend support zones.",
    "Market sentiment remains cautious despite positive global cues.",
]

smart_money_views = [
    "Smart money appears patient near resistance.",
    "Institutions seem to prefer selling volatility.",
    "Aggressive positioning visible near expiry levels.",
    "Retail traders appear overly directional.",
]

psychology_lines = [
    "Most traders react emotionally to volatility.",
    "Discipline matters more than prediction.",
    "Structured risk management beats aggressive trading.",
    "Market rewards patience, not excitement.",
]

meme_templates = [
    "Buying breakout after 3 green candles.",
    "Holding losing options hoping for reversal.",
    "Expiry traders after sudden reversal.",
    "Retail buying top while institutions quietly exit.",
    "FOMO traders entering after big move already happened.",
]

reel_hooks = [
    "Most traders got trapped today...",
    "This is why retail loses money near expiry...",
    "The market rewards structure, not emotions...",
    "What smart money did differently today...",
]

# -----------------------------------
# GENERATE POSTS
# -----------------------------------

morning_post = f"""
📈 MORNING MARKET ANALYSIS

{random.choice(market_structures)}

{random.choice(smart_money_views)}

Key Insight:
{random.choice(psychology_lines)}

#Nifty #BankNifty #StockMarket #Trading
"""

meme_post = f"""
😂 MARKET MEME

{random.choice(meme_templates)}

Reality:
{random.choice(psychology_lines)}

#TradingMemes #Nifty #OptionsTrading
"""

evening_wrap = f"""
📊 EVENING MARKET WRAP

Today's market reflected:
{random.choice(market_structures)}

Observation:
{random.choice(smart_money_views)}

Learning:
{random.choice(psychology_lines)}

#MarketWrap #TradingPsychology
"""

weekend_analysis = f"""
🌍 WEEKEND MARKET OUTLOOK

This week showed:
{random.choice(market_structures)}

Institutional View:
{random.choice(smart_money_views)}

Important Reminder:
{random.choice(psychology_lines)}

#WeeklyAnalysis #StockMarketIndia
"""

reel_script = f"""
🎥 REEL SCRIPT

Hook:
{random.choice(reel_hooks)}

Body:
{random.choice(market_structures)}

Ending:
{random.choice(psychology_lines)}

#Reels #Trading #Finance
"""

# -----------------------------------
# SAVE CONTENT
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

print("✅ FREE AI-style market content generated successfully!")
print(all_content)
