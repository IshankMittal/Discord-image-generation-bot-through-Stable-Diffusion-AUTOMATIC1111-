import asyncio
import time
import discord
from discord import app_commands
from dotenv import load_dotenv
from pathlib import Path
import os
import requests
import base64
from PIL import Image
from io import BytesIO
from datetime import datetime

# Paths & Environment
BASE_DIR = Path(__file__).parent
IMAGES_DIR = BASE_DIR / "images"
IMAGES_DIR.mkdir(exist_ok=True)

load_dotenv(dotenv_path=BASE_DIR / ".env")
TOKEN = os.getenv("DISCORD_TOKEN")

# Cooldown Config
COOLDOWN_SECONDS = 30
user_cooldowns = {}

# Discord Client Setup
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Stable Diffusion Image Generation
async def generate_image(prompt: str, username: str) -> str:
    url = "http://127.0.0.1:7860/sdapi/v1/txt2img"

    payload = {
        "prompt": prompt,
        "steps": 20,
        "width": 512,
        "height": 512,
        "cfg_scale": 7
    }

    def call_sd():
        response = requests.post(url, json=payload, timeout=600)
        response.raise_for_status()
        return response.json()

    data = await asyncio.to_thread(call_sd)

    if "images" not in data or not data["images"]:
        raise RuntimeError("Stable Diffusion returned no images")

    image_base64 = data["images"][0]
    if "," in image_base64:
        image_base64 = image_base64.split(",", 1)[1]

    image_bytes = base64.b64decode(image_base64)
    image = Image.open(BytesIO(image_bytes))

    # Create user directory
    user_dir = IMAGES_DIR / username
    user_dir.mkdir(exist_ok=True)

    # Timestamped filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_path = user_dir / f"{timestamp}.png"

    image.save(output_path)
    return str(output_path)

# Slash Command: /image
@tree.command(
    name="image",
    description="Generate an AI image using Stable Diffusion (local)"
)
@app_commands.describe(prompt="Describe the image you want to generate")
async def image(interaction: discord.Interaction, prompt: str):
    user_id = interaction.user.id
    now = time.time()

    # Cooldown check
    last_used = user_cooldowns.get(user_id, 0)
    remaining = COOLDOWN_SECONDS - (now - last_used)

    if remaining > 0:
        await interaction.response.send_message(
            f"⏳ Please wait {int(remaining)} seconds before generating another image.",
            ephemeral=True
        )
        return

    # Update cooldown
    user_cooldowns[user_id] = now

    await interaction.response.defer()

    try:
        image_path = await generate_image(prompt, interaction.user.name)

        await interaction.followup.send(
            file=discord.File(image_path)
        )

    except Exception as e:
        await interaction.followup.send(
            content=f"❌ Error generating image:\n`{str(e)}`"
        )

# Events
@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {client.user}")
    print("Slash commands synced. Bot is ready.")

# Run Bot
client.run(TOKEN)
