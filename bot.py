import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from dotenv import load_dotenv
from pathlib import Path
import os
import requests
import base64
from PIL import Image
from io import BytesIO

# Paths & Environment
BASE_DIR = Path(__file__).parent
IMAGES_DIR = BASE_DIR / "images"
IMAGES_DIR.mkdir(exist_ok=True)

load_dotenv(dotenv_path=BASE_DIR / ".env")
TOKEN = os.getenv("DISCORD_TOKEN")

# Bot Setup
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Events
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Bot is online and ready.")

# Commands
@bot.command()
async def ping(ctx):
    await ctx.send("pong")

# Image Generation (LOCAL STABLE DIFFUSION)
async def generate_image(prompt: str) -> str:
    url = "http://127.0.0.1:7860/sdapi/v1/txt2img"

    payload = {
        "prompt": prompt,
        "steps": 20,
        "width": 512,
        "height": 512,
        "cfg_scale": 7
    }

    def call_sd():
        r = requests.post(url, json=payload, timeout=600)
        r.raise_for_status()
        return r.json()

    data = await asyncio.to_thread(call_sd)

    if "images" not in data or not data["images"]:
        raise RuntimeError("Stable Diffusion returned no images")

    image_base64 = data["images"][0]

    if "," in image_base64:
        image_base64 = image_base64.split(",", 1)[1]

    image_bytes = base64.b64decode(image_base64)
    image = Image.open(BytesIO(image_bytes))

    output_path = IMAGES_DIR / "output.png"
    image.save(output_path)

    return str(output_path)

# !image Command

@bot.command()
@cooldown(1, 30, BucketType.user)
async def image(ctx, *, prompt: str = None):
    if not prompt:
        await ctx.send("❌ Please provide a prompt.\nExample: `!image a cat in space`")
        return

    async with ctx.typing():
        image_path = await generate_image(prompt)

    await ctx.send(
        # content=f"🖼️ Generated image for:\n**{prompt}**",
        file=discord.File(image_path)
    )

# Cooldown Error
@image.error
async def image_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(
            f"⏳ Please wait {int(error.retry_after)} seconds before generating another image."
        )

# Run Bot
bot.run(TOKEN)

