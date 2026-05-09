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
    "Put writers defending support aggressively.",
]

smart_money_views = [
    "Institutions appear patient near key levels.",
    "Retail positioning looks overly directional.",
    "Smart money appears focused on volatility selling.",
    "Aggressive hedging visible near expiry zones.",
]

psychology_lines = [
    "Discipline matters more than prediction.",
    "Risk management beats emotional trading.",
    "The market rewards patience.",
    "Structure matters more than excitement.",
print(f"✅ Image saved: {image_name}")
