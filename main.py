from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import textwrap
import random

today = datetime.now().strftime("%d %B %Y")

headlines = [
    "NIFTY closes strong amid bullish momentum",
    "Banking stocks lead market rally",
    "IT sector gains after global optimism",
    "FII buying boosts investor confidence",
    "Markets remain volatile before key data"
]

headline = random.choice(headlines)

psychology_lines = [
    "Discipline beats emotion in trading.",
    "Risk management creates consistency.",
    "Patience is a trader’s superpower."
]

psychology = random.choice(psychology_lines)

img = Image.new("RGB", (1080, 1080), color=(15, 15, 15))
draw = ImageDraw.Draw(img)

title_font = ImageFont.load_default()
text_font = ImageFont.load_default()

draw.text((40, 50), "AI MARKET UPDATE", fill="white", font=title_font)
draw.text((40, 120), today, fill="gray", font=text_font)

wrapped = textwrap.fill(headline, width=25)
draw.text((40, 250), wrapped, fill="white", font=text_font)

draw.text((40, 500), "TRADING PSYCHOLOGY", fill="orange", font=text_font)

wrapped2 = textwrap.fill(psychology, width=30)
draw.text((40, 560), wrapped2, fill="white", font=text_font)

filename = f"post_{datetime.now().strftime('%Y-%m-%d')}.png"
img.save(filename)

print(f"Created {filename}")
