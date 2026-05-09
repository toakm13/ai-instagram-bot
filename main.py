import os
from openai import OpenAI
from datetime import datetime

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -----------------------------------
# MARKET CONTEXT
# -----------------------------------

market_context = """
Indian market showing mixed sentiment.
Track:
- Nifty structure
- OI positioning
- Global cues
- Smart money behavior
- Trader psychology
"""

# -----------------------------------
# AI PROMPT
# -----------------------------------

prompt = f"""
You are an institutional market analyst.

Generate HIGH-QUALITY financial content for Instagram and Facebook.

The content must:
- Feel current
- Feel intelligent
- Avoid generic motivation
- Avoid buy/sell tips
- Focus on structure, psychology, positioning

Based on this market context:
{market_context}

Generate:

1. Morning Market Analysis Post
2. Midday Meme Idea
3. Evening Market Wrap
4. Weekend Macro Analysis
5. 30-second Reel Script

Tone:
- Professional
- Insightful
- Sharp
- Finance-native
- Indian stock market focused

Avoid:
- Generic content
- Cringe motivation
- Guaranteed returns
"""

# -----------------------------------
# OPENAI RESPONSE
# -----------------------------------

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "system", "content": "You are a professional market intelligence desk."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.9
)

content = response.choices[0].message.content

# -----------------------------------
# SAVE CONTENT
# -----------------------------------

with open("generated_content.txt", "w", encoding="utf-8") as file:
    file.write(content)

print("AI market content generated successfully!")
print(content)
