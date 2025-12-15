Discord Image Generator Bot using Stable Diffusion (AUTOMATIC1111)

This project is a Discord bot that generates AI images using a locally hosted
Stable Diffusion model through AUTOMATIC1111. The bot does not rely on any paid
APIs and performs image generation entirely on the local machine using GPU
acceleration.

The bot listens to Discord commands, sends prompts to a local Stable Diffusion
REST API, and returns the generated image back to the Discord channel.

--------------------------------------------------------------------

Features

- Generate AI images using a Discord command (!image)
- Uses Stable Diffusion locally without paid APIs
- GPU-accelerated image generation
- Async-safe request handling to keep the bot responsive
- Cooldown system to prevent command spam
- Clean and modular project structure
- Can be extended later to cloud or API-based image generation

--------------------------------------------------------------------

Tech Stack

- Python
- discord.py
- Stable Diffusion (AUTOMATIC1111)
- REST API (local inference)
- Requests
- Pillow
- Asyncio
- NVIDIA GPU for local execution

--------------------------------------------------------------------

How It Works

Discord User
    |
    |  !image <prompt>
    v
Discord Bot (Python)
    |
    |  HTTP request
    v
Local Stable Diffusion API (127.0.0.1:7860)
    |
    v
Stable Diffusion (AUTOMATIC1111)
    |
    v
Generated Image
    |
    v
Image sent back to Discord

--------------------------------------------------------------------

Prerequisites

- Python 3.12 for the Discord bot
- Python 3.10 for Stable Diffusion WebUI
- NVIDIA GPU with CUDA support
- Stable Diffusion WebUI (AUTOMATIC1111)
- Discord bot token

--------------------------------------------------------------------

Setup Instructions

1. Clone the repository

   git clone <your-repo-url>
   cd <repo-folder>

2. Create and activate a virtual environment

   python -m venv .venv
   .venv\Scripts\activate

3. Install required dependencies

   pip install -r requirements.txt

4. Configure environment variables

   Create a .env file and add:

   DISCORD_TOKEN=your_discord_bot_token_here

5. Start Stable Diffusion with API enabled

   In webui-user.bat, ensure the following line is present:

   set COMMANDLINE_ARGS=--api

   Then run:

   webui-user.bat

   Confirm Stable Diffusion is running at:
   http://127.0.0.1:7860

6. Run the Discord bot

   python bot.py

   The bot should appear online in Discord.

--------------------------------------------------------------------

Usage

In any Discord channel where the bot is added, use:

!image a futuristic cyberpunk bike

The bot will generate and send an AI-generated image based on the prompt.
