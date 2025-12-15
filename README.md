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
- Uses Stable Diffusion locally (no paid APIs)
- GPU-accelerated image generation
- Async-safe request handling
- Cooldown system to prevent spam
- Clean and modular project structure
- Easy to extend to cloud or API-based solutions later

--------------------------------------------------------------------

Tech Stack

- Python
- discord.py
- Stable Diffusion (AUTOMATIC1111)
- REST API (local inference)
- Requests
- Pillow
- Asyncio
- NVIDIA GPU (local execution)

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
Sent back to Discord

--------------------------------------------------------------------

Prerequisites

- Python 3.12 (for Discord bot)
- Python 3.10 (for Stable Diffusion WebUI)
- NVIDIA GPU with CUDA support
- Stable Diffusion WebUI (AUTOMATIC1111)
- Discord bot token

--------------------------------------------------------------------

Setup Instructions

1. Clone the repository

   git clone <your-repo-url>
   cd <repo-folder>

2. Create and activate virtual environment

   python -m venv .venv
   .venv\Scripts\activate

3. Install dependencies

   pip install -r requirements.txt

4. Configure environment variables

   Create a .env file with the following content:

   DISCORD_TOKEN=your_discord_bot_token_here

   Note: Do not upload the .env file to GitHub.

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

In any Discord channel where the bot is added:

!image a futuristic cyberpunk bike

The bot will generate and send an image based on the prompt.

--------------------------------------------------------------------

Security Notes

- Bot token is stored in .env and never committed
- Virtual environment (.venv) is excluded from GitHub
- Generated images are ignored using .gitignore
- Stable Diffusion files and models are not included in the repository

--------------------------------------------------------------------

Limitations

- Stable Diffusion must be running locally
- System must remain powered on
- Not intended for large-scale public deployment
- Real person likeness is approximate due to model behavior

--------------------------------------------------------------------

Future Improvements

- Slash command support (/image)
- Prompt presets and styles
- Automatic negative prompts
- Queue system for multiple users
- Cloud or API-based deployment
- Additional image configuration options

--------------------------------------------------------------------

Author

This project was built as a real-world application to explore Discord bot
development, AI model integration, REST APIs, async programming, and local GPU
inference.

--------------------------------------------------------------------

License

This project is intended for educational and personal use.
