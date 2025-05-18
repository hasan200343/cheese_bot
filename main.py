from keep_alive import keep_alive
import discord
from discord.ext import tasks
import json
import random
from datetime import datetime
import os

# Load environment variables
TOKEN = os.getenv("TOKEN")
BIRTHDAY_CHANNEL_ID = 1360308664619106596  # Replace with your actual channel ID

intents = discord.Intents.default()
intents.members = True
bot = discord.Client(intents=intents)

def load_birthdays():
    try:
        with open("birthdays.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def load_gifs():
    try:
        with open("gifs.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# 🎉 List of fun and warm titles
BIRTHDAY_TITLES = [
    "🎉 Happy Birthday to Someone Truly Special!",
    "🎂 Wishing You the Sweetest Birthday Ever!",
    "💖 A Day as Amazing as You Are!",
    "🌟 It's Your Time to Shine!",
    "🎈 Let’s Celebrate YOU Today!",
    "🥳 Cheers to Your Beautiful Journey!"
]


# 💌 Heartwarming wishes
BIRTHDAY_MESSAGES = [
    "You light up every room you walk into, and today, we celebrate the joy you bring into all our lives. 🌟 Wishing you all the love and magic this world has to offer! 💕🎁",
    "Here’s to you — to your kindness, strength, and all the little things that make you incredibly *you*. 💫 I hope today wraps you in joy, warmth, and heartfelt hugs. 🎉🤗",
    "On this beautiful day, may laughter surround you, love embrace you, and dreams guide your path. 🌸 You deserve nothing but the absolute best. Happy birthday! 🎂❤️",
    "Birthdays are for cherishing the people who make life brighter — and you, my friend, are the brightest of them all. ☀️ Here's to happiness, health, and endless surprises! 🎁🎈",
    "Sending you a sky full of blessings and a heart full of gratitude for just being you. 🌌 May your year ahead overflow with love, growth, and unforgettable memories. 🎊💖",
    "You’re more than just a friend — you’re a blessing. 🥰 May today remind you of how loved and appreciated you truly are. Here's to another amazing chapter! 📖✨"
]


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    check_birthdays.start()

@tasks.loop(hours=24)
async def check_birthdays():
    await bot.wait_until_ready()
    from datetime import timezone
    today = datetime.now(timezone.utc).strftime("%m-%d")
    birthdays = load_birthdays()
    gifs = load_gifs()
    channel = bot.get_channel(BIRTHDAY_CHANNEL_ID)

    for user_id, bday in birthdays.items():
        if bday == today:
            user = await bot.fetch_user(int(user_id))
            if user and channel:
                gif_url = random.choice(gifs) if gifs else ""
                title = random.choice(BIRTHDAY_TITLES)
                message = random.choice(BIRTHDAY_MESSAGES)

                embed = discord.Embed(
                    title=title,
                    description=f"{user.mention}, {message}",
                    color=discord.Color.pink()
                )
                if gif_url:
                    embed.set_image(url=gif_url)

                await channel.send(content="@everyone", embed=embed)


# ----------------------
# 🚫 Error Handling
# ----------------------
keep_alive()
token = os.getenv("TOKEN")
if token:
    bot.run(token)
else:
    print(
        "Error: Discord bot token not found. Please set the 'TOKEN' environment variable."
    )

